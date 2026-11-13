import subprocess

sevenzip = r"C:\Program Files\7-Zip\7z.exe"
cmd = [
    sevenzip,
    "a",
    "-t7z",
    "-y",
    "-r",
    r"E:\备份盘\8000_大文件夹_同\009_备份文件夹_同\快捷方式\快捷方式_自.7z",
    r"F:\自动同步_只增加\快捷方式_自\*",
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
