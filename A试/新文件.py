import urllib.request

# 华硕国内支持页（页面，不是zip直链，仅用于浏览器访问；无法直接抓包拿到永久zip地址）
# 👉 这个脚本只能演示下载逻辑，因为华硕的文件真实地址是动态生成的，会过期
page_url = "https://www.asus.com.cn/supportonly/armoury%20crate/helpdesk_download/"
save_path = "ArmouryCrate_Uninstall_Page.html"

try:
    print("正在下载页面...")
    urllib.request.urlretrieve(page_url, save_path)
    print(f"页面已保存到 {save_path}，请打开html，手动找到卸载工具的zip下载链接")
except Exception as e:
    print(f"下载失败: {e}")
