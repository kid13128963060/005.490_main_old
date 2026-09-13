
import os
import pythoncom
import win32com.client
from typing import Final


def read_simulator_cell(file_path: str) -> str:
    """读取Excel单元格，返回模拟器类型文本"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到文件：{file_path}")

    pythoncom.CoInitialize()
    excel = None
    wb = None
    ws = None
    cell_text: str = ""
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        wb = excel.Workbooks.Open(file_path)
        ws = wb.Worksheets.Item(1)
        cell_text = ws.Cells.Item(2, 2).Text
    finally:
        if wb is not None:
            wb.Close()
        if excel is not None:
            excel.Quit()
        del ws, wb, excel
        pythoncom.CoUninitialize()
    return cell_text


if __name__ == "__main__":
    EXCEL_PATH = r"E:\自动同步_只增加\设备识别\设备识别.xls"
    CELL_READ_CONST: Final[str] = read_simulator_cell(EXCEL_PATH)
    print(f"读取单元格结果：{CELL_READ_CONST}")
