# -*- coding: utf-8 -*-
# version: V1.8
# 功能: 指定app_root根目录，自动遍历目录，
#       根据文件名自动搜索目标脚本，匹配ps1/py后缀，
#       使用遍历得到的脚本路径，不硬编码拼接脚本路径；
#       把搜索逻辑封装成函数，target_script_name设置为函数入参，
#       删除函数的app_root形参，app_root使用脚本内部配置变量；
#       只执行脚本搜索；已完整删除第二步业务文件遍历全部代码；
#       修改迭代逻辑，修复原代码递归判断逻辑bug。
# 注意: recursive控制是否递归遍历子文件夹，True开启，False仅扫描一级目录；
#       找不到目标脚本直接提示，函数返回找到的脚本完整路径，未找到返回None。
import os

# ========= 配置项 =========
app_root = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main\App"
recursive = True  # 是否遍历子文件夹，True开启，False仅扫描一级目录
target_script_name = "open_plus_close_wifi"  # 不带后缀的脚本基础名称
# ==========================


def find_target_script(target_script_name: str, recursive: bool):
    """
    在配置的app_root根目录搜索目标脚本，匹配 .ps1 / .py 后缀
    :param target_script_name: 不带后缀的脚本基础名称（输入参数）
    :param recursive: 是否递归遍历子文件夹
    :return: 找到返回脚本完整绝对路径，未找到返回None
    """
    found_script_path = None
    for walk_root, walk_dirs, walk_files in os.walk(app_root):
        for f in walk_files:
            base_name, ext = os.path.splitext(f)
            if base_name == target_script_name and ext in (".ps1", ".py"):
                found_script_path = os.path.join(walk_root, f)
                break
        if found_script_path is not None:
            break
        if not recursive:
            break
    return found_script_path


if __name__ == "__main__":
    # target_script_name：输入，脚本短名；full_script_path：输出，完整路径
    target_script_name = target_script_name
    full_script_path = find_target_script(target_script_name, recursive)
    print(full_script_path)
