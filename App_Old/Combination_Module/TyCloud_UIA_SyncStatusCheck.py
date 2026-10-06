# 版本：V3.3 整合docx文档要求；保留情况图1到情况图2完整UIA跳转逻辑；
# 使用代码2的descendants()获取全部后代控件文本替换原识别逻辑；修复原main_win.window_text()
# 无法读取子面板内容的报错图1问题；适配真实UI：列表有历史记录时仅识别"同步已完成"即可判定；
# 全部注释使用中文，长注释换行处理
# 依赖安装：python.exe -m pip install pywinauto
import time
from typing import Optional, cast

from pywinauto import Application
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.findwindows import ElementNotFoundError

WAIT_TIMEOUT = 80


def get_cloud_disk_window() -> Optional[UIAWrapper]:
    """
    获取天翼云盘主窗口对象，恢复窗口、前置激活，窗口不可最小化至托盘
    :return: 返回UIA窗口对象；查找失败返回None
    """
    try:
        app = Application(backend="uia").connect(title_re="^天翼云盘.*", timeout=WAIT_TIMEOUT)
        main_win = app.window(title_re="^天翼云盘.*")
        main_win = cast(UIAWrapper, main_win)
        main_win.restore()
        main_win.set_focus()
        time.sleep(0.05)
        return main_win
    except ElementNotFoundError:
        print("❌未找到天翼云盘窗口，请手动打开天翼云盘客户端，禁止最小化到系统托盘！")
        return None


def find_child_by_name(root: UIAWrapper, target_name: str, depth: int = 8) -> Optional[UIAWrapper]:
    """
    UIA递归遍历控件树，按控件Name文本查找子控件
    :param root: 根窗口控件对象
    :param target_name: 需要查找的控件显示文本
    :param depth: 递归遍历最大深度，防止无限遍历
    :return: 找到返回控件对象，找不到返回None
    """
    if depth <= 0:
        return None
    try:
        children = root.children()
        for child in children:
            child_wrap = cast(UIAWrapper, child)
            if child_wrap.window_text().strip() == target_name.strip():
                return child_wrap
            res = find_child_by_name(child_wrap, target_name, depth - 1)
            if res is not None:
                return res
    except Exception:
        pass
    return None


def get_all_descendant_text(root: UIAWrapper) -> str:
    """
    【取自代码2】使用descendants获取全部后代控件文本，穿透所有容器面板
    解决children()、顶层window_text()拿不到内部标签文本的报错图1问题
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


def goto_sync_list_page() -> bool:
    """
    页面跳转逻辑（纯UIA控件操作，无鼠标坐标）
    情况图1【全部文件】 →点击左侧导航【传输】 →等待右侧面板加载 →点击【同步列表】
    →到达情况图2【同步列表】页面
    :return: True成功进入同步列表页面；False跳转失败
    """
    main_win = get_cloud_disk_window()
    if main_win is None:
        return False

    # 1.递归UIA树查找左侧导航栏【传输】控件
    print("🔍UIA遍历控件树，查找左侧导航【传输】控件……")
    ctrl_transfer = find_child_by_name(main_win, "传输")
    if ctrl_transfer is None:
        print("❌UIA未找到【传输】导航控件！控件Name属性为空，无法通过文本匹配")
        return False
    # UIA调用控件原生click，不需要模拟屏幕鼠标
    ctrl_transfer.click_input()
    print("✅已点击【传输】导航项，等待右侧传输面板渲染加载")
    time.sleep(2.6)

    # 2.在右侧传输面板中查找【同步列表】控件
    print("🔍UIA遍历控件树，查找右侧面板【同步列表】控件……")
    ctrl_sync_list = find_child_by_name(main_win, "同步列表")
    if ctrl_sync_list is None:
        print("❌UIA未找到【同步列表】控件！")
        return False
    ctrl_sync_list.click_input()
    print("✅已点击【同步列表】控件，等待页面切换完成")
    time.sleep(1.8)

    # 3.【修复】使用代码2的descendants获取全部后代文本做页面进入校验
    full_ui_text = get_all_descendant_text(main_win)
    if "同步列表" in full_ui_text:
        print("✅校验通过，成功跳转【情况图2：同步列表】页面")
        return True
    else:
        print("❌校验失败，未成功进入同步列表页面")
        return False


def judge_sync_finish() -> bool:
    """
    【取自代码2识别逻辑】在情况图2同步列表页面判定同步任务全部完成
    适配真实截图UI：
        场景1：列表存在历史同步条目：识别"同步已完成"绿色标签即判定完成
        场景2：列表完全空白：同时识别"同步已完成"+"没有相关内容哦"判定完成
    :return: True全部同步完成；False同步进行中/识别异常
    """
    main_win = get_cloud_disk_window()
    if main_win is None:
        return False

    full_text = get_all_descendant_text(main_win)
    has_sync_complete = "同步已完成" in full_text
    has_empty_tip = "没有相关内容哦" in full_text

    if has_sync_complete:
        if has_empty_tip:
            print("✅UIA识别：同步已完成 + 没有相关内容哦；列表空白，全部同步任务结束")
        else:
            print("✅UIA识别：同步已完成；列表存在历史条目，全部同步任务结束")
        return True
    else:
        print("⏳UIA识别：尚未检测到【同步已完成】标记，同步还在执行")
        return False


def poll_sync_status(poll_interval: float = 3.0, max_round: int = 30) -> bool:
    """
    轮询检测同步状态，防止单次采样时机不对漏判；超过最大次数判定超时
    :param poll_interval: 两次检测间隔，单位秒
    :param max_round: 最大循环检测次数
    :return: True同步完成；False超时未完成
    """
    print(f"\n====开始轮询检测，间隔{poll_interval}秒，最大轮询{max_round}次====\n")
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
    print(f"\n⚠️达到最大轮询次数 {max_round}，判定同步超时未完成")
    return False


if __name__ == "__main__":
    print("====天翼云盘同步检测【整合文档要求 V3.3】====")
    print("说明：纯UIA无鼠标坐标；情况图1自动跳转至情况图2；使用descendants读取全部后代控件")
    print("前提条件：天翼云盘客户端已打开，窗口不能最小化托盘，可以缩小窗口\n")

    sync_done = poll_sync_status(poll_interval=3.0, max_round=20)
    if sync_done:
        print("\n提醒：重要业务文件建议登录网页版，二次校验云端文件真实存在")
    else:
        print("\n脚本结束：同步未完成或者超时")
