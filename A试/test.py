from module.make_folder_func import make_folder_func

if __name__ == "__main__":
    target_dir = r"F:\备份盘\8000_大文件夹_同\009_备份文件夹_同\新建测试目录"
    ret = make_folder_func(target_dir)
    print("返回码：", ret)
