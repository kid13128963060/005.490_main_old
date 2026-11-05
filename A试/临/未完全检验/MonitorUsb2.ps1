# V1.1 稳定版 | 监测USB-WiFi网卡插入，内置WinRT开启移动热点
#Requires -PSEdition Desktop
#Requires -RunAsAdministrator

<#
.SYNOPSIS
实时监测USB‑Wifi网卡热插拔，网卡变为Up状态时，调用WinRT开启系统移动热点
#>

Write-Information "==== USB‑Wifi网卡插入监视器已启动 ====" -InformationAction Continue
Write-Information "等待USB设备接入... 按 Ctrl+C 停止监测`n" -InformationAction Continue

# 注册CIM设备插入事件
Register-CimIndicationEvent -Query "SELECT * FROM Win32_DeviceChangeEvent WHERE EventType = 2" `
    -SourceIdentifier USBInsertMonitor -Action {
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    # 筛选USB网卡，状态Up
    $usbWifiAdapters = Get-NetAdapter | Where-Object {
        $_.Status -eq 'Up' -and $_.InterfaceDescription -match 'USB'
    }

    if ($usbWifiAdapters) {
        Write-Information "【$time】✅检测USB‑Wifi网卡已插入，准备调用WinRT开启移动热点" -InformationAction Continue

        try {
            Add-Type -AssemblyName System.Runtime.WindowsRuntime

            # 获取AsTask泛型方法，用于等待WinRT异步任务
            $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
                    $_.Name -eq 'AsTask' -and
                    $_.GetParameters().Count -eq 1 -and
                    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
                })[0]

            # Await函数定义在Action内部，适配独立运行空间
            function Await($WinRtTask, $ResultType) {
                $m = $asTaskGeneric.MakeGenericMethod($ResultType)
                $taskObj = $m.Invoke($null, @($WinRtTask))
                $taskObj.Wait(-1)
                return $taskObj.Result
            }

            # ========== WinRT类型加载【单行！彻底消除换行语法报错】 ==========
            [Windows.Networking.Connectivity.NetworkInformation, Windows.Networking.Connectivity, ContentType = WindowsRuntime] | Out-Null
            [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager, Windows.Networking.NetworkOperators, ContentType = WindowsRuntime] | Out-Null
            [Windows.Networking.NetworkOperators.NetworkOperatorTetheringOperationResult, Windows.Networking.NetworkOperators, ContentType = WindowsRuntime] | Out-Null
            # ==================================================================

            $cp = [Windows.Networking.Connectivity.NetworkInformation]::GetInternetConnectionProfile()
            if (-not $cp) {
                Write-Information "【$time】⚠️未获取到有效的互联网连接配置文件，无法启动热点" -InformationAction Continue
                return
            }
            $tm = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager]::CreateFromConnectionProfile($cp)

            $r = Await $tm.StartTetheringAsync() ([Windows.Networking.NetworkOperators.NetworkOperatorTetheringOperationResult])
            Write-Information "【$time】热点结果：$($r.Status)" -InformationAction Continue
        }
        catch {
            Write-Information "【$time】❌开启热点发生异常：$($_.Exception.Message)" -InformationAction Continue
        }
    }
}

try {
    while ($true) {
        Wait-Event -SourceIdentifier USBInsertMonitor
    }
}
finally {
    Unregister-Event -SourceIdentifier USBInsertMonitor -ErrorAction SilentlyContinue
    Write-Information "`nUSB监视器已停止，事件订阅已清理" -InformationAction Continue
    Write-Output "脚本执行完毕"
}