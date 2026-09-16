# version:1.9 天翼云盘启动脚本，修复点任务计划【运行】产生log文件冲突；pid锁文件防多实例(纯标准库)；socket网络检测；最大等待秒数配置
import subprocess
import os
import socket
import time
import sys
from datetime import datetime

# 脚本目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(SCRIPT_DIR, "run_log.txt")
lock_file = os.path.join(SCRIPT_DIR, "start_tycloud.lock")

# --------------------------配置参数--------------------------
MAX_WAIT_SEC = 360         # 最大等待总时长【单位秒】，6分钟 = 360秒
CHECK_INTERVAL_SEC = 10    # 每10秒执行一次网络检测
EXE_PATH = r"C:\Program Files\ecloud\eCloud.exe"
WORK_DIR = r"C:\Program Files\ecloud"
# -----------------------------------------------------------


def write_log(msg):
    """日志写入，每次打开写完立刻关闭，降低文件占用时间"""
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} | {msg}\n")
    except Exception as e:
        print(f"【日志写入失败】{str(e)}")


def check_network(timeout=3):
    """socket检测外网连通，True=联网，False=断网"""
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("223.5.5.5", 53))
        s.close()
        return True
    except Exception:
        return False


def is_process_running(process_name: str) -> bool:
    """调用系统tasklist命令检测进程是否存在"""
    try:
        result = subprocess.run(
            ["tasklist", "/fo", "csv", "/nh"],
            capture_output=True,
            text=True,
            encoding="gbk",
            shell=False
        )
        for line in result.stdout.splitlines():
            if process_name.lower() in line.lower():
                return True
        return False
    except Exception as e:
        write_log(f"进程检测异常: {str(e)}")
        return False


def check_pid_exist(pid: int) -> bool:
    """Windows检查pid进程是否还在运行，移除check=True，不抛出CalledProcessError"""
    try:
        ret = subprocess.run(
            ["tasklist", "/fi", f"PID eq {pid}"],
            capture_output=True,
            shell=False
        )
        return ret.returncode == 0
    except Exception:
        return False


def acquire_lock() -> bool:
    """获取锁文件，返回True拿到锁；False已有实例运行"""
    if os.path.exists(lock_file):
        try:
            with open(lock_file, "r", encoding="utf-8") as f:
                old_pid = int(f.read().strip())
            if check_pid_exist(old_pid):
                write_log(f"⚠️检测到已有实例PID={old_pid}正在运行，本次脚本直接退出，避免日志冲突")
                return False
            else:
                # 锁文件残留，进程已经死掉，清理旧锁
                os.remove(lock_file)
                write_log(f"ℹ️清理过期锁文件，旧PID={old_pid}进程已不存在")
        except Exception:
            # 锁文件损坏，直接删除
            try:
                os.remove(lock_file)
                write_log("ℹ️损坏的锁文件已清除")
            except Exception:
                pass
    # 写入当前pid
    with open(lock_file, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))
    return True


def release_lock():
    """释放锁文件"""
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except Exception:
            pass


def main():
    # 获取单实例锁
    if not acquire_lock():
        return
    try:
        if not os.path.exists(EXE_PATH):
            write_log(f"错误：找不到天翼云盘程序 {EXE_PATH}")
            return

        if is_process_running("eCloud.exe"):
            write_log("提示：天翼云盘已经在运行，无需重复启动")
            return

        start_timestamp = time.time()
        write_log(f"开始网络等待，最长等待 {MAX_WAIT_SEC} 秒")

        # 循环等待网络，超时达到MAX_WAIT_SEC直接退出
        while True:
            elapsed_sec = time.time() - start_timestamp
            if elapsed_sec >= MAX_WAIT_SEC:
                write_log(f"⏰已达到最大等待 {MAX_WAIT_SEC}秒，依旧无网络，脚本直接退出，不启动天翼云盘")
                return

            if check_network():
                write_log("✅检测到外网，准备启动天翼云盘")
                break
            else:
                write_log(f"❌当前无外网，继续等待，已等待 {int(elapsed_sec)} 秒")
                time.sleep(CHECK_INTERVAL_SEC)

        # 网络正常，启动云盘
        try:
            subprocess.Popen(
                [EXE_PATH],
                cwd=WORK_DIR,
                shell=False
            )
            write_log("✅ 天翼云盘启动成功")
        except Exception as e:
            write_log(f"❌ 启动异常：{str(e)}")
    finally:
        # 无论正常/异常退出，都删除锁文件
        release_lock()


if __name__ == "__main__":
    main()
