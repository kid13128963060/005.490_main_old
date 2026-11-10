# 64位解释器运行au3源码
Start-Sleep 7
$au3 = "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\JisuPDF_Uninstall_Auto.au3"
$au3x64 = "C:\Program Files (x86)\AutoIt3\AutoIt3_x64.exe"
Start-Process -Wait -FilePath $au3x64 -ArgumentList "`"$au3`""
