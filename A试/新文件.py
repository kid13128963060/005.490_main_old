# Ditto 进程检测+启动 + 虚拟按键 + 完整控件树调试 + 精准三点按钮点击 V6.4
# 修复：不会误点空白关闭弹窗、深度遍历所有控件、打印全部按钮信息

import logging
import sys
import os
import time
import psutil
import win32api
import win32con
import win32gui
import uiautomation as auto

# ===================== 用户配置区 =====================
SELECT_KEY = "OEM3_BACKQUOTE"  # 默认波浪键 `
AUTO_CLICK_THREE_DOTS = True
POPUP_WAIT_SEC = 1.8
# =====================================================

# 完整 26字母 + 全部主键盘符号虚拟键码表
KEY_MAP = {
    # 26字母
    "A": 0x41,
    "B": 0x42,
    "C": 0x43,
    "D": 0x44,
    "E": 0x45,
    "F": 0x46,
    "G": 0x47,
    "H": 0x48,
    "I": 0x49,
    "J": 0x4A,
    "K": 0x4B,
    "L": 0x4C,
    "M": 0x4D,
    "N": 0x4E,
    "O": 0x4F,
    "P": 0x50,
    "Q": 0x51,
    "R": 0x52,
    "S": 0x53,
    "T": 0x54,
    "U": 0x55,
    "V": 0x56,
    "W": 0x57,
    "X": 0x58,
    "Y": 0x59,
    "Z": 0x5A,
    # 数字行符号
    "OEM3_BACKQUOTE": 0xC0,
    "D1": 0x31,
    "D2": 0x32,
    "D3": 0x33,
    "D4": 0x34,
    "D5": 0x35,
    "D6": 0x36,
    "D7": 0x37,
    "D8": 0x38,
    "D9": 0x39,
    "D0": 0x30,
    "OEM_MINUS": 0xBD,
    "OEM_PLUS": 0xBB,
    # 括号符号
    "OEM_4": 0xDB,
    "OEM_5": 0xDC,
    "OEM_6": 0xDD,
    "OEM_1": 0xBA,
    "OEM_7": 0xDE,
    "OEM_COMMA": 0xBC,
    "OEM_PERIOD": 0xBE,
    "OEM_2": 0xBF,
}

# 日志配置
SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_NAME = os.path.join(SCRIPT_FOLDER, "ditto_log.txt")
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO, format="%(asctime)s - %(message)s", encoding="utf-8")
logger = logging.getLogger(__name__)


def get_ditto_pid():
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == "ditto.exe":
                return proc.info["pid"]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def start_ditto_if_not_exist():
    pid = get_ditto_pid()
    if pid:
        print("✅ Ditto 已运行，跳过启动")
        return pid
    print("🔍 启动 Ditto...")
    os.startfile(r"C:\Program Files\Ditto\Ditto.exe")
    time.sleep(3.2)
    return get_ditto_pid()


def send_virtual_key(vk_code):
    print(f"📤 发送虚拟键码 0x{vk_code:02X}")
    win32api.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.1)
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
    print("✅ 按键发送完成")


# ====================== 核心：深度打印全部控件（方案A）======================
def print_all_controls(ctrl, depth=0):
    """递归打印Ditto弹窗所有控件，找出真实三点按钮"""
    try:
        name = ctrl.Name.strip()
        ctype = ctrl.ControlTypeName
        indent = "  " * depth
        print(f"{indent}[{ctype}] 名称: '{name}'")

        # 限制5层深度，足够找到三点按钮
        if depth < 5:
            for child in ctrl.GetChildren():
                print_all_controls(child, depth + 1)
    except Exception:
        pass


def auto_click_ditto_three_dots(ditto_pid):
    print("\n⏳ 等待Ditto弹窗渲染...")
    time.sleep(POPUP_WAIT_SEC)

    # 获取所有顶层窗口
    root = auto.GetRootControl()
    windows = root.GetChildren()
    ditto_win = None

    for w in windows:
        try:
            if w.ProcessId == ditto_pid:
                ditto_win = w
                break
        except Exception:
            continue

    if not ditto_win:
        print("❌ 未找到Ditto弹窗")
        return False

    print("\n========== 【Ditto 全部控件树】 ==========")
    print_all_controls(ditto_win)
    print("========================================\n")

    # 先用官方标准字符「...」匹配 + 「…」双匹配
    btn1 = auto.ButtonControl(searchFromControl=ditto_win, searchDepth=5, Name="...")
    btn2 = auto.ButtonControl(searchFromControl=ditto_win, searchDepth=5, Name="…")

    if btn1.Exists(1):
        btn1.Click()
        print("✅ 成功点击三点菜单（...）")
        return True
    if btn2.Exists(1):
        btn2.Click()
        print("✅ 成功点击三点菜单（…）")
        return True

    print("❌ 未识别到三点按钮")
    return False


def main():
    print("===== Ditto 虚拟按键+自动三点菜单 V6.4 调试版 =====")
    try:
        target_vk = KEY_MAP[SELECT_KEY]
        ditto_pid = start_ditto_if_not_exist()

        # 切桌面防止输入进编辑器
        desktop = win32gui.GetDesktopWindow()
        win32gui.SetForegroundWindow(desktop)
        time.sleep(0.3)

        # 呼出Ditto弹窗
        send_virtual_key(target_vk)

        # 调试+自动点击
        if AUTO_CLICK_THREE_DOTS:
            auto_click_ditto_three_dots(ditto_pid)

        print("\n🎉 脚本执行完毕")

    except Exception as e:
        print(f"❌ 异常: {e}")


if __name__ == "__main__":
    main()
