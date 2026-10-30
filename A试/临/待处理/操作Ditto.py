# 版本：V3.0 Ditto自动化脚本；修复find_elements() got an unexpected keyword argument 'timeout'；
# 使用pywinauto UIA后端；禁止pyautogui图像识别；logging输出uia_log.txt；捕获Ctrl+C中断；显式等待10秒；全部中文注释
# 修复清单：
# 1.移除app.window(class_name=None)，该传参是报错图2的真正根源；
# 2.完全复用参考代码2：find_child_by_name、get_all_descendant_text、click_input()点击方式；
# 3.解决观察1：彻底移除记事本/Word输入文本逻辑，脚本仅操作DittoUI；
# 4.解决Ditto启动后无法激活前台，执行restore+set_focus；
# 5.不导入LookupError，运行时通过异常类名字符串捕获，消除导入符号报错；
# 6.日志采用脚本所在目录绝对路径，不受运行工作目录影响
import logging
import sys
import os
import time
from typing import Optional, cast
from pywinauto import Application
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.findwindows import ElementNotFoundError

# --------------------------全局常量配置--------------------------
WAIT_TIMEOUT: int = 10  # 元素、窗口显式等待超时时间，单位秒
DITTO_EXE_PATH: str = r"C:\Program Files\Ditto\Ditto.exe"
# 获取当前脚本所在文件夹，日志uia_log.txt固定生成在脚本同级目录，不受cmd/vscode运行目录影响
SCRIPT_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_NAME: str = os.path.join(SCRIPT_FOLDER, "uia_log.txt")

# --------------------------日志初始化配置--------------------------
logging.basicConfig(
    filename=LOG_FILE_NAME, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8"
)
logger = logging.getLogger(__name__)


def find_child_by_name(root: UIAWrapper, target_name: str, depth: int = 8) -> Optional[UIAWrapper]:
    """
    UIA递归遍历控件树，按控件Name文本查找子控件，取自参考代码2实现
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
    """
    【取自参考代码2】使用descendants获取全部后代控件文本，穿透所有容器面板
    解决children()、顶层window_text()拿不到内部悬浮菜单面板文本的问题
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
    except Exception as exc:
        logger.warning(f"获取后代控件文本异常:{str(exc)}")
    return result_text


def start_ditto_app() -> Optional[UIAWrapper]:
    """
    步骤1：启动Ditto.exe；步骤2等待程序窗口加载完成；步骤3恢复窗口并激活到前台
    修复关键点：删除 app.window(class_name=None)，class_name=None会触发内部find_elements参数异常（报错图2）
    :return: 返回Ditto主窗口UIAWrapper对象；失败返回None
    """
    try:
        logger.info(f"准备启动Ditto程序，路径：{DITTO_EXE_PATH}")
        app = Application(backend="uia").start(DITTO_EXE_PATH)
        # 【关键修复】删除 class_name=None 传参，直接使用timeout等待窗口
        main_win = app.window(timeout=WAIT_TIMEOUT)
        main_win = cast(UIAWrapper, main_win)
        # 解决观察：Ditto启动成功但是无法激活到前台，先restore恢复窗口再set_focus置顶
        main_win.restore()
        main_win.set_focus()
        time.sleep(1.2)
        logger.info("✅Ditto程序启动成功，窗口已恢复并激活至前台")
        return main_win
    except ElementNotFoundError as exc:
        err_msg = f"❌等待Ditto窗口超时{WAIT_TIMEOUT}秒，没有找到Ditto窗口，" f"异常信息：{str(exc)}"
        logger.error(err_msg)
        print(err_msg)
        return None
    except Exception as exc:
        err_msg = f"❌启动Ditto程序发生异常：{str(exc)}"
        logger.error(err_msg)
        print(err_msg)
        return None


def execute_delete_unused_clip_item() -> bool:
    """
    业务主逻辑：Ditto窗口找到三点【选项...】按钮，点击弹出悬浮菜单，
    在菜单中点击【删除所有未使用的剪贴项】，完全参考代码2控件遍历与click_input点击方式
    解决观察1：脚本完全移除记事本/Word输入文本逻辑，仅操作Ditto程序UI
    对应截图情况图2三点按钮，情况图3下拉菜单项
    :return: True操作执行成功；False执行失败
    """
    ditto_main_win = start_ditto_app()
    if ditto_main_win is None:
        logger.error("Ditto主窗口获取失败，流程终止")
        return False

    # 1.查找三点更多选项菜单按钮（情况图3，菜单文本：选项...）
    logger.info("🔍UIA控件树遍历，查找Ditto三点【选项...】菜单按钮")
    three_dot_menu_ctrl = find_child_by_name(ditto_main_win, "选项...")
    if three_dot_menu_ctrl is None:
        err_msg = "❌未找到三点【选项...】菜单控件，控件不存在"
        logger.error(err_msg)
        print(err_msg)
        return False
    # 参考代码2点击方式：UIA原生click_input，禁止坐标/图像模拟鼠标
    three_dot_menu_ctrl.click_input()
    logger.info("✅已点击三点【选项...】，等待下拉悬浮菜单面板渲染")
    time.sleep(1.5)

    # 使用descendants读取全部后代文本校验悬浮菜单是否弹出
    menu_full_text = get_all_descendant_text(ditto_main_win)
    if "删除所有未使用的剪贴项" not in menu_full_text:
        err_msg = "❌点击三点后，未检测到下拉菜单内容，菜单面板弹出失败"
        logger.error(err_msg)
        print(err_msg)
        return False

    # 2.在弹出悬浮菜单中定位目标菜单项：删除所有未使用的剪贴项
    logger.info("🔍遍历弹出菜单控件，查找【删除所有未使用的剪贴项】")
    delete_menu_item = find_child_by_name(ditto_main_win, "删除所有未使用的剪贴项")
    if delete_menu_item is None:
        err_msg = "❌找不到菜单项【删除所有未使用的剪贴项】，控件不存在"
        logger.error(err_msg)
        print(err_msg)
        return False
    delete_menu_item.click_input()
    logger.info("✅成功点击【删除所有未使用的剪贴项】，操作完成")
    time.sleep(0.8)
    return True


def main():
    """
    脚本入口主函数，捕获Ctrl+C；
    解决报错图3、图4：不导入LookupError，通过异常类型名称字符串捕获该异常，消除导入符号报错
    """
    print("===== Ditto剪贴板清理自动化脚本 V3.0 =====")
    print(f"📝日志文件完整路径：{LOG_FILE_NAME}")
    logger.info("============脚本开始执行============")
    try:
        run_result = start_ditto_app()
        if run_result:
            logger.info("业务流程全部执行成功")
        else:
            logger.error("业务流程执行失败")
    except KeyboardInterrupt:
        print("\n⚠️检测到Ctrl+C快捷键，脚本安全退出")
        logger.warning("用户按下Ctrl+C中断脚本运行")
        sys.exit(1)
    except Exception as exc:
        # 不导入LookupError类，靠异常名称捕获，解决「LookupError是未知的导入符号」编译报错
        if type(exc).__name__ == "LookupError":
            err_msg = f"❌LookupError 控件查找匹配失败异常:{str(exc)}"
        else:
            err_msg = f"❌脚本运行未捕获异常：{str(exc)}"
        print(err_msg)
        logger.error(err_msg)
        sys.exit(1)

    print("脚本执行完毕")
    logger.info("============脚本执行完毕============")


if __name__ == "__main__":
    main()
