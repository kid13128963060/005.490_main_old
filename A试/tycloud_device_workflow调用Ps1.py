import subprocess

ps1_path = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\云端_本地配置_互传\云端覆盖本地配置.ps1"

# 调用powershell执行脚本
result = subprocess.run(
    ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1_path],
    capture_output=True,
    text=True
)

print("标准输出：", result.stdout)
print("错误信息：", result.stderr)
print("返回码：", result.returncode) # 0代表成功
