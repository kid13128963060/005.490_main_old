import subprocess


# 温和退出（优先，等待同步）
def close_天翼云盘_grace():
    ret = subprocess.run(["taskkill", "/im", "ecloud.exe"], capture_output=True, text=True)
    return ret


# 强制关闭（卡住时用）
def close_天翼云盘_force():
    ret = subprocess.run(["taskkill", "/f", "/im", "ecloud.exe"], capture_output=True, text=True)
    return ret


# 调用示例
if __name__ == "__main__":
    r = close_天翼云盘_force()
    print(r.stdout)
    print(r.stderr)
