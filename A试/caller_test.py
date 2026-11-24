# caller_test.py 最终修复版
import subprocess
import os
import sys

# ====================== 配置区 ======================
run_mode = 2  # 1测试模式，2正常执行模式
# 只需要写【被调用脚本的相对路径】，不用写python路径！
# caller_test.py 在 005.490_main_old\A试
TARGET_SCRIPT_REL = (
    r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\test.py"
)
# ====================================================


def main():
    PY_EXE = sys.executable
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TARGET_SCRIPT = os.path.abspath(os.path.join(BASE_DIR, TARGET_SCRIPT_REL))

    print("【测试模式】" if run_mode == 1 else "【正常模式】")
    print(f"解释器路径(sys.executable自动获取): {PY_EXE}")
    print(f"待调用脚本: {TARGET_SCRIPT}")

    if os.path.exists(PY_EXE):
        print("✅ python解释器存在")
    else:
        print("❌ python解释器不存在")
    if os.path.exists(TARGET_SCRIPT):
        print("✅ 目标脚本存在")
    else:
        print("❌ 目标脚本不存在")

    if run_mode == 1:
        return

    cmd = [PY_EXE, TARGET_SCRIPT]
    print(f"准备执行命令：{cmd}")
    try:
        ret = subprocess.run(cmd, capture_output=True, encoding="gbk", errors="replace", timeout=30)
        print("---------- stdout ----------")
        print(ret.stdout)
        print("---------- stderr ----------")
        print(ret.stderr)
        print(f"返回码：{ret.returncode}")
    except subprocess.TimeoutExpired:
        print("⚠️ 执行超时！")
    except Exception as e:
        print(f"⚠️ 调用异常：{repr(e)}")


if __name__ == "__main__":
    main()
