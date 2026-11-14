<<<<<<< HEAD
﻿Write-Host "确认要覆盖性复制文件吗"

    Write-Host "正在本地覆盖云端配置"
# Here-String 多行书写，再替换换行符
$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\PathHistory.json
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\Preferences.json
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\SearchHistory.json
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\IrfanView\i_view64.ini
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_238_irfanview!2_设置备份\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\Ditto\005_211_Ditto!2_数据备份.db
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_211_Ditto!2_数据备份\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

    Write-Host "本地覆盖云端配置 ok"
=======
﻿Write-Host "确认要覆盖性复制文件吗"

    Write-Host "正在本地覆盖云端配置"
# Here-String 多行书写，再替换换行符
$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\PathHistory.json
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\Preferences.json
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\SearchHistory.json
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_209_Listary!2_设置\自定义设置\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\IrfanView\i_view64.ini
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_238_irfanview!2_设置备份\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

$sourcePath =@"
C:\Users\Administrator\AppData\Roaming\Ditto\005_211_Ditto!2_数据备份.db
"@ -replace "`r`n", "\"  # 将换行符替换为\源文件路径
$destinationPath =@"
E:\备份盘\8000_大文件夹\009_备份文件夹_自\005_211_Ditto!2_数据备份\
"@ -replace "`r`n", "\"  # 将换行符替换为\目标文件路径
Copy-Item -Path $sourcePath -Destination $destinationPath -Recurse -Force

    Write-Host "本地覆盖云端配置 ok"
>>>>>>> dcb2bd4413adc8b529063e4a9adb64a4d0dc99e9
