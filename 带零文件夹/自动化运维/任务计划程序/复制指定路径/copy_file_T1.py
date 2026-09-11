<<<<<<< HEAD
import os
import shutil
from pathlib import Path

# 定义文件路径
source_path = r'''C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\PathHistory.json'''.replace('\n', '')  # 源文件路径
dest_dir = r'''E:\备份盘\8000_大文件夹\009_备份文件夹_自
\005_209_Listary!2_设置\自定义设置\\'''.replace('\n', '')  # 目标文件夹路径
# 目标文件夹路径

# 函数体移至最下方


def copy_file(source_path_str, dest_dir_str, overwrite=False):
    source_path = Path(source_path_str)
    dest_dir = Path(dest_dir_str)
    try:
        # 确保目标目录存在
        os.makedirs(dest_dir, exist_ok=True)
        # 提取源文件的基本名称
        file_name = os.path.basename(source_path)
        # 构建完整的目标路径
        dest_path = os.path.join(dest_dir, file_name)

        # 如果需要强制覆盖且目标文件已存在，则先删除目标文件
        if overwrite and os.path.exists(dest_path):
            os.remove(dest_path)

        # 复制文件（递归参数对单个文件无效）
        shutil.copy2(source_path, dest_path)
        print(f"成功复制文件到: {dest_path}")
    except FileNotFoundError:
        print(f"错误: 源文件不存在 - {source_path}")
    except PermissionError:
        print(f"错误: 权限不足，无法复制文件")
    except IsADirectoryError:
        print(f"错误: 源路径是目录，请使用 copytree 函数进行递归复制")
    except Exception as e:
        print(f"错误: 发生未知错误 - {str(e)}")


# 执行复制操作，开启强制覆盖功能
copy_file(source_path, dest_dir, overwrite=True)
=======
import os
import shutil
from pathlib import Path

# 定义文件路径
source_path = r'''C:\Users\Administrator\AppData\Roaming\Listary\UserProfile
\Settings\PathHistory.json'''.replace('\n', '')  # 源文件路径
dest_dir = r'''E:\备份盘\8000_大文件夹\009_备份文件夹_自
\005_209_Listary!2_设置\自定义设置\\'''.replace('\n', '')  # 目标文件夹路径
# 目标文件夹路径

# 函数体移至最下方


def copy_file(source_path_str, dest_dir_str, overwrite=False):
    source_path = Path(source_path_str)
    dest_dir = Path(dest_dir_str)
    try:
        # 确保目标目录存在
        os.makedirs(dest_dir, exist_ok=True)
        # 提取源文件的基本名称
        file_name = os.path.basename(source_path)
        # 构建完整的目标路径
        dest_path = os.path.join(dest_dir, file_name)

        # 如果需要强制覆盖且目标文件已存在，则先删除目标文件
        if overwrite and os.path.exists(dest_path):
            os.remove(dest_path)

        # 复制文件（递归参数对单个文件无效）
        shutil.copy2(source_path, dest_path)
        print(f"成功复制文件到: {dest_path}")
    except FileNotFoundError:
        print(f"错误: 源文件不存在 - {source_path}")
    except PermissionError:
        print(f"错误: 权限不足，无法复制文件")
    except IsADirectoryError:
        print(f"错误: 源路径是目录，请使用 copytree 函数进行递归复制")
    except Exception as e:
        print(f"错误: 发生未知错误 - {str(e)}")


# 执行复制操作，开启强制覆盖功能
copy_file(source_path, dest_dir, overwrite=True)
>>>>>>> dcb2bd4413adc8b529063e4a9adb64a4d0dc99e9
