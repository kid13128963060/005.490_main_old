# 脚本路径，放在顶部
$scriptPath = "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\MonitorUsb.ps1"

# 调用（PS5.1 执行，防止闪退）
powershell.exe -ExecutionPolicy Bypass -File $scriptPath
