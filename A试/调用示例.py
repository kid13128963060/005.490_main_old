from Combination_Module.run_python_script import run_python_script

# 传入脚本短名（不带 .py / .ps1 后缀）

# 方式A：不捕获输出，脚本print直接打印控制台
res1 = run_python_script("本地覆盖云端配置", capture_output_flag=False)
if res1 is not None:
    print(f"执行返回码 res1.returncode = {res1.returncode}")
