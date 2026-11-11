import subprocess

# au3脚本路径，换成你自己的 mes登录.au3
au3_path = (
    r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\mes登录.au3"
)
autoit_exe = r"C:\Program Files (x86)\AutoIt3\AutoIt3_x64.exe"

# 执行au3脚本
cmd = [autoit_exe, au3_path]
result = subprocess.run(cmd, capture_output=True, text=True)

print("返回码：", result.returncode)
print("输出：", result.stdout)
print("错误：", result.stderr)
