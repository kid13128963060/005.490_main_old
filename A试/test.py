import subprocess
import os
import sys

# V1.0 ok
# =====================配置区=====================
run_mode = 2  # 1测试模式，2正常执行模式
task_list_txt = r"E:\备份盘\8000_大文件夹_同\009_备份文件夹_同\list\close_process_list.txt"
# 代码2：保存并关闭文档脚本（路径含中文标点，复制后不要手改）
save_close_script = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App\Combination_Module\work_onekey_save_close_doc.py"
save_close_timeout = 30  # 子脚本超时秒数
# ================================================


def read_process_list(filepath):
    proc_list = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if line:
                    proc_list.append(line)
    return proc_list


def kill_process(proc_name):
    """代码1：强制关闭指定进程"""
    return subprocess.run(["taskkill", "/f", "/im", proc_name], capture_output=True, text=True)


def run_save_close_doc(script_path, timeout=30, check_only=False):
    """代码2：调用 work_onekey_save_close_doc.py，保存并关闭文档"""
    py_exe = sys.executable
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 绝对路径不存在时，回退到脚本同目录下的相对位置
    if not os.path.exists(script_path):
        candidate = os.path.join(base_dir, "App", "Combination_Module", "work_onekey_save_close_doc.py")
        if os.path.exists(candidate):
            script_path = candidate

    print(f"解释器路径(sys.executable自动获取)：{py_exe}")
    print(f"保存关闭脚本：{script_path}")

    if not os.path.exists(py_exe):
        print("❌ python解释器不存在")
        return None
    if not os.path.exists(script_path):
        print("❌ 保存关闭脚本不存在")
        return None

    print("✅ python解释器存在")
    print("✅ 保存关闭脚本存在")

    if check_only:
        return None

    cmd = [py_exe, script_path]
    print(f"准备执行命令：{cmd}")
    try:
        ret = subprocess.run(cmd, capture_output=True, encoding="gbk", errors="replace", timeout=timeout)
        print("---------- stdout ----------")
        print(ret.stdout)
        print("---------- stderr ----------")
        print(ret.stderr)
        print(f"返回码：{ret.returncode}")
        return ret
    except subprocess.TimeoutExpired:
        print("⚠️ 保存关闭脚本执行超时！")
        return None
    except Exception as e:
        print(f"⚠️ 保存关闭脚本调用异常：{repr(e)}")
        return None


def main():
    # ---------- 代码1：按清单强制关闭进程 ----------
    proc_name_list = read_process_list(task_list_txt)
    print(f"读取清单，共 {len(proc_name_list)} 个进程名")

    for proc_name in proc_name_list:
        if run_mode == 1:
            print(f"【测试模式】模拟强制关闭进程：{proc_name}")
            continue

        print(f"正在强制关闭：{proc_name}")
        result = kill_process(proc_name)
        print("stdout：", result.stdout)
        print("stderr：", result.stderr)

    # ---------- 新增代码2：保存并关闭文档 ----------
    print("=" * 40)
    print("开始执行【保存并关闭文档】")
    save_close_ret = run_save_close_doc(save_close_script, save_close_timeout, check_only=(run_mode == 1))
    if save_close_ret is not None:
        print(f"保存并关闭文档脚本返回码：{save_close_ret.returncode}")


if __name__ == "__main__":
    main()
