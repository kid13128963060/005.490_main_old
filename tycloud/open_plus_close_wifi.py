import subprocess


def close_wifi():
    # 执行powershell关闭WLAN网卡
    cmd = [
        "powershell",
        "-Command",
        'Disable-NetAdapter -Name "WLAN" -Confirm:$false'
    ]
    # shell必须为True，windows调用powershell
    subprocess.run(cmd, shell=True)


def open_wifi():
    cmd = [
        "powershell",
        "-Command",
        'Enable-NetAdapter -Name "WLAN" -Confirm:$false'
    ]
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    close_wifi()
