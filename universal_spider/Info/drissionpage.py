DRISSIONPAGE_PATHS = {
    "browser_path": None,  # 浏览器可执行文件路径
    "local_port": None,  # 本地端口号
    "address": "127.0.0.1:9221",  # 调试浏览器地址，例：127.0.0.1：9222
    "download_path": None,  # 下载文件路径
    "user_data_path": None,  # 用户数据路径
    "cache_path": None,  # 缓存路径
}
DRISSIONPAGE_HEADLESS = True  # 是否无头模式
DRISSIONPAGE_ARGUMENTS = [
    "--no-sandbox",  # 禁用沙盒模式
    "--disable-gpu",  # 禁用GPU加速
    ("--window-size", "1920,1080"),  # 设置浏览器窗口大小
]  # 启动参数
