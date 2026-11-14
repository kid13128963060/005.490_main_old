@echo off
echo 确定要云端覆盖本地配置
set /p choice=请输入 [Y/N]: 

if /i "%choice%"=="Y" (
    echo 确定要云端覆盖本地配置
taskkill /IM Listary.exe /F
echo Listary已关闭
    xcopy E:\备份盘\8000-大文件夹\009-备份文件夹-自\005-209-Listary!2-设置\自定义设置 C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\ /S /E /Y/I
    taskkill /IM i_view64.exe /F
    echo i_view64已关闭
    xcopy E:\备份盘\8000-大文件夹\009-备份文件夹-自\005-238-irfanview!2-设置备份 C:\Users\Administrator\AppData\Roaming\IrfanView\ /S /E /Y/I
    taskkill /IM Ditto.exe /F
    echo Ditto已关闭
    xcopy E:\备份盘\8000-大文件夹\009-备份文件夹-自\005-211-Ditto!2-数据备份\ C:\Users\Administrator\AppData\Roaming\Ditto\ /S /E /Y/I
    start "" "C:\Program Files\Ditto\Ditto.exe"
    echo Ditto 已启动
    start "" "C:\Program Files\Listary\Listary.exe"
    echo Listary 已启动
    echo 云端覆盖本地配置 ok
) else if /i "%choice%"=="N" (
    echo 操作已取消！
) else (
    echo 无效输入，请重新运行脚本！
)
pause
