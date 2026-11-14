from module.list_operate import list_operate
from module.sevenzip_wrapper import sevenzip_run

# 删除：mode="d"，src参数随便填，这里传dst保持统一
txt = r"E:\备份盘\8000_大文件夹_同\009_备份文件夹_同\快捷方式\quick_dir_list.txt"

sevenzip_run(
    mode="a",
    base_path=r"E:\备份盘\8000_大文件夹_同\009_备份文件夹_同\快捷方式\快捷方式_自.7z",
    src=r"F:\自动同步_只增加\快捷方式_自\*",
)
