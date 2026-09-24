# V2.0.3 Excel读取模块；读取指定单元格获取模拟器标识，
# 返回读取到的字符串，捕获文件读取异常向上抛出，供GUI日志展示
import xlrd


def read_simulator_cell(excel_path: str):
    """读取xls的模拟器标识单元格，返回内容字符串"""
    book = xlrd.open_workbook(excel_path)
    sheet = book.sheet_by_index(0)
    # 根据你实际业务修改行列号
    val = sheet.cell_value(rowx=1, colx=1)  # 读取第2行第2列的单元格
    return str(val)


# 新增：脚本直接运行时调用函数并打印结果，供外部主脚本捕获输出
if __name__ == "__main__":
    out_str = read_simulator_cell(r"E:\自动同步_只增加\设备识别\设备识别.xls")
    print(out_str)
