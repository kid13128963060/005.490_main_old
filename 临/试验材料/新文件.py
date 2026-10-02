# 版本说明: V1.0 pywin32基础波浪按键; V1.1 新增字符转虚拟键码+全字母映射; V1.2 增加ctrl、alt、shift修饰键映射; V1.4 改为直接使用虚拟键码配置
import logging
import sys
import win32api
import win32con
from typing import NoReturn

# ===================== 【在此处手动输入虚拟键码】 =====================
# 示例：波浪/反引号按键VK_OEM_3 = 0xC0，可直接修改为其他十六进制虚拟键码
VAR1: int = 0xC0
# ========================================================================

# 日志配置，输出至uia_log.txt
logging.basicConfig(
    filename="uia_log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8"
)
logger = logging.getLogger(__name__)


def simulate_key_press(vk_code: int) -> None:
    """
    根据传入的虚拟键码执行按键按下再释放模拟
    :param vk_code: Windows虚拟键码(整数)
    """
    logger.info(f"模拟按键，虚拟键码:{hex(vk_code)}")
    # 按下按键
    win32api.keybd_event(vk_code, 0, 0, 0)
    # 释放按键
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
    logger.info(f"虚拟键码 {hex(vk_code)} 按下释放动作执行完成")


def main() -> NoReturn:
    try:
        # 校验虚拟键码合法范围，Windows虚拟键码有效区间0x01~0xFF
        if not (0x01 <= VAR1 <= 0xFF):
            raise LookupError(f"虚拟键码 {hex(VAR1)} 超出Windows有效虚拟键码范围")

        simulate_key_press(VAR1)

    except KeyboardInterrupt:
        logger.warning("捕获Ctrl+C，脚本主动退出")
        sys.exit(0)
    except LookupError as ex:
        logger.error(f"LookupError异常: {str(ex)}", exc_info=True)
        sys.exit(1)
    except Exception as ex:
        logger.error(f"脚本运行未知异常：{str(ex)}", exc_info=True)
        sys.exit(1)

    print("脚本执行完毕")
    sys.exit(0)


if __name__ == "__main__":
    main()
