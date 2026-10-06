# version:V1.0.0 | 2026‑10‑06 | 初始版本，实现成功失败弹窗UI
# version:V1.0.1 | 2026‑10‑06 | 修复tk、messagebox未导入报错，移除logging日志模块
# version:V1.0.2 | 2026‑10‑06 | 新增Ctrl+C捕获，增加LookupError、超时异常捕获，完善类型注解
"""
设备识别工作流弹窗提示脚本
环境：Python3.13 Windows10专业版 22H2
"""

import tkinter as tk
from tkinter import messagebox
import sys
from typing import NoReturn


def show_success_ui() -> None:
    """脚本全部流程正常执行完成，弹出成功提示UI"""
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(
        title="工作流执行完成",
        message="✅ 设备识别工作流全部脚本执行成功！\n"
        "流程：设备识别→网络检测→Wifi控制→天翼云盘→ps1配置脚本全部走完。",
    )
    root.destroy()


def show_fail_ui(error_msg: str) -> None:
    """
    发生异常/失败，弹出失败提示UI，显示错误详情
    :param error_msg: 需要展示的错误文本
    """
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title="工作流执行失败", message=f"❌ 设备识别工作流执行异常！\n错误信息：\n{error_msg}")
    root.destroy()


def exit_script(print_msg: str) -> NoReturn:
    """
    控制台打印错误信息，退出脚本
    :param print_msg: 控制台输出的错误内容
    """
    print(f"\n[ERROR] {print_msg}")
    sys.exit(1)


if __name__ == "__main__":
    try:
        show_success_ui()
    except KeyboardInterrupt:
        err_text = "用户按下Ctrl+C手动终止脚本"
        print(f"\n!!!捕获到异常：{err_text}")
        show_fail_ui(err_text)
    except LookupError as e:
        err_text = f"找不到控件(LookupError): {str(e)}"
        print(f"\n!!!捕获到异常：{err_text}")
        show_fail_ui(err_text)
        exit_script(err_text)
    except TimeoutError as e:
        err_text = f"控件操作超时异常(TimeoutError): {str(e)}"
        print(f"\n!!!捕获到异常：{err_text}")
        show_fail_ui(err_text)
        exit_script(err_text)
    except Exception as e:
        err_text = str(e)
        print(f"\n!!!捕获到异常：{err_text}")
        show_fail_ui(err_text)

    print("脚本执行完毕")
