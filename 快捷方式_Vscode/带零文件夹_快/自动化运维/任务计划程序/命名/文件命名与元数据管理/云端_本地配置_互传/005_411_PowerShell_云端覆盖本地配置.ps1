# PowerShell 脚本：云端覆盖本地配置
# 该脚本用于监控云盘同步目录中的文件大小变化，并在检测到变化时，自动覆盖本地配置文件。

# 配置：云盘本地同步目录
$SyncFolder = "E:\备份盘"  

# 初始化：记录初始文件大小（递归获取所有文件，存储为哈希表）
$InitialFileSizes = @{}
Get-ChildItem -Path $SyncFolder -Recurse -File | ForEach-Object {
    $InitialFileSizes[$_.FullName] = $_.Length  # 文件大小（字节）
}

Write-Host "初始化完成，监控文件大小变化..." -ForegroundColor Green
 Start-Sleep -Seconds 60  # 等待初始文件大小稳定,云盘同步完成 

# 监控循环：持续检测文件大小变化
while ($true) {
    $hasChange = $false
    
    # 遍历当前文件，对比大小
    Write-Host "开始遍历当前文件"
    Get-ChildItem -Path $SyncFolder -Recurse -File | ForEach-Object {
        $currentSize = $_.Length
        $initialSize = $InitialFileSizes[$_.FullName]
        
        # 如果文件大小不一致，说明文件被修改
        if ($currentSize -ne $initialSize) {
            Write-Host "检测到文件变化：$($_.FullName)" -ForegroundColor Yellow
            Write-Host "  大小变化：$initialSize → $currentSize 字节" -ForegroundColor Yellow
            $hasChange = $true
            return  # 跳出当前遍历
        }
    }

    # 若检测到变化，触发批处理并退出
   if ($hasChange) {  
    Write-Host "云盘同步完成（文件大小变化），触发复制命令..." -ForegroundColor Cyan
    
    # 关闭多个应用程序
    Stop-Process -Name "Listary", "i_view64", "Ditto" -Force
    Start-Sleep -Seconds 10

    #云端配置恢复到本地
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\PathHistory.json" -Destination "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\" -Recurse -Force
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\Preferences.json" -Destination "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\" -Recurse -Force
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\SearchHistory.json" -Destination "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\" -Recurse -Force
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_238_irfanview!2_设置备份\i_view64.ini" -Destination "C:\Users\Administrator\AppData\Roaming\IrfanView\" -Recurse -Force
    Copy-Item -Path "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_211_Ditto!2_数据备份\005_211_Ditto!2_数据备份.db" -Destination "C:\Users\Administrator\AppData\Roaming\Ditto\" -Recurse -Force
    
    #启动关闭的应用
    Start-Process -FilePath "C:\Program Files\Listary\Listary.exe"
    # Listary 已启动
    Start-Process -FilePath "C:\Program Files\Ditto\Ditto.exe"
    # Ditto 已启动
    New-Item -Path "E:\备份盘\带零文件夹\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\同步成功提示文件.txt"

    break  # 仅触发一次，退出监控
}

    # 每隔 7 秒检查一次（可根据需要调整频率）
    Start-Sleep -Seconds 7  
}   Write-Host "执行云端覆盖本地配置操作ok"
