import os
import argparse
import win32con
import ctypes
from ctypes import wintypes
import pythoncom
from win32com.client import Dispatch
import win32gui
import win32process
from datetime import datetime


def get_last_active_explorer_path(path=None):
    """获取资源管理器最后活动的后台窗口路径"""
    try:
        pythoncom.CoInitialize()
        shell_windows = Dispatch("Shell.Application").Windows()
        explorer_windows = []
        for window in shell_windows:
            if window and window.LocationURL and window.LocationURL.startswith("file:///"):
                hwnd = window.HWND
                title = win32gui.GetWindowText(hwnd)
                path = window.LocationURL[8:].replace("/", "\\")
                explorer_windows.append((hwnd, title, path))
        if not explorer_windows:
            print("未找到资源管理器窗口")
            return path if path is not None else None
        user32 = ctypes.windll.user32
        active_hwnd = user32.GetForegroundWindow()
        non_active_explorers = [
            win for win in explorer_windows if win[0] != active_hwnd]
        if not non_active_explorers:
            print("使用当前活动窗口路径")
            path = explorer_windows[0][2]
        else:
            def get_window_z_order(hwnd):
                z_order = 0
                current = hwnd
                while True:
                    current = win32gui.GetWindow(current, win32con.GW_HWNDPREV)
                    if not current:
                        break
                    z_order += 1
                return z_order
            non_active_explorers.sort(key=lambda x: get_window_z_order(x[0]))
            path = non_active_explorers[0][2]
        print(f"资源管理器最后活动窗口路径: {path}")
        return path
    except Exception as e:
        print(f"获取路径时出错: {e}")
        return path if path is not None else None
    finally:
        pythoncom.CoUninitialize()


def generate_filename(prefix="", lang="", version="", year="", month="", day="", source_name=None, is_folder=False):
    """生成标准化文件名（修复version自动加点逻辑，区分文件/文件夹）"""
    # 从源文件提取语言标识（优先于参数）
    if source_name and not lang:
        base_name = os.path.basename(source_name)
        if 'py' in base_name or 'python' in base_name.lower():
            lang = 'py'
        elif 'ps' in base_name or 'powershell' in base_name.lower():
            lang = 'ps'
        else:
            lang = ''

    # 提取前缀（优先使用参数，其次从源文件名提取）
    if source_name:
        parts = base_name.split('_')
        prefix = prefix or (parts[0] if parts else "")
        prefix = prefix.replace('-', '_')
        prefix = '_'.join(filter(None, prefix.split()))

    # 提取版本号（仅对文件有效）
    if not is_folder and source_name and not version:
        parts = base_name.split('_')
        for part in parts:
            if 'v' in part and '.' in part:
                version = part[1:]
            elif '.' in part and all(p.isdigit() for p in part.split('.')):
                version = part

    # 提取日期（仅对文件有效）
    if not is_folder and source_name and not (year and month and day):
        parts = base_name.split('_')
        for part in parts:
            if len(part) == 8 and part.isdigit():
                year, month, day = part[:4], part[4:6], part[6:8]
                break

    # 日期处理（仅对文件有效）
    date_part = ""
    if not is_folder:
        date_part = f"{year}{month.zfill(2)}{day.zfill(2)}" if all(
            [year, month, day]) else datetime.now().strftime("%Y%m%d")

    # 版本号处理（核心修复：恢复自动加点功能）
    version_formatted = ""
    if not is_folder and version is not None:
        version = version or "1.0"  # 默认为1.0
        # 自动加点逻辑：无点时补全（如"1"→"1.0"，"12"→"1.2"）
        if '.' not in version:
            if len(version) == 1:
                version_formatted = f"{version}.0"
            else:
                major = version[0]
                minor = version[1:]
                version_formatted = f"{major}.{minor}"
        else:
            version_formatted = version
        # 统一加v前缀（如"1.0"→"v1.0"）
        if version_formatted:
            version_clean = version_formatted.lstrip('vV')
            version_formatted = f"v{version_clean}"

    # 核心逻辑：组合组件（文件夹不含版本/日期）
    components = [prefix, lang]
    if not is_folder and lang in ['py', 'ps']:  # 仅脚本文件保留版本和日期
        components.extend([version_formatted, date_part])
    # 过滤空组件
    components = [c for c in components if c]
    return "_".join(components)


def rename_entity(old_folder, new_name, source_name, overwrite=False):
    """重命名文件或文件夹"""
    old_folder = os.path.abspath(old_folder)
    source_path = os.path.join(old_folder, source_name)
    if not os.path.exists(source_path):
        source_candidates = [f for f in os.listdir(
            old_folder) if source_name.lower() in f.lower()]
        if source_candidates:
            source_path = os.path.join(old_folder, source_candidates[0])
            print(f"提示: 自动匹配源文件/文件夹: {source_candidates[0]}")
        else:
            return False, f"错误: 源文件/文件夹不存在 ({source_path})\n当前文件夹内容: {', '.join(os.listdir(old_folder))}"
    new_path = os.path.join(old_folder, new_name)

    if os.path.exists(new_path):
        if overwrite:
            try:
                if os.path.isfile(new_path):
                    os.remove(new_path)
                    print(f"已删除冲突文件: {new_path}")
                else:
                    import shutil
                    shutil.rmtree(new_path)
                    print(f"已删除冲突文件夹: {new_path}")
            except Exception as e:
                return False, f"删除冲突文件/文件夹失败: {str(e)}"
        else:
            return False, f"错误: 目标文件/文件夹已存在 ({new_path})，请使用 --overwrite 参数覆盖"

    try:
        os.rename(source_path, new_path)
        return True, f"成功重命名: {source_path} -> {new_path}"
    except Exception as e:
        return False, f"重命名失败: {str(e)}"


def create_new_entity(folder_path, entity_name):
    """创建新文件或文件夹"""
    entity_path = os.path.join(folder_path, entity_name)
    try:
        if '.' in entity_name:  # 含扩展名则为文件
            with open(entity_path, 'w') as f:
                pass
            return True, f"成功创建新文件: {entity_path}"
        else:  # 无扩展名则为文件夹
            os.makedirs(entity_path)
            return True, f"成功创建新文件夹: {entity_path}"
    except Exception as e:
        return False, f"创建新文件/文件夹失败: {str(e)}"


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='文件和文件夹重命名与创建工具')
    parser.add_argument('--old_folder', help='文件夹路径', default=None)
    parser.add_argument('--prefix', help='文件名/文件夹名前缀', default='')
    parser.add_argument('--lang', help='语言标识（如py/ps）', default='')
    parser.add_argument('-e', '--ext', help='文件扩展名（如--ext .ps1）', default=None)
    parser.add_argument('--version', help='版本号（如1→1.0，12→1.2）', default='')
    parser.add_argument('--year', help='年份', default='')
    parser.add_argument('--month', help='月份', default='')
    parser.add_argument('--day', help='日期', default='')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在文件/文件夹')
    parser.add_argument('--source', help='源文件名/文件夹名（重命名时必选）', required=False)
    parser.add_argument('--new_entity_name',
                        help='手动指定新文件名/文件夹名', default=None)
    parser.add_argument('--create', action='store_true', help='执行创建新文件/文件夹操作')
    args = parser.parse_args()  # 显式解析参数，让Pylance识别

    # 处理文件夹路径（优先使用资源管理器活动窗口路径）
    if args.old_folder:
        args.old_folder = os.path.abspath(args.old_folder)
        if not os.path.exists(args.old_folder):
            print(f"警告: 文件夹不存在，尝试获取资源管理器路径: {args.old_folder}")
            args.old_folder = get_last_active_explorer_path(args.old_folder)
    else:
        args.old_folder = get_last_active_explorer_path()

    if not args.old_folder or not os.path.exists(args.old_folder):
        print("\n错误: 无法找到有效文件夹！")
        exit(1)

    # 区分创建和重命名操作
    if args.create:
        # 处理扩展名（优先用户指定，其次按语言标识）
        if not args.ext:
            if args.lang.lower() == 'ps':
                args.ext = '.ps1'  # 修复PowerShell标准扩展名
            else:
                args.ext = '.py'  # 默认Python扩展名

        if args.new_entity_name:
            # 手动指定名称：替换横线为下划线，补全扩展名
            full_name = args.new_entity_name.replace('-', '_')
            is_folder = '.' not in full_name  # 无扩展名则为文件夹
            if not is_folder and not full_name.endswith(args.ext):
                full_name += args.ext
        else:
            # 自动生成名称：根据扩展名判断是否为文件
            has_ext = bool(args.ext and args.ext.strip())
            # 先生成临时文件名（按文件逻辑）
            temp_name = generate_filename(
                prefix=args.prefix,
                lang=args.lang,
                version=args.version,
                year=args.year,
                month=args.month,
                day=args.day,
                is_folder=False
            )
            # 判断是否为文件夹：指定扩展名则必为文件
            is_folder = not has_ext and ('.' not in temp_name)

            # 生成最终名称（补全扩展名或调整文件夹名称）
            full_name = temp_name
            if not is_folder:
                if not full_name.endswith(args.ext):
                    full_name += args.ext
            else:
                # 文件夹名称不含版本和日期
                full_name = generate_filename(
                    prefix=args.prefix,
                    lang=args.lang,
                    is_folder=True
                )

        success, msg = create_new_entity(args.old_folder, full_name)

    else:
        # 重命名操作（必选--source参数）
        if not args.source:
            parser.error("--source 参数在重命名时为必填项")
        source_name = args.source
        source_path = os.path.join(args.old_folder, source_name)

        if not os.path.exists(source_path):
            source_candidates = [f for f in os.listdir(
                args.old_folder) if source_name.lower() in f.lower()]
            if source_candidates:
                source_path = os.path.join(
                    args.old_folder, source_candidates[0])
                print(f"提示: 自动匹配源文件/文件夹: {source_candidates[0]}")
            else:
                parser.error(f"错误: 源文件/文件夹不存在 ({source_path})")

        # 确定源类型（文件/文件夹）
        is_file = os.path.isfile(source_path)
        is_folder = not is_file

        # 处理扩展名（优先源文件扩展名）
        if not args.ext and is_file:
            _, ext = os.path.splitext(source_path)
            args.ext = ext if ext else (
                '.ps1' if args.lang.lower() == 'ps' else '.py')

        if args.new_entity_name:
            full_name = args.new_entity_name.replace('-', '_')
            if is_file and not full_name.endswith(args.ext):
                full_name += args.ext
        else:
            # 自动生成重命名后的名称
            full_name = generate_filename(
                prefix=args.prefix,
                lang=args.lang,
                version=args.version,
                year=args.year,
                month=args.month,
                day=args.day,
                source_name=source_name,
                is_folder=is_folder
            )
            if is_file and not full_name.endswith(args.ext):
                full_name += args.ext

        success, msg = rename_entity(
            args.old_folder, full_name, source_name, args.overwrite)

    # 输出调试与结果信息
    print(f"\n[调试信息]")
    print(f"扩展名: {args.ext}")
    print(f"生成的名称: {full_name}")
    print(f"源路径: {source_path if 'source_path' in locals() else 'N/A'}")
    print(f"是否为文件: {not is_folder if 'is_folder' in locals() else 'N/A'}")
    print(f"覆盖参数: {args.overwrite}")

    print(f"\n执行详情:")
    print(msg)
    print(f"目标路径: {os.path.join(args.old_folder, full_name)}")

    exit(0 if success else 1)
