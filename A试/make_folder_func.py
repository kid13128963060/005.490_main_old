from pathlib import Path
import sys


def make_folder(folder_path: str) -> int:
    """
    指定路径新建文件夹，父目录不存在自动创建，已存在不报错
    :param folder_path: 文件夹完整路径
    :return: 返回码 0=成功，1=异常失败
    """
    try:
        p = Path(folder_path)
        p.mkdir(parents=True, exist_ok=True)
        print(f"✅ 目录就绪：{p}")
        return 0
    except Exception as e:
        print(f"❌ 创建目录失败：{folder_path}，错误：{e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：python make_folder.py 目标文件夹路径")
        sys.exit(1)
    target = sys.argv[1]
    code = make_folder(target)
    sys.exit(code)
