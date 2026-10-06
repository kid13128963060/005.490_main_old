# Ditto V7.4 Ok 基于文档V3.0修复：QPasteClass弹窗不支持WindowPattern，移除restore/set_focus

# 依赖: pip install psutil pywin32 pywinauto

import logging
import sys
import os
import time
import psutil
import win32api
import win32con
import win32gui
import pyautogui

from typing import Optional, cast
from pywinauto import Application
from pywinauto.controls.uiawrapper import UIAWrapper
from Combination_Module.run_python_script import run_python_script, run_script_capture, run_script_get_stdout

# ===================== 用户配置区 =====================
SELECT_KEY = "OEM3_BACKQUOTE"  # 虚拟按键 0xC0 `
AUTO_CLICK_THREE_DOTS = True
POPUP_WAIT_SEC = 1.8
DITTO_EXE_PATH: str = r"C:\Program Files\Ditto\Ditto.exe"
DITTO_PROCESS_NAME = "Ditto.exe"
WAIT_TIMEOUT: int = 10

print("========== 设备识别工作流开始 ==========")

# 获取模拟器标识 read_excel_once，捕获输出
CELL_READ_CONST = run_script_get_stdout("read_excel_once")
if not CELL_READ_CONST:
    print("错误：未找到 read_excel_once 脚本，程序终止")
print(CELL_READ_CONST)

# 鼠标点击偏移配置（全部提取到顶部配置）
if CELL_READ_CONST == "家脑模拟器":
    DOT_DX = 40
    DOT_DY = 387

    MENU_DX = 40
    MENU_DY = 550

    CONFIRM_DX = 83
    CONFIRM_DY = 270

elif CELL_READ_CONST == "工脑模拟器":
    DOT_DX = 40
    DOT_DY = 337

    MENU_DX = 40
    MENU_DY = 495

    CONFIRM_DX = 83
    CONFIRM_DY = 240

# 虚拟键码对照表【26字母 + 主键盘符号】
KEY_MAP = {
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
    "OEM3_BACKQUOTE": 0xC0,  # ` ~
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
    "OEM_4": 0xDB,
    "OEM_5": 0xDC,
    "OEM_6": 0xDD,
    "OEM_1": 0xBA,
    "OEM_7": 0xDE,
    "OEM_COMMA": 0xBC,
    "OEM_PERIOD": 0xBE,
    "OEM_2": 0xBF,
}


SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))

LOG_FILE_NAME: str = os.path.join(SCRIPT_FOLDER, "uia_log.txt")

logging.basicConfig(
    filename=LOG_FILE_NAME, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8"
)

logger = logging.getLogger(__name__)


def get_ditto_pid():
    """获取Ditto PID，未运行返回None"""
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == DITTO_PROCESS_NAME.lower():
                return proc.info["pid"]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def start_ditto_if_not_exist():
    """Ditto不存在则启动，返回PID"""
    pid = get_ditto_pid()
    if pid is not None:
        logger.info("✅检测到Ditto进程已经在运行，跳过启动")
        print("✅检测到Ditto进程已经在运行，跳过启动")
        return pid
    logger.info("🔍未检测Ditto，准备启动Ditto")
    print("🔍未检测Ditto，准备启动Ditto")
    os.startfile(DITTO_EXE_PATH)
    time.sleep(3.0)
    pid = get_ditto_pid()
    logger.info(f"✅Ditto已启动完成 PID={pid}")
    print(f"✅Ditto已启动完成 PID={pid}")
    return pid


def send_virtual_key(vk_code):
    """发送虚拟键码，无Shift"""
    logger.info(f"📤发送虚拟键码: 0x{vk_code:02X}")
    print(f"📤发送虚拟键码: 0x{vk_code:02X}")
    win32api.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.1)
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
    logger.info("✅按键发送完毕")
    print("✅按键发送完毕")


def find_child_by_name(root: UIAWrapper, target_name: str, depth: int = 8) -> Optional[UIAWrapper]:
    """UIA递归遍历控件树，按控件Name文本查找子控件（文档V3.0原版）"""
    if depth <= 0:
        return None
    try:
        children = root.children()
        for child in children:
            child_wrap = cast(UIAWrapper, child)
            ctrl_text = child_wrap.window_text().strip()
            if ctrl_text == target_name.strip():
                return child_wrap
            res = find_child_by_name(child_wrap, target_name, depth - 1)
            if res is not None:
                return res
    except Exception as exc:
        logger.warning(f"递归查找子控件发生异常:{str(exc)}")
    return None


def get_all_descendant_text(root: UIAWrapper) -> str:
    """获取全部后代控件文本（文档V3.0原版）"""
    result_text = ""
    try:
        all_ctrls = root.descendants()
        for ctrl in all_ctrls:
            wrap = cast(UIAWrapper, ctrl)
            txt = wrap.window_text()
            result_text += txt
    except Exception as exc:
        logger.warning(f"获取后代控件文本异常:{str(exc)}")
    return result_text


def click_ditto_option_menu(ditto_pid):
    """连接Ditto悬浮弹窗QPasteClass，pyautogui屏幕坐标点击三点:"""
    print("⏳等待Ditto悬浮窗口渲染...")
    time.sleep(POPUP_WAIT_SEC)
    try:
        app = Application(backend="uia").connect(process=ditto_pid, timeout=8)
        all_wins = app.windows()
        ditto_win = None
        print(f"🔍共找到该进程 {len(all_wins)} 个窗口，逐个打印信息：")
        for idx, w in enumerate(all_wins):
            wrap = cast(UIAWrapper, w)
            win_text = wrap.window_text()
            cls_name = wrap.class_name()
            print(f" 窗口{idx}: text='{win_text}' | class_name='{cls_name}'")
            if cls_name == "QPasteClass":
                ditto_win = wrap
        if ditto_win is None:
            logger.error("❌未找到QPasteClass悬浮窗口")
            return None
        # 点击三点按钮（这里也可以改成相对窗口坐标，一并优化）
        rect = ditto_win.rectangle()
        # 三点按钮：相对于窗口左上角的偏移 dx, dy

        dot_dx = rect.width() - DOT_DX
        dot_dy = DOT_DY

        screen_x = rect.left + dot_dx
        screen_y = rect.top + dot_dy
        # 仅移动鼠标预览，不点击，调试用
        # pyautogui.moveTo(x=screen_x, y=screen_y)
        print(f"三点按钮：窗口内偏移({dot_dx},{dot_dy}) → 屏幕坐标 X={screen_x},Y={screen_y}")
        pyautogui.click(x=screen_x, y=screen_y)
        time.sleep(0.4)
        return ditto_win
    except Exception as e:
        logger.error(f"连接Ditto窗口异常：{e}")
        return None


def step4_delete_unused_clip_items(ditto_win):
    """
    步骤四：
    第一步：点击菜单【删除所有未使用剪贴项】（QPasteClass窗口相对偏移 dx=40 dy=550）
    第二步：延时等待确认弹窗弹出，同样基于QPasteClass窗口左上角偏移，直接点击【确定】；不捕获弹窗窗口
    """
    logger.info("=====进入【步骤四】执行删除操作 =====")
    print("=====进入【步骤四】执行删除操作 =====")

    rect = ditto_win.rectangle()
    win_left = rect.left
    win_top = rect.top
    print(f"Ditto悬浮窗左上角屏幕坐标：left={win_left}, top={win_top}")

    # --------第一步：点击删除菜单项，文档原始测好偏移不变--------
    dx = MENU_DX
    dy = MENU_DY

    menu_x = win_left + dx
    menu_y = win_top + dy
    print(f"删除菜单项 相对偏移 dx={dx}, dy={dy} → 屏幕 X={menu_x}, Y={menu_y}")
    # pyautogui.moveTo(x=menu_x, y=menu_y)

    pyautogui.click(x=menu_x, y=menu_y)

    # 等待确认弹窗弹出
    time.sleep(0.8)

    # --------第二步：点击确认弹窗【确定】按钮，同样基于QPasteClass左上角取相对偏移，不捕获弹窗对象--------
    # confirm_dx：确定按钮相对于QPasteClass窗口左上角向右像素
    # confirm_dy：确定按钮相对于QPasteClass窗口左上角向下像素

    confirm_dx = CONFIRM_DX
    confirm_dy = CONFIRM_DY

    confirm_x = win_left + confirm_dx
    confirm_y = win_top + confirm_dy
    print(
        f"确认弹窗【确定】相对偏移 confirm_dx={confirm_dx}, confirm_dy={confirm_dy} → 屏幕 X={confirm_x}, Y={confirm_y}"
    )
    # 仅移动鼠标预览，不点击，调试用
    # pyautogui.moveTo(x=confirm_x, y=confirm_y, duration=0.3)

    pyautogui.click(x=confirm_x, y=confirm_y)

    logger.info("✅【步骤四全部完成】删除+确认点击完毕")
    print("✅【步骤四全部完成】删除+确认点击完毕")
    time.sleep(1.2)
    return True


def main():
    print("===== Ditto V7.2 虚拟按键+pywinautoUIA点击三点菜单 =====")
    logger.info("============脚本开始执行============")
    try:
        if SELECT_KEY not in KEY_MAP:
            print(f"❌错误：{SELECT_KEY} 不在按键列表中！")
            logger.error(f"❌错误：{SELECT_KEY} 不在按键列表中！")
            sys.exit(1)
        target_vk = KEY_MAP[SELECT_KEY]

        ditto_pid = start_ditto_if_not_exist()

        # 切到桌面，防止按键输入编辑器
        desktop_hwnd = win32gui.GetDesktopWindow()
        win32gui.SetForegroundWindow(desktop_hwnd)
        time.sleep(0.3)

        # 发送虚拟键呼出Ditto悬浮窗(QPasteClass)
        send_virtual_key(target_vk)

        if AUTO_CLICK_THREE_DOTS:
            ditto_win = click_ditto_option_menu(ditto_pid)
            if ditto_win is not None:
                step4_delete_unused_clip_items(ditto_win)
                logger.info("脚本全部流程执行成功")
                print("✅全部流程执行成功")

    except KeyboardInterrupt:
        print("\n⚠️Ctrl+C中断脚本")
        logger.warning("用户按下Ctrl+C中断")
        sys.exit(1)
    except Exception as exc:
        err_msg = f"❌脚本运行未捕获异常：{str(exc)}"
        print(err_msg)
        logger.error(err_msg)
        sys.exit(1)

    logger.info("============脚本执行完毕============")


if __name__ == "__main__":
    main()
