<<<<<<< HEAD
@echo off
echo 确定要本地覆盖云端配置
set /p choice=请输入 [Y/N]: 
if /i "%choice%"=="Y" (
    echo 正在本地覆盖云端配置
@echo off
    powershell -WindowStyle Hidden -File "E:\备份盘\带零文件夹\005_计算机科学、程式、资料,硬件\005_400_电脑编程!1\Scripts\005_410_PowerShell\005_411_PowerShell_本地覆盖云端配置.ps1"
    echo 本地覆盖云端配置 ok
) else if /i "%choice%"=="N" (
    echo 操作已取消！
) else (
    echo 无效输入，请重新运行脚本！
)
=======
@echo off
echo 确定要本地覆盖云端配置
set /p choice=请输入 [Y/N]: 
if /i "%choice%"=="Y" (
    echo 正在本地覆盖云端配置
@echo off
    powershell -WindowStyle Hidden -File "E:\备份盘\带零文件夹\005_计算机科学、程式、资料,硬件\005_400_电脑编程!1\Scripts\005_410_PowerShell\005_411_PowerShell_本地覆盖云端配置.ps1"
    echo 本地覆盖云端配置 ok
) else if /i "%choice%"=="N" (
    echo 操作已取消！
) else (
    echo 无效输入，请重新运行脚本！
)
>>>>>>> dcb2bd4413adc8b529063e4a9adb64a4d0dc99e9
pause