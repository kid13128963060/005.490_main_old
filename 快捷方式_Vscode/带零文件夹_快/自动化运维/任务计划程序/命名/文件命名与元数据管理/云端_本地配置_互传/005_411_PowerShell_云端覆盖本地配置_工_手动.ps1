
$choice = Read-Host "确定要云端覆盖本地配置吗？请输入 [Y/N]"
if ($choice -eq "Y" -or $choice -eq "y") {
# 关闭多个应用程序
    Stop-Process -Name "Listary", "i_view64", "Ditto" -Force
    Start-Sleep -Seconds 7

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

    Write-Host "执行云端覆盖本地配置操作ok"
} elseif ($choice -eq "N" -or $choice -eq "n") {
    Write-Host "已取消云端覆盖本地配置操作"
} else {
    Write-Host "输入无效，请按要求输入 Y/N"
}