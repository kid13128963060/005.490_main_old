# -*- coding: utf-8 -*-
# version: V1.0
import xlrd

EXCEL_PATH = r"E:\自动同步_只增加\设备识别\设备识别.xls"

def get_current_device():
    wb = xlrd.open_workbook(EXCEL_PATH)
    sheet = wb.sheet_by_index(0)
    cell_value = sheet.cell_value(rowx=1, colx=1)
    print(f"\n读取Excel行2列2的值：{cell_value}")

    if cell_value == "家脑模拟器":
        return 1
    elif cell_value == "工脑模拟器":
        return 2
    else:
        print("未匹配模拟器类型")
        return None

# wrapper逻辑直接写入本文件末尾（要求3，不单独建wrapper_dev.py）
if __name__ == "__main__":
    res = get_current_device()
    print(f"DEV_RET:{res}")
