import xlrd

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
