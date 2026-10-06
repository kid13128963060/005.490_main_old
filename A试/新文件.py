from pathlib import Path

"""
p.parent.mkdir(parents=True, exist_ok=True)  # 建父目录，等价 -Force
p.touch(exist_ok=True)  # touch 新建空文件，exist_ok=True 已存在不报错
"""

p = Path(r"E:\备份盘\8000_大文件夹\009_备份文件夹_自\同步用\启动云端覆盖本地用.txt")
p.unlink(missing_ok=True)  # missing_ok=True：文件不存在不抛异常，类似 -Force
