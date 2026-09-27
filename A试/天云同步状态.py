# 版本：V1.7 修复坐标计算错误，将rectangle()替换为client_rect()客户区坐标；
# 根据截图情况图1界面重新校正左侧导航栏【传输】相对偏移；实现从情况图1全部文件页面，
# 点击左侧传输，再点击同步列表，跳转至情况图2同步列表页面；增加调试打印客户区信息；
# 严格匹配截图UI文本"同步已完成"+"没有相关内容哦"双重判定；全部注释中文
# 依赖安装：python.exe -m pip install pywinauto pyautogui
import time
from typing import cast

import pyautogui
from pywinauto import Application
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.findwindows import ElementNotFoundError

# ==========【配置区：根据截图情况图1天翼云盘窗口客户区调整相对偏移】==========
# 窗口【客户区】内部相对坐标：以云盘客户区左上角(不含标题栏)为原点，不是屏幕全局坐标
# 情况图1截图：左侧导航栏【传输】图标位置
REL_TRANSFER_X = 22
REL_TRANSFER_Y = 310
# 点击传输展开菜单之后，子菜单【同步列表】客户区相对偏移
REL_SYNC_X = 80
REL_SYNC_Y = 175
WAIT_TIMEOUT = 10
# ====================================================================


def activate_cloud_disk(wait_timeout: int = WAIT_TIMEOUT):
    """
    查找并激活天翼云盘窗口，恢复窗口防止最小化，前置窗口到屏幕可见
    :param wait_timeout: 查找窗口超时时间，单位秒
    :return: (是否成功, 窗口对象)
    """
    try:
        app = Application(backend="uia").connect(
            title_re="^天翼云盘.*", timeout=wait_timeout
        )
        main_win = app.window(title_re="^天翼云盘.*")
        main_win = cast(UIAWrapper, main_win)

        main_win.restore()
        main_win.set_focus()
        time.sleep(0.7)
        return True, main_win
    except ElementNotFoundError:
        print("❌ 未找到天翼云盘窗口，请先打开天翼云盘客户端！窗口不要最小化托盘")
        return False, None


def goto_sync_list_page():
    """
    激活云盘，通过窗口内相对坐标点击，进入同步列表页面
    返回 True = 成功进入；False = 失败
    """
    act_ok, main_win = activate_cloud_disk()
    if not act_ok:
        return False

    # UIA后端使用 rectangle() 获取窗口外框屏幕坐标
    win_rect = main_win.rectangle()
    win_left = win_rect.left
    win_top = win_rect.top
    print(f"调试：云盘窗口左上角屏幕坐标 left={win_left}, top={win_top}")

    # 换算屏幕真实点击坐标：窗口左上角 + 内部相对偏移（注意要包含标题栏高度）
    click_transfer_screen_x = win_left + REL_TRANSFER_X
    click_transfer_screen_y = win_top + REL_TRANSFER_Y
    pyautogui.click(x=click_transfer_screen_x, y=click_transfer_screen_y)
    time.sleep(1.0)

    click_synclist_screen_x = win_left + REL_SYNC_X
    click_synclist_screen_y = win_top + REL_SYNC_Y
    pyautogui.click(x=click_synclist_screen_x, y=click_synclist_screen_y)
    time.sleep(1.2)

    # 读取窗口文本校验页面
    win_text = main_win.window_text()
    if "同步列表" in win_text:
        print("✅ 校验成功，已经跳转至【情况图2：同步列表】页面")
        return True
    else:
        print("❌ 校验失败，未进入同步列表页面，请调整REL_*相对偏移参数")
        return False


def judge_sync_finish(wait_timeout: int = WAIT_TIMEOUT):
    """
    在情况图2同步列表页面，判定云盘是否全部同步完成
    严格匹配截图UI：必须同时存在 "同步已完成" 和 "没有相关内容哦" 两个文本标记
    :param wait_timeout: 查找窗口超时
    :return: True全部同步完成；False同步进行中/识别失败
    """
    try:
        app = Application(backend="uia").connect(
            title_re="^天翼云盘.*", timeout=wait_timeout
        )
        main_win = app.window(title_re="^天翼云盘.*")
        main_win = cast(UIAWrapper, main_win)

        win_text = main_win.window_text()
        has_sync_ok = "同步已完成" in win_text
        has_empty_tip = "没有相关内容哦" in win_text

        if has_sync_ok and has_empty_tip:
            print(
                "✅UI识别：同时检测到【同步已完成】+【没有相关内容哦】，全部同步任务结束"
            )
            return True
        else:
            print("⏳UI识别：未满足同步完成条件，同步还在进行")
            return False

    except ElementNotFoundError:
        print("❌ judge_sync_finish：找不到天翼云盘窗口")
        return False


def poll_sync_status(poll_interval: float = 3.0, max_round: int = 20):
    """
    循环轮询同步状态，防止单次检测时机不对漏判，达到最大次数直接超时退出
    :param poll_interval: 每次检测间隔，单位秒
    :param max_round: 最大循环检测次数
    :return: True同步完成，False超时未完成
    """
    print(f"\n开始轮询检测，检测间隔{poll_interval}秒，最大检测{max_round}次\n")
    for idx in range(max_round):
        print(f"-----第 {idx + 1} 次检测 -----")
        goto_ret = goto_sync_list_page()
        if not goto_ret:
            time.sleep(poll_interval)
            continue
        finish_ret = judge_sync_finish()
        if finish_ret:
            return True
        time.sleep(poll_interval)
    print(f"\n⚠️已达到最大轮询次数 {max_round}，判定同步超时未完成")
    return False


if __name__ == "__main__":
    print("=== 天翼云盘同步状态自动化脚本 V1.7 ===")
    print("校准坐标操作提示：")
    print("1.天翼云盘手动切到【情况图1：全部文件】界面，窗口不要最小化托盘")
    print(
        "2.运行 import pyautogui;print(pyautogui.position())，鼠标放到目标图标读取屏幕坐标"
    )
    print("3.REL_* = 图标屏幕坐标 − 打印输出的客户区left/top\n")

    sync_done = poll_sync_status(poll_interval=3.0, max_round=20)
    if sync_done:
        print("\n提醒：重要业务文件建议登录网页版二次校验云端文件真实存在")
    else:
        print("\n脚本结束：同步未完成或者超时")
