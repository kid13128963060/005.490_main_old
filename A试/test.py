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

# 调试版，可以看到输出
result = subprocess.run(cmd, capture_output=True, text=True)
print("返回码：", result.returncode)
print("stdout：", result.stdout)
print("stderr：", result.stderr)
