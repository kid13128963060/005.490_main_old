# 版本:V1.16
# 更新：测试模式新增打开 短临.docx
# 修复：VSCode(code.exe) 管道句柄继承导致父进程退出跟着关闭
import subprocess
import os
import sys
import time

# =====================配置区=====================
run_mode = 2  # 1=测试模式，2=正常运行模式
delay_sec = 0.5  # 动作之间延时，单位秒
txt_list_path = r"E:\备份盘\带零文件夹_同\005_计算机科学、程式、资料,硬件\005_400_电脑编程_1\005.490_main_old\A试\要打开文件清单.txt"
ShortTask_txt_path = (
    r"E:\备份盘\600----------------------------技术-应用科学_同\650_管理及辅助服务\650_11_时间管理\短期任务.txt"
)
Short临_docx_path = (
    r"E:\备份盘\600----------------------------技术-应用科学_同\650_管理及辅助服务\650_11_时间管理\短临.docx"
)
# ================================================

print("脚本已启动")
print(f"run_mode = {run_mode}")
print(f"单步延时：{delay_sec} s")
print(f"清单路径：{txt_list_path}")
print(f"清单文件是否存在：{os.path.exists(txt_list_path)}")
print(f"测试附加文件：{ShortTask_txt_path}")
print(f"附加文件是否存在：{os.path.exists(ShortTask_txt_path)}")
print(f"测试附加docx：{Short临_docx_path}")
print(f"docx是否存在：{os.path.exists(Short临_docx_path)}")


def read_txt_list(filepath):
    path_list = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if line:
                    path_list.append(line)
    return path_list


path_list = read_txt_list(txt_list_path)
print(f"读取到 {len(path_list)} 条路径")

if run_mode == 1:
    print("【测试模式】仅校验，并且打开短期任务.txt + 短临.docx")
    if os.path.exists(ShortTask_txt_path):
        print(f"📄 打开测试文件：{ShortTask_txt_path}")
        os.startfile(ShortTask_txt_path)
    else:
        print(f"❌ 测试文件不存在：{ShortTask_txt_path}")

    if os.path.exists(Short临_docx_path):
        print(f"📄 打开测试docx：{Short临_docx_path}")
        os.startfile(Short临_docx_path)
    else:
        print(f"❌ docx文件不存在：{Short临_docx_path}")

    if not path_list:
        print("清单为空或文件不存在")
        sys.exit()

    for p in path_list:
        status = "✅存在" if os.path.exists(p) else "❌不存在"
        print(f"{status} | {p}")

elif run_mode == 2:
    print("【正常运行模式】开始打开")
    if not path_list:
        print("清单为空或文件不存在")
        sys.exit()

    for p in path_list:
        if not os.path.exists(p):
            print(f"❌跳过，不存在：{p}")
            continue

        try:
            if os.path.isdir(p):
                print(f"📂 定位文件夹：{p}")
                cmd = f'explorer /select,"{p}"'
                subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            else:
                if p.lower().endswith(".exe"):
                    print(f"⚙️ 启动程序：{p}")
                    if "code.exe" in p.lower():
                        # VSCode单独处理：切断IO管道 + DETACHED_PROCESS彻底脱离父控制台
                        subprocess.Popen(
                            [p],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            creationflags=subprocess.DETACHED_PROCESS,
                        )
                    else:
                        # Ditto等其他exe保持原有标记
                        subprocess.Popen([p], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:
                    print(f"📄 打开文档：{p}")
                    os.startfile(p)
            time.sleep(delay_sec)
        except Exception as e:
            print(f"⚠️ 打开异常：{p}")
            print(f"错误信息：{str(e)}")
else:
    print(f"错误：run_mode={run_mode}，只能是1或2")
