#Requires -PSEdition Desktop
#Requires -RunAsAdministrator

<#
.SYNOPSIS
实时监测USB‑Wifi网卡插入，自动启热点脚本
#>
#Requires -RunAsAdministrator

# 外层定义脚本路径
$hotspotScriptPath = "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\StartMobileHotspot.ps1"

Write-Information "==== USB设备插入监视器已启动 ====" -InformationAction Continue
Write-Information "等待USB设备接入... 按 Ctrl+C 停止监测`n" -InformationAction Continue

Register-CimIndicationEvent -Query "SELECT * FROM Win32_DeviceChangeEvent WHERE EventType = 2" -SourceIdentifier USBInsertMonitor -Action {
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    # 只筛选已经启用的USB‑Wifi网卡
    $usbWifiAdapters = Get-NetAdapter | Where-Object {
        $_.Status -eq 'Up' -and $_.InterfaceDescription -match 'USB'
    }

    if ($usbWifiAdapters) {
        Write-Information "【$time】✅检测USB‑Wifi网卡已插入，准备启动热点脚本" -InformationAction Continue

        # $using: 拿到外层路径，&执行脚本
        if (Test-Path $using:hotspotScriptPath) {
            & $using:hotspotScriptPath
        }
        else {
            Write-Information "文件不存在：$($using:hotspotScriptPath)" -InformationAction Continue
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
}
