<<<<<<< HEAD
import os
import re
import sys
import argparse
from datetime import datetime
import pygetwindow as gw


def get_last_active_explorer_path():
    """获取最后活动的资源管理器窗口路径（备用方案）"""
    try:
        explorer_windows = [
            w for w in gw.getWindowsWithTitle('文件资源管理器') if w.title]
        if not explorer_windows:
            explorer_windows = [
                w for w in gw.getWindowsWithTitle('Explorer') if w.title]

        if explorer_windows:
            last_active = max(explorer_windows, key=lambda w: w.activate_time)
            path_match = re.search(r'^(.+?) - 文件资源管理器$', last_active.title)
            if not path_match:
                path_match = re.search(
                    r'^(.+?) - Explorer$', last_active.title)

            if path_match:
                return path_match.group(1).strip()
    except Exception as e:
        print(f"获取资源管理器路径失败: {e}")
    return None


def create_new_entity(old_folder, prefix, lang, ext, new_entity_name=None, is_file=True):
    """
    创建新文件或文件夹，自动处理不存在的路径

    参数:
        old_folder: 目标路径（手动指定，具有最高优先级）
        prefix: 名称前缀
        lang: 语言标识
        ext: 文件扩展名
        new_entity_name: 手动指定的名称（可选）
        is_file: 是否创建文件（True）或文件夹（False）
    """
    # 确保目标路径存在，不存在则创建
    try:
        os.makedirs(old_folder, exist_ok=True)
        print(f"确保路径存在: {old_folder}")
    except Exception as e:
        print(f"创建路径失败: {e}")
        return None

    # 确定新实体名称
    if new_entity_name:
        entity_name = new_entity_name
    else:
        # 生成基于时间的名称
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{prefix}_{timestamp}" if prefix else f"new_entity_{timestamp}"

        # 添加文件扩展名（如果是文件）
        if is_file:
            # 根据语言确定扩展名
            lang_ext_map = {
                'py': '.py',
                'ps': '.ps1',
                'txt': '.txt',
                'md': '.md',
                'html': '.html',
                'css': '.css',
                'js': '.js'
            }

            if ext:
                file_ext = ext if ext.startswith('.') else f'.{ext}'
            else:
                file_ext = lang_ext_map.get(lang.lower(), '.txt')

            entity_name = f"{base_name}{file_ext}"
        else:
            entity_name = base_name

    # 完整路径
    entity_path = os.path.join(old_folder, entity_name)

    # 避免名称冲突
    counter = 1
    while os.path.exists(entity_path):
        if is_file:
            name, ext = os.path.splitext(entity_name)
            entity_path = os.path.join(old_folder, f"{name}_{counter}{ext}")
        else:
            entity_path = os.path.join(old_folder, f"{entity_name}_{counter}")
        counter += 1

    # 创建实体
    try:
        if is_file:
            with open(entity_path, 'w', encoding='utf-8') as f:
                # 可以根据需要添加文件初始内容
                pass
            print(f"文件创建成功: {entity_path}")
        else:
            os.makedirs(entity_path, exist_ok=True)
            print(f"文件夹创建成功: {entity_path}")
        return entity_path
    except Exception as e:
        print(f"创建实体失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='文件和文件夹创建工具（手动指定路径为最高优先级）')
    parser.add_argument('--create', action='store_true', help='执行创建操作')
    parser.add_argument('--old_folder', help='手动指定目标路径（最高优先级）')
    parser.add_argument('--prefix', help='名称前缀')
    parser.add_argument('--lang', help='语言标识（如py, ps, txt等）')
    parser.add_argument('--ext', help='文件扩展名（如.txt）')
    parser.add_argument('--new_entity_name', help='手动指定新实体名称')
    parser.add_argument('--folder', action='store_true', help='创建文件夹而不是文件')

    args = parser.parse_args()

    if not args.create:
        print("请使用--create参数执行创建操作")
        return

    # 确定目标路径 - 手动指定路径为最高优先级
    target_path = args.old_folder

    # 如果没有手动指定路径，尝试获取资源管理器路径
    if not target_path:
        print("未手动指定路径，尝试获取资源管理器路径...")
        target_path = get_last_active_explorer_path()

        # 如果仍无法获取路径，使用当前工作目录
        if not target_path:
            target_path = os.getcwd()
            print(f"使用当前工作目录: {target_path}")
        else:
            print(f"使用资源管理器路径: {target_path}")
    else:
        print(f"使用手动指定路径: {target_path}")  # 明确显示使用了手动指定的路径

    # 创建新实体
    create_new_entity(
        old_folder=target_path,
        prefix=args.prefix,
        lang=args.lang,
        ext=args.ext,
        new_entity_name=args.new_entity_name,
        is_file=not args.folder
    )


if __name__ == "__main__":
    main()
=======
import os
import re
import sys
import argparse
from datetime import datetime
import pygetwindow as gw


def get_last_active_explorer_path():
    """获取最后活动的资源管理器窗口路径（备用方案）"""
    try:
        explorer_windows = [
            w for w in gw.getWindowsWithTitle('文件资源管理器') if w.title]
        if not explorer_windows:
            explorer_windows = [
                w for w in gw.getWindowsWithTitle('Explorer') if w.title]

        if explorer_windows:
            last_active = max(explorer_windows, key=lambda w: w.activate_time)
            path_match = re.search(r'^(.+?) - 文件资源管理器$', last_active.title)
            if not path_match:
                path_match = re.search(
                    r'^(.+?) - Explorer$', last_active.title)

            if path_match:
                return path_match.group(1).strip()
    except Exception as e:
        print(f"获取资源管理器路径失败: {e}")
    return None


def create_new_entity(old_folder, prefix, lang, ext, new_entity_name=None, is_file=True):
    """
    创建新文件或文件夹，自动处理不存在的路径

    参数:
        old_folder: 目标路径（手动指定，具有最高优先级）
        prefix: 名称前缀
        lang: 语言标识
        ext: 文件扩展名
        new_entity_name: 手动指定的名称（可选）
        is_file: 是否创建文件（True）或文件夹（False）
    """
    # 确保目标路径存在，不存在则创建
    try:
        os.makedirs(old_folder, exist_ok=True)
        print(f"确保路径存在: {old_folder}")
    except Exception as e:
        print(f"创建路径失败: {e}")
        return None

    # 确定新实体名称
    if new_entity_name:
        entity_name = new_entity_name
    else:
        # 生成基于时间的名称
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{prefix}_{timestamp}" if prefix else f"new_entity_{timestamp}"

        # 添加文件扩展名（如果是文件）
        if is_file:
            # 根据语言确定扩展名
            lang_ext_map = {
                'py': '.py',
                'ps': '.ps1',
                'txt': '.txt',
                'md': '.md',
                'html': '.html',
                'css': '.css',
                'js': '.js'
            }

            if ext:
                file_ext = ext if ext.startswith('.') else f'.{ext}'
            else:
                file_ext = lang_ext_map.get(lang.lower(), '.txt')

            entity_name = f"{base_name}{file_ext}"
        else:
            entity_name = base_name

    # 完整路径
    entity_path = os.path.join(old_folder, entity_name)

    # 避免名称冲突
    counter = 1
    while os.path.exists(entity_path):
        if is_file:
            name, ext = os.path.splitext(entity_name)
            entity_path = os.path.join(old_folder, f"{name}_{counter}{ext}")
        else:
            entity_path = os.path.join(old_folder, f"{entity_name}_{counter}")
        counter += 1

    # 创建实体
    try:
        if is_file:
            with open(entity_path, 'w', encoding='utf-8') as f:
                # 可以根据需要添加文件初始内容
                pass
            print(f"文件创建成功: {entity_path}")
        else:
            os.makedirs(entity_path, exist_ok=True)
            print(f"文件夹创建成功: {entity_path}")
        return entity_path
    except Exception as e:
        print(f"创建实体失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='文件和文件夹创建工具（手动指定路径为最高优先级）')
    parser.add_argument('--create', action='store_true', help='执行创建操作')
    parser.add_argument('--old_folder', help='手动指定目标路径（最高优先级）')
    parser.add_argument('--prefix', help='名称前缀')
    parser.add_argument('--lang', help='语言标识（如py, ps, txt等）')
    parser.add_argument('--ext', help='文件扩展名（如.txt）')
    parser.add_argument('--new_entity_name', help='手动指定新实体名称')
    parser.add_argument('--folder', action='store_true', help='创建文件夹而不是文件')

    args = parser.parse_args()

    if not args.create:
        print("请使用--create参数执行创建操作")
        return

    # 确定目标路径 - 手动指定路径为最高优先级
    target_path = args.old_folder

    # 如果没有手动指定路径，尝试获取资源管理器路径
    if not target_path:
        print("未手动指定路径，尝试获取资源管理器路径...")
        target_path = get_last_active_explorer_path()

        # 如果仍无法获取路径，使用当前工作目录
        if not target_path:
            target_path = os.getcwd()
            print(f"使用当前工作目录: {target_path}")
        else:
            print(f"使用资源管理器路径: {target_path}")
    else:
        print(f"使用手动指定路径: {target_path}")  # 明确显示使用了手动指定的路径

    # 创建新实体
    create_new_entity(
        old_folder=target_path,
        prefix=args.prefix,
        lang=args.lang,
        ext=args.ext,
        new_entity_name=args.new_entity_name,
        is_file=not args.folder
    )


if __name__ == "__main__":
    main()
>>>>>>> dcb2bd4413adc8b529063e4a9adb64a4d0dc99e9
