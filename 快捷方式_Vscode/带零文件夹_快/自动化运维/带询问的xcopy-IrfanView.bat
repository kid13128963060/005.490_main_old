@echo off
echo 确定要本地覆盖云端配置
set /p choice=请输入 [Y/N]: 

if /i "%choice%"=="Y" (
    echo 正在本地覆盖云端配置
    xcopy C:\Users\Administrator\AppData\Roaming\IrfanView E:\备份盘\8000-大文件夹\009-备份文件夹-自\005-238-irfanview!2-设置备份\ /S /E /Y/I
    echo 本地覆盖云端配置 ok
) else if /i "%choice%"=="N" (
    echo 操作已取消！
) else (
    echo 无效输入，请重新运行脚本！
)
pause