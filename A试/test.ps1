<#$au3Path = "E:\au3test\卸载.au3"
$exePath = "E:\au3test\卸载_auto.exe"
$aut2exe = "C:\Program Files (x86)\AutoIt3\Aut2Exe\Aut2Exe_x64.exe"

& $aut2exe /in "$au3Path" /out "$exePath" /console
if (-not (Test-Path $exePath)) {
    Write-Host "编译失败"
    exit 1
}
#>
Move-Item -Path "E:\au3test\卸载_auto.exe" -Destination "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\module" -Recurse -Force

$exePath2 = "E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\临\卸载\卸载_auto.exe"

Write-Host "编译完成，启动AutoIt exe"
Start-Process -FilePath $exePath2 -Wait
