<#
版本: V1.2
连续N秒文件无变化判定同步完成
函数：Wait‑CloudSyncStable
功能：等待天翼云盘同步目录稳定，连续N秒文件无变化代表同步完成
参数：
$MonitorPath：同步盘路径
$StableSeconds：需要连续多少秒无变动判定同步结束
$TimeoutSeconds：最大总等待超时秒数，超时直接退出，避免永久死循环
#>
function Wait-CloudSyncStable {
    param(
        [string]$MonitorPath,
        [int]$StableSeconds = 10,
        [int]$TimeoutSeconds = 300
    )

    # 校验监控路径是否存在
    if (-not (Test-Path -Path $MonitorPath -PathType Container)) {
        Write-Host "❌错误：监控路径不存在 $MonitorPath" -ForegroundColor Red
        return $false
    }

    $stableCount = 0
    $startTime = Get-Date

    while ($true) {
        # 全局超时保护
        $elapsed = (Get-Date) - $startTime
        if ($elapsed.TotalSeconds -ge $TimeoutSeconds) {
            Write-Host "⚠️警告：已达到最大等待超时 $TimeoutSeconds 秒，强制退出等待" -ForegroundColor DarkYellow
            return $false
        }

        # 采集文件元信息：仅拿路径、大小、修改时间，不读取文件内容，不会触发文件占用锁
        $snapshotBefore = Get-ChildItem $MonitorPath -Recurse -File -ErrorAction SilentlyContinue |
        Select-Object FullName, Length, LastWriteTimeUtc

        Start-Sleep -Seconds 1

        $snapshotAfter = Get-ChildItem $MonitorPath -Recurse -File -ErrorAction SilentlyContinue |
        Select-Object FullName, Length, LastWriteTimeUtc

        # 对比两次快照
        $diffResult = Compare-Object -ReferenceObject $snapshotBefore -DifferenceObject $snapshotAfter -Property FullName, Length, LastWriteTimeUtc

        if ($diffResult) {
            # 检测到文件新增/删除/修改，重置稳定计数
            $stableCount = 0
            Write-Host "检测到云盘还在同步，文件发生变动，继续等待..." -ForegroundColor Yellow
        }
        else {
            $stableCount += 1
            Write-Host "同步目录稳定计数 $stableCount / $StableSeconds"
            if ($stableCount -ge $StableSeconds) {
                Write-Host "✅判定：天翼云盘同步目录已经稳定，同步完成" -ForegroundColor Green
                return $true
            }
        }
    }
}

#调用示例，监控E:\备份盘，连续10秒无变动判定完成，最长等待300秒超时
#Wait-CloudSyncStable -MonitorPath "E:\备份盘" -StableSeconds 10 -TimeoutSeconds 300
