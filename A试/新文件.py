import subprocess


def enable_wlan_adapter():
    ps_cmd = r'Enable-NetAdapter -Name "WLAN" -Confirm:$false'
    # 用 pwsh 或者 powershell，windows 一般用 powershell.exe
    p = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, shell=False
    )
    print("out:", p.stdout)
    print("err:", p.stderr)
    return p.returncode


if __name__ == "__main__":
    enable_wlan_adapter()
