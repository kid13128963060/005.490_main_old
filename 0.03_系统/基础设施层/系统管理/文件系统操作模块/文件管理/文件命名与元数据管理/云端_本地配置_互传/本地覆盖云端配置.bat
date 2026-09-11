@echo off
echo 确定要本地覆盖云端配置
set /p choice=请输入 [Y/N]: 
if /i "%choice%"=="Y" (
    echo 正在本地覆盖云端配置
@echo off
    powershell -WindowStyle Hidden -File "E:\备份盘\带零文件夹\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\Scripts\005_490_first\0.03_系统\基础设施层\系统管理\文件系统操作模块\文件管理\文件命名与元数据管理\云端_本地配置_互传\005_411_PowerShell_本地覆盖云端配置.ps1"
    echo 本地覆盖云端配置 ok
) else if /i "%choice%"=="N" (
    echo 操作已取消！
) else (
    echo 无效输入，请重新运行脚本！
)
pause