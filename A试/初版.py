import shutil
from pathlib import Path


def del_by_list(root_dir: str, txt_path: str):
    """
    根据清单，只删除root_dir根目录下的条目，跳过子目录里的同名项
    :param root_dir: 目标根目录
    :param txt_path: 清单文件路径，一行一个名称
    """
    root = Path(root_dir)
    txt = Path(txt_path)

    with open(txt, "r", encoding="utf-8-sig") as f:
        del_names = [line.strip() for line in f if line.strip()]

    for name in del_names:
        target = root / name
        print(f"检查：{target}")
        if not target.exists():
            print(f"❌ 不存在：{name}\n")
            continue
        # 限定只在根目录，子目录直接跳过
        if target.parent != root:
            print(f"⚠️ 不在根目录，跳过：{name}\n")
            continue

        print(f"✅ 准备删除：{target}")
        if target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
        print(f"✅ 已删除：{target}\n")


# ========== 调用示例 ==========
if __name__ == "__main__":
    del_by_list(
        root_dir=r"F:\自动同步_只增加\快捷方式_自",
        txt_path=r"E:\备份盘\8000_大文件夹_同\009_备份文件夹_同\快捷方式\del_list.txt",
    )


def copy_by_list(src_root_dir: str, dst_root_dir: str, txt_path: str):
    """
    根据清单，从源根目录复制条目到目标根目录
    规则：源不存在跳过；目标已存在直接跳过，不覆盖
    """
    src_root = Path(src_root_dir)
    dst_root = Path(dst_root_dir)
    txt = Path(txt_path)

    # 读取清单
    with open(txt, "r", encoding="utf-8-sig") as f:
        copy_names = [line.strip() for line in f if line.strip()]

    for name in copy_names:
        src_item = src_root / name
        dst_item = dst_root / name
        print(f"\n【{name}】")
        if not src_item.exists():
            print(f"❌ 源不存在：{src_item}")
            continue
        if dst_item.exists():
            print(f"⚠️ 目标已存在，跳过：{dst_item}")
            continue

        print(f"✅ 复制：{src_item} --> {dst_item}")
        if src_item.is_file():
            shutil.copy2(src_item, dst_item)
        elif src_item.is_dir():
            shutil.copytree(src_item, dst_item)
        print(f"✅ 复制完成：{dst_item}")


if __name__ == "__main__":
    copy_by_list(
        src_root_dir=r"F:\自动同步_只增加\快捷方式_自\工脑用\快捷方式_自_工",
        dst_root_dir=r"F:\自动同步_只增加\快捷方式_自",
        txt_path=r"E:\备份盘\8000_大文件夹_同\009_备份文件夹_同\快捷方式\del_list.txt",
    )
