import subprocess


# 强制关闭（卡住时用）
def close_天翼云盘_force():
    ret = subprocess.run(["taskkill", "/f", "/im", "ecloud.exe"], capture_output=True, encoding="gbk", errors="replace")
    return ret


close_天翼云盘_force()
