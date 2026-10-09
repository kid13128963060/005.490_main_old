# V1.0 实时监测USB‑Wifi网卡插入，直接调用WinRT开启移动热点；替换外部ps1调用，内置代码2全部逻辑
#Requires -PSEdition Desktop
#Requires -RunAsAdministrator

<#
.SYNOPSIS
实时监测USB‑Wifi网卡热插拔，检测到网卡Up状态时，使用WinRT API直接开启系统移动热点
#>

Write-Information "==== USB‑Wifi网卡插入监视器已启动 ====" -InformationAction Continue
Write-Information "等待USB设备接入... 按 Ctrl+C 停止监测`n" -InformationAction Continue

# 注册CIM设备变更事件；EventType=2代表设备插入事件
Register-CimIndicationEvent -Query "SELECT * FROM Win32_DeviceChangeEvent WHERE EventType = 2" `
    -SourceIdentifier USBInsertMonitor -Action {
    $time = Get-Date -Format "yyyy‑MM‑dd HH:mm:ss"

    # 筛选状态为Up、描述包含USB的网卡设备
    $usbWifiAdapters = Get‑NetAdapter | Where‑Object {
        $_.Status -eq 'Up' -and $_.InterfaceDescription -match 'USB'
    }

    if ($usbWifiAdapters) {
        Write‑Information "【$time】✅检测USB‑Wifi网卡已插入，准备调用WinRT开启移动热点" `
            -InformationAction Continue

        # ==========【原& $using:hotspotScriptPath位置，完整嵌入代码2】==========
        try {
            # 加载WinRT程序集，用于异步任务Await封装
            Add‑Type -AssemblyName System.Runtime.WindowsRuntime

            # 查找IAsyncOperation`1对应的AsTask泛型扩展方法
            $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where‑Object {
                    $_.Name -eq 'AsTask' -and
                    $_.GetParameters().Count -eq 1 -and
                    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
                })[0]

            # 封装WinRT异步操作等待函数，在事件Action内部定义，避免跨运行空间作用域丢失
            function Await($WinRtTask, $ResultType) {
                $m = $asTaskGeneric.MakeGenericMethod($ResultType)
                $t = $m.Invoke($null, @($WinRtTask))
                $t.Wait(-1)
                return $t.Result
            }

            # 加载移动热点相关WinRT命名空间
            [Windows.Networking.Connectivity.NetworkInformation, 
            Windows.Networking.Connectivity, ContentType = WindowsRuntime] | Out‑Null
            [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager, 
            Windows.Networking.NetworkOperators, ContentType = WindowsRuntime] | Out‑Null
            [Windows.Networking.NetworkOperators.NetworkOperatorTetheringOperationResult, 
            Windows.Networking.NetworkOperators, ContentType = WindowsRuntime] | Out‑Null

            # 获取当前互联网连接配置文件，构造热点管理器
            $cp = [Windows.Networking.Connectivity.NetworkInformation]::GetInternetConnectionProfile()
            if (-not $cp) {
                Write‑Information "【$time】⚠️未获取到有效的互联网连接配置文件，无法启动热点" `
                    -InformationAction Continue
                return
            }
            $tm = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager]::CreateFromConnectionProfile($cp)

            # 异步执行开启热点，并等待完成获取结果
            $r = Await $tm.StartTetheringAsync() `
            ([Windows.Networking.NetworkOperators.NetworkOperatorTetheringOperationResult])
            Write‑Information "【$time】热点结果：$($r.Status)" -InformationAction Continue
        }
        catch {
            Write‑Information "【$time】❌开启热点发生异常：$($_.Exception.Message)" -InformationAction Continue
        }
        # =====================================================================
    }
}

try {
    while ($true) {
        Wait‑Event -SourceIdentifier USBInsertMonitor
    }
}
finally {
    Unregister‑Event -SourceIdentifier USBInsertMonitor -ErrorAction SilentlyContinue
    Write‑Information "`nUSB监视器已停止，事件订阅已清理" -InformationAction Continue
    Write‑Output "脚本执行完毕"
}
