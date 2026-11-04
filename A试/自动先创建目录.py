import logging
from pathlib import Path

# 日志完整路径
LOG_FILE_NAME: str = (
    r"F:\带零文件夹\005_计算机科学、程式、资料,硬件\005_74_文件系统、日志、数据记录\005_74_L15_Log日志\ditto_operation.log"
)

# 取出日志所在文件夹路径，自动创建（parents=True 逐级建目录，exist_ok=True 已存在不报错）
log_dir = Path(LOG_FILE_NAME).parent
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE_NAME, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8"
)
logger = logging.getLogger(__name__)
