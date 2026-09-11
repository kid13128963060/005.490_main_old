<<<<<<< HEAD
$pythonScript = @"
E:\备份盘\带零文件夹\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\Scripts
\005_490_运行与调试\试验夹\005_410_命名\005_430_file_rename_creator_py_T1.py
"@.Replace("`r`n", "").Trim()
# 调用 Python 脚本（参数用空格分隔）
python "$pythonScript" --source "old" --prefix "new" --version 10 `
=======
$pythonScript = @"
E:\备份盘\带零文件夹\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\Scripts
\005_490_运行与调试\试验夹\005_410_命名\005_430_file_rename_creator_py_T1.py
"@.Replace("`r`n", "").Trim()
# 调用 Python 脚本（参数用空格分隔）
python "$pythonScript" --source "old" --prefix "new" --version 10 `
>>>>>>> dcb2bd4413adc8b529063e4a9adb64a4d0dc99e9
--overwrite