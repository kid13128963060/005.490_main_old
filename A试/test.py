# v1.0
import win32com.client
import win32gui
import win32con
import win32api
import win32process
import psutil
import time
import pythoncom
import subprocess

SHUTDOWN_DELAY = 10


def close_all_word_documents():
    pythoncom.CoInitialize()
    word_com_ok = False
    try:
        word = win32com.client.GetActiveObject("Word.Application")
        doc_list = []
        for i in range(word.Documents.Count):
            doc = word.Documents(i + 1)
            doc_list.append(doc)
        print(f"【COM捕获】一共 {len(doc_list)} 个Word文档")
        # 先全部保存
        for doc in doc_list:
            try:
                doc.Save()
                print(f"✅ COM已保存: {doc.Name}")
            except Exception as e:
                print(f"⚠️ COM保存失败 {doc.Name}: {repr(e)}")
        # COM尝试关闭
        for doc in reversed(doc_list):
            try:
                doc.Close(SaveChanges=0)
                print(f"✅ COM关闭文档: {doc.Name}")
            except Exception as e:
                print(f"⚠️ COM关闭文档失败（COM断连是Word通病）: {repr(e)}")
        word_com_ok = True
    except OSError:
        print("【COM】没有检测到Word程序")
    except Exception as e:
        print(f"【COM】异常：{repr(e)}")
    finally:
        pythoncom.CoUninitialize()

    # ========== 兜底方案：枚举Word窗口，强制WM_CLOSE，把剩下残留标签页全部关掉 ==========
    print("\n===== 启动窗口兜底关闭Word =====")
    word_hwnds = []

    def enum_windows_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            cls = win32gui.GetClassName(hwnd)
            # Word主窗口类名：OpusApp
            if cls == "OpusApp":
                word_hwnds.append(hwnd)
        return True

    win32gui.EnumWindows(enum_windows_callback, None)
    print(f"【窗口兜底】找到 {len(word_hwnds)} 个Word主窗口(OpusApp)")

    for hwnd in word_hwnds:
        title = win32gui.GetWindowText(hwnd)
        print(f"发送关闭消息给Word窗口：{title}  hwnd={hwnd}")
        # 发送关闭消息，Word自己弹出保存提示（已经COM保存过，点保存不会重复）
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        time.sleep(0.8)


def send_ctrl_s(hwnd):
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.keybd_event(ord("S"), 0, 0, 0)
    time.sleep(0.15)
    win32api.keybd_event(ord("S"), 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.6)


def is_real_notepad_main_window(hwnd):
    if not win32gui.IsWindowVisible(hwnd):
        return False
    class_name = win32gui.GetClassName(hwnd)
    if class_name != "Notepad":
        return False
    title = win32gui.GetWindowText(hwnd)
    fake_keywords = [
        "Visual Studio Code",
        "VSCode",
        "vscode",
        "PowerShell",
        "Windows PowerShell",
        "cmd.exe",
        "命令行",
        "终端",
        "输出",
        "调试控制台",
        "导航",
        "搜索",
        "Word",
        "Excel",
        "Outlook",
    ]
    for kw in fake_keywords:
        if kw in title:
            return False
    if not title:
        return False
    return True


def force_save_and_close_notepad():
    NOTEPAD_CLASS = "Notepad"
    txt_hwnds = []

    def enum_callback(hwnd, extra):
        if win32gui.GetClassName(hwnd) == NOTEPAD_CLASS:
            txt_hwnds.append(hwnd)
        return True

    win32gui.EnumWindows(enum_callback, None)
    print(f"\n枚举到 {len(txt_hwnds)} 个 Notepad 类窗口")
    real_main_hwnds = [hwnd for hwnd in txt_hwnds if is_real_notepad_main_window(hwnd)]
    print(f"识别为真正记事本主窗口 {len(real_main_hwnds)} 个")

    for hwnd in real_main_hwnds:
        if not win32gui.IsWindow(hwnd):
            continue
        title = win32gui.GetWindowText(hwnd)
        print(f"处理记事本主窗口: {title} (句柄: {hwnd})")
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                pass
            time.sleep(0.4)
            send_ctrl_s(hwnd)
            edit_hwnd = win32gui.FindWindowEx(hwnd, None, "Edit", None)
            if edit_hwnd:
                win32gui.SendMessage(edit_hwnd, win32con.EM_EMPTYUNDOBUFFER, 0, 0)
            win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            time.sleep(0.7)
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
    print("记事本处理完成")


def cancel_shutdown():
    try:
        result = subprocess.run(["shutdown", "/a"], capture_output=True, text=True)
        if result.returncode == 0:
            print("\n✅ 关机已成功中止")
        else:
            print(f"\n⚠️ 中止关机失败：{result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"\n⚠️ 中止关机发生异常：{repr(e)}")
        return False


def start_shutdown(countdown_sec: int):
    try:
        print(f"\n将在{countdown_sec}秒后关机...")
        subprocess.run(["shutdown", "/s", "/t", str(countdown_sec)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n⚠️ 关机命令执行失败: {str(e)}")
        return False


if __name__ == "__main__":
    close_all_word_documents()
    force_save_and_close_notepad()
    # start_shutdown(SHUTDOWN_DELAY)
