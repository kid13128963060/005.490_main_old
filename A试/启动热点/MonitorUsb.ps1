#Requires -PSEdition Desktop
#Requires -RunAsAdministrator
<#
V2.0 ok ok
MonitorUsb.ps1
- 网卡就绪等待8秒
- 热点最多重试 4 次
- 只触发一次，完成后等待60秒退出
#>
$hotspotScriptPath = "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\启动热点\StartMobileHotspot.ps1"

Write-Information "==== USB Wifi网卡监视器启动 ====" -InformationAction Continue
Write-Information "等待USB网卡接入...按 Ctrl+C 终止`n" -InformationAction Continue

$triggered = $false
$foundAdapter = $null

try {
    while (-not $triggered) {
        $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $adapters = @(Get-NetAdapter | Where-Object {
                $_.Status -eq 'Up' -and $_.InterfaceDescription -match 'USB'
            })

        if ($adapters.Count -gt 0) {
            $foundAdapter = $adapters[0]
            Write-Information "【$time】检测到USB网卡：$($foundAdapter.Name)，等待网卡就绪..." -InformationAction Continue

            $readyWait = 8
            $hotspotTryMax = 4   # 最多尝试4次
            $hotspotOk = $false

            for ($i = 1; $i -le $readyWait; $i++) {
                Start-Sleep -Seconds 1
                $chk = Get-NetAdapter -Name $foundAdapter.Name -ErrorAction SilentlyContinue
                if ($chk -and $chk.Status -eq 'Up') {
                    Write-Information "网卡就绪，开始尝试启动热点" -InformationAction Continue
                    for ($t = 1; $t -le $hotspotTryMax; $t++) {
                        Write-Information "第 $t / $hotspotTryMax 次启动热点脚本" -InformationAction Continue
                        powershell.exe -ExecutionPolicy Bypass -File "$hotspotScriptPath"
                        Start-Sleep -Seconds 3
                        $hotspotStatus = Get-MobileHotspotStatus -ErrorAction SilentlyContinue
                        if ($hotspotStatus -and $hotspotStatus.HotspotEnabled) {
                            $hotspotOk = $true
                            Write-Information "✅ 热点启动成功！" -InformationAction Continue
                            break
                        }
                    }
                    break
                }
            }

            if (-not $hotspotOk) {
                Write-Information "⚠️ 4次尝试全部失败，热点未开启" -InformationAction Continue
            }
            Write-Information "等待60秒后关闭监视器脚本" -InformationAction Continue
            $triggered = $true
            Start-Sleep -Seconds 3
        }
        Start-Sleep -Seconds 1
    }
}
finally {
    Write-Information "`n监视器脚本结束" -InformationAction Continue
}
