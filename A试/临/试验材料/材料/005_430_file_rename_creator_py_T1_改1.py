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
        non_active_explorers = [win for win in explorer_windows if win[0] != active_hwnd]
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
        date_part = f"{year}{month.zfill(2)}{day.zfill(2)}" if all([year, month, day]) else datetime.now().strftime("%Y%m%d")

    # 版本号处理（仅对文件有效）
    version_formatted = ""
    if not is_folder:
        version = version or "1.0"
        if '.' not in version:
            if len(version) == 1:
                version_formatted = f"{version}.0"
            else:
                major = version[0]
                minor = version[1:]
                version_formatted = f"{major}.{minor}"
        else:
            version_formatted = version
        # 统一处理成v1.0样式（若传入空则跳过版本）
        if version_formatted:
            version_clean = version_formatted.lstrip('vV')
            version_formatted = f"v{version_clean}"

    # 核心逻辑：区分【脚本文件】和【非脚本文件】
    components = [prefix, lang]  # 基础组件：前缀 + 语言标识（如old_bat + bat）

    if not is_folder:  # 非文件夹时才考虑版本/日期
        # 仅脚本类型文件（py/ps）保留版本和日期
        is_script = lang in ['py', 'ps']
        if is_script:
            # 脚本文件：拼接版本 + 日期（如v1.0 + 20250629）
            components.extend([version_formatted, date_part])

    # 过滤空组件（如version为空时，version_formatted是空字符串，会被过滤）
    components = [c for c in components if c]
    return "_".join(components)
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
        date_part = f"{year}{month.zfill(2)}{day.zfill(2)}" if all([year, month, day]) else datetime.now().strftime("%Y%m%d")

    # 版本号处理（仅对文件有效）
    version_formatted = ""
    if not is_folder:
        version = version or "1.0"
        if '.' not in version:
            if len(version) == 1:
                version_formatted = f"{version}.0"
            else:
                major = version[0]
                minor = version[1:]
                version_formatted = f"{major}.{minor}"
        else:
            version_formatted = version

    # 版本号格式化：统一处理成v1.0样式（若传入空则跳过版本）
    version_formatted = ""
    if version:
        # 去掉版本字符串里可能的v前缀，再拼接成vx.y格式
        version_clean = version.lstrip('vV')
        version_formatted = f"v{version_clean}"

    # 核心逻辑：区分【脚本文件】和【非脚本文件】
    components = [prefix, lang]  # 基础组件：前缀 + 语言标识（如old_bat + bat）

    if not is_folder:  # 非文件夹时才考虑版本/日期
        # 仅脚本类型文件（py/ps）保留版本和日期
        is_script = lang in ['py', 'ps']
        if is_script:
            # 脚本文件：拼接版本 + 日期（如v1.0 + 20250629）
            components.extend([version_formatted, date_part])

    # 过滤空组件（如version为空时，version_formatted是空字符串，会被过滤）
    components = [c for c in components if c]
    return "_".join(components)
    """
    生成重命名后的文件名（区分脚本/非脚本文件逻辑）
    :param prefix:       文件前缀（如 old_bat、old_data）
    :param lang:         语言标识（如 bat、xlsx、py、ps）
    :param version:      版本号（如 "1.0" "v2.1"，空则自动处理）
    :param date_part:    日期部分（如 20250629，非脚本文件会忽略）
    :param is_folder:    是否是文件夹（文件夹无需版本/日期）
    :return:             拼接后的新文件名（带后缀）
    """
    # 版本号格式化：统一处理成 v1.0 样式（若传入空则跳过版本）
    version_formatted = ""
    if version:
        # 去掉版本字符串里可能的 v 前缀，再拼接成 vx.y 格式
        version_clean = version.lstrip('vV')  
        version_formatted = f"v{version_clean}"  

    # 核心逻辑：区分【脚本文件】和【非脚本文件】
    components = [prefix, lang]  # 基础组件：前缀 + 语言标识（如 old_bat + bat）
    
    if not is_folder:  # 非文件夹时才考虑版本/日期
        # 仅脚本类型文件（py/ps）保留版本和日期
        is_script = lang in ['py', 'ps']  
        if is_script:
            # 脚本文件：拼接 版本 + 日期（如 v1.0 + 20250629）
            components.extend([version_formatted, date_part])
    
    # 过滤空组件（如 version 为空时，version_formatted 是空字符串，会被过滤）
    components = [c for c in components if c]  
    return "_".join(components)
    """标准化文件名生成（新增is_folder参数，文件夹不包含版本和日期）"""
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
        date_part = f"{year}{month.zfill(2)}{day.zfill(2)}" if all([year, month, day]) else datetime.now().strftime("%Y%m%d")
    
    # 版本号处理（仅对文件有效）
    version_formatted = ""
    if not is_folder:
        version = version or "1.0"
        if '.' not in version:
            if len(version) == 1:
                version_formatted = f"{version}.0"
            else:
                major = version[0]
                minor = version[1:]
                version_formatted = f"{major}.{minor}"
        else:
            version_formatted = version
    
    # 组合组件（文件夹仅保留前缀和语言标识）
    components = [prefix, lang]
    if not is_folder:
        components.extend([f"v{version_formatted}", date_part])
    components = filter(None, components)
    return "_".join(components)

def rename_entity(old_folder, new_name, source_name, overwrite=False):
    """重命名文件或文件夹"""
    old_folder = os.path.abspath(old_folder)
    source_path = os.path.join(old_folder, source_name)
    if not os.path.exists(source_path):
        source_candidates = [f for f in os.listdir(old_folder) if source_name.lower() in f.lower()]
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
        if '.' in entity_name:
            with open(entity_path, 'w') as f:
                pass
            return True, f"成功创建新文件: {entity_path}"
        else:
            os.makedirs(entity_path)
            return True, f"成功创建新文件夹: {entity_path}"
    except Exception as e:
        return False, f"创建新文件/文件夹失败: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='文件和文件夹重命名与创建工具')
    parser.add_argument('--old_folder', help='文件夹路径', default=None)
    parser.add_argument('--prefix', help='文件名/文件夹名前缀', default='')
    parser.add_argument('--lang', help='语言标识（如py/ps）', default='')
    parser.add_argument('-e', '--ext', help='文件扩展名（可带点号）', default=None)
    parser.add_argument('--version', help='版本号', default='1.0')
    parser.add_argument('--year', help='年份', default='')
    parser.add_argument('--month', help='月份', default='')
    parser.add_argument('--day', help='日期', default='')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在文件/文件夹')
    parser.add_argument('--source', help='源文件名/文件夹名（重命名时必选）', required=False)
    parser.add_argument('--new_entity_name', help='手动指定新文件名/文件夹名', default=None)
    parser.add_argument('--create', action='store_true', help='执行创建新文件/文件夹操作')
    
    args = parser.parse_args()
    
    # 处理文件夹路径
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
        args.ext = args.ext if args.ext else None
    # 处理扩展名（用户指定--ext .txt时优先使用）
    if not args.ext:
        if args.lang.lower() == 'ps':
            args.ext = '.ps1'  # 修正powershell常见扩展名
        else:
            args.ext = '.py'
    
    if args.new_entity_name:
        full_name = args.new_entity_name.replace('-', '_')
        # 有扩展名则为文件，否则为文件夹
        is_folder = '.' not in full_name
        if not is_folder and not full_name.endswith(args.ext):
            full_name += args.ext
    else:
        # 自动生成名称：优先根据--ext判断是否为文件（核心修复点）
        # 1. 先生成临时文件名（按文件逻辑，包含版本/日期）
        temp_name = generate_filename(
            args.prefix, args.lang, args.version,
            args.year, args.month, args.day,
            is_folder=False  # 临时按文件生成完整组件
        )
        # 2. 判断是否为文件夹：若指定了扩展名，则强制为文件
        has_ext = bool(args.ext and args.ext.strip())
        if has_ext:
            is_folder = False  # 有扩展名→必为文件
        else:
            is_folder = '.' not in temp_name  # 无扩展名→按.判断
        
        # 3. 构建完整文件名（添加扩展名）
        full_name = temp_name
        if not is_folder:
            # 确保文件名称以指定扩展名结尾
            if not full_name.endswith(args.ext):
                full_name += args.ext
        else:
            # 若为文件夹，重新生成不含版本/日期的名称
            full_name = generate_filename(
                args.prefix, args.lang, args.version,
                args.year, args.month, args.day,
                is_folder=True
            )
    success, msg = create_new_entity(args.old_folder, full_name)
    
    else:
        if not args.source:
            parser.error("--source 参数在重命名时为必填项")
        source_name = args.source
        source_path = os.path.join(args.old_folder, source_name)
        
        if not os.path.exists(source_path):
            source_candidates = [f for f in os.listdir(args.old_folder) if source_name.lower() in f.lower()]
            if source_candidates:
                source_path = os.path.join(args.old_folder, source_candidates[0])
                print(f"提示: 自动匹配源文件/文件夹: {source_candidates[0]}")
            else:
                parser.error(f"错误: 源文件/文件夹不存在 ({source_path})")
        
        # 确定源是文件还是文件夹
        is_file = os.path.isfile(source_path)
        is_folder = not is_file
        
        # 处理扩展名
        if not args.ext:
            if is_file:
                _, ext = os.path.splitext(source_path)
                args.ext = ext if ext else ('.ps' if args.lang.lower() == 'ps' else '.py')
            else:
                args.ext = '.ps' if args.lang.lower() == 'ps' else '.py'
        args.ext = args.ext or ('.ps' if args.lang.lower() == 'ps' else '.py')
        
        if args.new_entity_name:
            full_name = args.new_entity_name.replace('-', '_')
            if is_file and not full_name.endswith(args.ext):
                full_name += args.ext
        else:
            full_name = generate_filename(
                args.prefix, args.lang, args.version,
                args.year, args.month, args.day,
                source_name=source_name,
                is_folder=is_folder
            )
            if is_file and not full_name.endswith(args.ext):
                full_name += args.ext
        
        success, msg = rename_entity(args.old_folder, full_name, source_name, args.overwrite)
    
    # 输出调试信息
    print(f"\n[调试信息]")
    print(f"args.ext: {args.ext}")
    print(f"full_name: {full_name}")
    print(f"source_path: {source_path if 'source_path' in locals() else 'N/A'}")
    print(f"is_file: {is_file if 'is_file' in locals() else 'N/A'}")
    print(f"overwrite参数: {args.overwrite}")
    
    # 输出结果
    print(f"\n执行详情:")
    print(msg)
    print(f"目标路径: {os.path.join(args.old_folder, full_name)}")
    
    exit(0 if success else 1)