from pathlib import Path
import shutil


def list_operate(mode: str, src_root_dir: str, dst_root_dir: str, txt_path: str):
    """
    清单操作函数
    :param mode: 'c' = 复制，'d' = 删除
    :param src_root_dir: 源根目录（复制时用，删除时该参数传和dst_root_dir一样的值即可）
    :param dst_root_dir: 目标根目录
    :param txt_path: 清单txt路径
    """
    mode = mode.lower()
    if mode not in ("c", "d"):
        raise ValueError("mode 只能是 c(复制) 或者 d(删除)")

    txt = Path(txt_path)
    with open(txt, "r", encoding="utf-8-sig") as f:
        name_list = [line.strip() for line in f if line.strip()]

    if mode == "c":
        src_root = Path(src_root_dir)
        dst_root = Path(dst_root_dir)
        for name in name_list:
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

    elif mode == "d":
        root = Path(dst_root_dir)
        for name in name_list:
            target = root / name
            print(f"检查：{target}")
            if not target.exists():
                print(f"❌ 不存在：{name}\n")
                continue
            if target.parent != root:
                print(f"⚠️ 不在根目录，跳过：{name}\n")
                continue
            print(f"✅ 准备删除：{target}")
            if target.is_file():
                target.unlink()
            elif target.is_dir():
                shutil.rmtree(target)
            print(f"✅ 已删除：{target}\n")


if __name__ == "__main__":
    txt = r"E:\备份盘\8000_大文件夹_同\009_备份文件夹_同\快捷方式\del_list.txt"
    src = r"F:\自动同步_只增加\快捷方式_自\工脑用\快捷方式_自_工"
    dst = r"F:\自动同步_只增加\快捷方式_自"

    # ===== 调用示例 =====
    # 复制：mode="c"
    list_operate("c", src, dst, txt)

    # 删除：mode="d"，src参数随便填，这里传dst保持统一
    # list_operate("d", dst, dst, txt)
