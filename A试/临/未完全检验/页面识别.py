# 版本：V1.2 修复文档场景下识别失败问题；根据docx情况图截图，
# 当同步列表存在历史同步条目时，不会出现"没有相关内容哦"，仅识别"同步已完成"作为判定条件；
# 使用descendants()获取全部后代控件，读取顶部绿色标签；仅文本采集调试，无页面跳转；全部注释中文
# 依赖安装：python.exe -m pip install pywinauto
import time
from typing import Optional, cast
from pywinauto import Application
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.findwindows import ElementNotFoundError

WAIT_TIMEOUT = 12


def get_cloud_disk_window() -> Optional[UIAWrapper]:
    """
    获取天翼云盘主窗口，恢复并激活窗口，窗口不可最小化至托盘
    :return: UIA窗口对象，失败返回None
    """
    try:
        app = Application(backend="uia").connect(
            title_re="^天翼云盘.*", timeout=WAIT_TIMEOUT)
        main_win = app.window(title_re="^天翼云盘.*")
        main_win = cast(UIAWrapper, main_win)
        main_win.restore()
        main_win.set_focus()
        time.sleep(0.5)
        return main_win
    except ElementNotFoundError:
        print("❌未找到天翼云盘窗口，请打开客户端，窗口不要最小化托盘！")
        return None


def get_all_descendant_text(root: UIAWrapper) -> str:
    """
    UIA获取全部后代控件文本，使用descendants穿透容器；
    解决children()只能获取直接子节点，拿不到顶部提示标签的问题
    :param root: 遍历根控件
    :return: 拼接后的全部UI文本字符串
    """
    result_text = ""
    try:
        all_ctrls = root.descendants()
        for ctrl in all_ctrls:
            wrap = cast(UIAWrapper, ctrl)
            txt = wrap.window_text()
            result_text += txt
    except Exception:
        pass
    return result_text


def check_sync_key_text() -> tuple[bool, bool, str]:
    """
    读取当前天翼云盘界面UIA全部文本
    文档情况图：同步列表存在历史任务条目，只需要识别"同步已完成"；
    "没有相关内容哦"仅列表完全空白时才会出现
    :return: (has_sync_complete, has_empty_tip, full_text)
             has_sync_complete：是否识别"同步已完成"顶部标签
             has_empty_tip：是否识别"没有相关内容哦"空列表提示
             full_text：采集到的完整UI文本片段
    """
    main_win = get_cloud_disk_window()
    if main_win is None:
        return False, False, ""

    full_text = get_all_descendant_text(main_win)
    has_sync_complete = "同步已完成" in full_text
    has_empty_tip = "没有相关内容哦" in full_text

    return has_sync_complete, has_empty_tip, full_text


if __name__ == "__main__":
    print("====天翼云盘 UIA文本识别独立脚本 V1.2====")
    print("【使用说明】")
    print("1.手动打开天翼云盘，手动切换到【同步列表】页面（docx情况图界面）")
    print("2.窗口不能最小化托盘，可以缩小窗口")
    print("3.本脚本只做UI文本采集，不做任何自动点击跳转\n")

    sync_ok, empty_tip, ui_all_text = check_sync_key_text()

    print(f"✅是否检测到【同步已完成】：{sync_ok}")
    print(f"✅是否检测到【没有相关内容哦】：{empty_tip}")
    print("\n----------采集到的UI文本片段(截取前1000字符)----------")
    print(ui_all_text[:1000])
    print("\n---------------------------------------------------")

    # =====按照文档docx真实界面修改判定逻辑=====
    # 场景A：列表内存在同步历史记录(截图情况图)：只要识别"同步已完成"即判定完成
    # 场景B：列表完全空白无任何任务：同时识别"同步已完成"+"没有相关内容哦"
    if sync_ok:
        if empty_tip:
            print("\n>>>判定：UI命中【同步已完成】+空列表提示，全部同步任务结束(列表空白)")
        else:
            print("\n>>>判定：UI命中【同步已完成】，当前列表存在历史同步记录，同步任务全部完成")
    else:
        print("\n>>>判定：未识别【同步已完成】标记，同步未完成或不在同步列表页面")
