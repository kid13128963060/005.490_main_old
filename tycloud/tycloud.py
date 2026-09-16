import xlrd
import subprocess

# 文件路径
path1 = r"E:\自动同步_只增加\设备识别\设备识别.xls"
current_device = None  # 变量1：当前设备

# 打开xls文件
wb = xlrd.open_workbook(path1)
sheet = wb.sheet_by_index(0)  # 获取第一个工作表

# 行2，列2；xlrd下标从0开始，所以行索引=1，列索引=1
cell_value = sheet.cell_value(rowx=1, colx=1)
print(f"读取到Excel行2列2的值：{cell_value}")

# 判断赋值
if cell_value == "家脑模拟器":
    current_device = 1
elif cell_value == "工脑模拟器":
    current_device = 2
else:
    current_device = None
    print("未匹配到模拟器类型")

print(f"变量【当前设备】的值 = {current_device}")

# ========== 业务分支逻辑 按照你的要求实现 ==========
if current_device == 1:
    # 执行命令1 Disable‑NetAdapter
    print("current_device=1，执行禁用WLAN 2网卡powershell命令")
    cmd = [
        "powershell",
        "-Command",
        'Disable-NetAdapter -Name "WLAN 2" -Confirm:$false'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("命令stdout：", result.stdout)
    print("命令stderr：", result.stderr)

elif current_device == 2:
    print("current_device=2，调用文件1 open+close_wifi 的 open_wifi()")
    # 导入同目录 open+close_wifi.py，调用open_wifi函数
    from open_plus_close_wifi import open_wifi
    open_wifi()

else:
    print("current_device为空，不执行任何操作")
