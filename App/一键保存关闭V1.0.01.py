from multiprocessing.resource_sharer import stop

import win32com.client
import win32gui
import win32con
import win32api
import win32process
import psutil
import time
import pythoncom
import subprocess
import threading


def save_vscode_all_files():
    """查找所有VSCode窗口，发送 Ctrl+K S 保存全部修改文件"""
    VSCODE_TITLE_KEYWORD = "Visual Studio Code"
    vscode_hwnds = []

    def enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            win_title = win32gui.GetWindowText(hwnd)
            if VSCODE_TITLE_KEYWORD in win_title:
                extra.append(hwnd)
        return True

    win32gui.EnumWindows(enum_callback, vscode_hwnds)
    print(f"找到 {len(vscode_hwnds)} 个VSCode窗口")

    for hwnd in vscode_hwnds:
        if not win32gui.IsWindow(hwnd):
            continue
        title = win32gui.GetWindowText(hwnd)
        print(f"处理VSCode窗口：{title} 句柄={hwnd}")
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                print("  无法前置窗口，继续发送快捷键")
            time.sleep(0.4)

            # Ctrl+K 然后 S 保存全部
            win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            time.sleep(0.1)
            win32api.keybd_event(ord('K'), 0, 0, 0)
            time.sleep(0.15)
            win32api.keybd_event(ord('K'), 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.1)
            win32api.keybd_event(ord('S'), 0, 0, 0)
            time.sleep(0.15)
            win32api.keybd_event(ord('S'), 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(win32con.VK_CONTROL, 0,
                                 win32con.KEYEVENTF_KEYUP, 0)

            time.sleep(0.6)
            print(f"✅ {title} 已执行保存全部")
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
    print("VSCode保存处理完成")


if __name__ == "__main__":
    save_vscode_all_files()

# 配置常量：关机倒计时秒数
SHUTDOWN_DELAY = 60


def close_all_word_documents():
    """保存并关闭所有打开的Word文档，兼容Word未启动场景"""
    pythoncom.CoInitialize()
    try:
        # 捕获Word没有运行的异常
        try:
            word = win32com.client.GetActiveObject("Word.Application")
        except OSError:
            print("没有检测到正在运行的Word程序")
            return

        doc_count = word.Documents.Count
        if doc_count <= 0:
            print("没有打开的Word文档")
            return

        print(f"发现 {doc_count} 个打开的Word文档，正在关闭并保存...")
        # 复制文档列表，避免循环过程集合变化
        docs = [doc for doc in word.Documents]
        for doc in docs:
            try:
                doc.Save()
                print(f"已保存: {doc.Name}")
            except Exception as e:
                print(f"保存文档 {doc.Name} 时出错: {repr(e)}")
            try:
                doc.Close()
                print(f"已关闭: {doc.Name}")
            except Exception as e:
                print(f"关闭文档 {doc.Name} 时出错: {repr(e)}")

    except Exception as e:
        print(f"Word操作出错: {repr(e)}")
    finally:
        pythoncom.CoUninitialize()


def send_ctrl_s(hwnd):
    """安全发送 Ctrl+S，修复按键抬起顺序错误"""
    # 按下Ctrl
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    # 按下S
    win32api.keybd_event(ord('S'), 0, 0, 0)
    time.sleep(0.15)
    # 先释放S，再释放Ctrl（原代码顺序颠倒！）
    win32api.keybd_event(ord('S'), 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.6)


def force_save_and_close_notepad():
    """修复记事本：移除EM_SETMODIFY致命bug，优化窗口激活容错"""
    NOTEPAD_CLASS = "Notepad"
    txt_hwnds = []

    def enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetClassName(hwnd) == NOTEPAD_CLASS:
            txt_hwnds.append(hwnd)
        return True

    win32gui.EnumWindows(enum_callback, None)
    print(f"找到 {len(txt_hwnds)} 个记事本窗口（可见状态）")

    for hwnd in txt_hwnds:
        if not win32gui.IsWindow(hwnd):
            continue
        title = win32gui.GetWindowText(hwnd)
        print(f"处理窗口: {title} (句柄: {hwnd})")
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                # 后台权限不足无法置前台，静默跳过
                pass
            time.sleep(0.4)

            send_ctrl_s(hwnd)

            edit_hwnd = win32gui.FindWindowEx(hwnd, None, "Edit", None)
            if edit_hwnd:
                win32gui.SendMessage(
                    edit_hwnd, win32con.EM_EMPTYUNDOBUFFER, 0, 0)

            # 发送关闭消息
            win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            time.sleep(0.7)

            # 判断窗口是否还存在
            if win32gui.IsWindow(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    p = psutil.Process(pid)
                    p.terminate()
                    print(f"记事本窗口未响应，已强制终止进程 {pid}")
                except psutil.NoSuchProcess:
                    print(f"进程 {pid} 已经退出")
            else:
                print(f"记事本窗口 {title} 已正常关闭")

            time.sleep(0.2)
        except Exception as e:
            print(f"处理记事本出错: {str(e)}")

    print(f"已处理 {len(txt_hwnds)} 个记事本窗口")


def cancel_shutdown():
    """中止系统关机（调用 shutdown /a）"""
    try:
        result = subprocess.run(
            ["shutdown", "/a"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ 关机已成功中止")
        else:
            print(f"⚠️ 中止关机失败：{result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"中止关机发生异常：{repr(e)}")
        return False


def start_shutdown(countdown_sec: int):
    """发起定时关机
    :param countdown_sec: 关机倒计时秒数
    """
    try:
        print(f"将在{countdown_sec}秒后关机...")
        print("程序内可调用 cancel_shutdown() 取消关机；命令行可执行 shutdown /a")
        subprocess.run(
            ["shutdown", "/s", "/t", str(countdown_sec)],
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"关机命令执行失败: {str(e)}")
        return False


if __name__ == "__main__":
    save_vscode_all_files()
    close_all_word_documents()
    force_save_and_close_notepad()

    start_shutdown(SHUTDOWN_DELAY)

    # ============ 示例：测试中止功能，需要启用就把下面注释去掉 ==========
    # print("等待3秒后演示中止关机……")
    # time.sleep(9)
    # cancel_shutdown()
