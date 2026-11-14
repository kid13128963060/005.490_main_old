Write-Host "确认要覆盖性复制文件吗"


    Write-Host "正在覆盖性复制文件"
    Copy-Item -Path "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\PathHistory.json" -Destination "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\" -Recurse -Force
    Copy-Item -Path "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\Preferences.json" -Destination "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\" -Recurse -Force
    Copy-Item -Path "C:\Users\Administrator\AppData\Roaming\Listary\UserProfile\Settings\SearchHistory.json" -Destination "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\" -Recurse -Force
    Copy-Item -Path "C:\Users\Administrator\AppData\Roaming\IrfanView\i_view64.ini" -Destination "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_238_irfanview!2_设置备份\" -Recurse -Force
    Copy-Item -Path "C:\Users\Administrator\AppData\Roaming\Ditto\005_211_Ditto!2_数据备份.db" -Destination "E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_211_Ditto!2_数据备份\" -Recurse -Force
    Write-Host "覆盖性复制文件 ok"