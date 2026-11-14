@echo off
echo 确定要本地覆盖云端文件
set /p choice=请输入 [Y/N]: 

if /i "%choice%"=="Y" (
    echo 正在本地覆盖云端文件
    xcopy E:\备份盘-副\带0文件夹-副\005-计算机科学、程式、资料,硬件-副\005-400-电脑编程!1-副\BAT-副\试验文件夹-上传 E:\备份盘\带0文件夹\005-计算机科学、程式、资料,硬件\005-400-电脑编程!1\BAT\试验文件夹\ /S /E /Y/I
    echo 本地覆盖云端配置 ok
) else if /i "%choice%"=="N" (
    echo 操作已取消！
) else (
    echo 无效输入，请重新运行脚本！
)
pause