# -*- coding: utf-8 -*-
# 功能：时间段命中则执行 open_plus_close_wifi，参数["2"]
import datetime
from Combination_Module.run_python_script import run_python_script

# ====================== 顶部配置区（可自行修改，24小时制，HH:MM） ======================
TIME_START1 = "00:00"  # 分支1起始时间
TIME_END1 = "07:08"  # 分支1结束时间
# ====================================================================================


def time_is_between(start_hhmm: str, end_hhmm: str) -> bool:
    """
    判断当前本地时间是否在 [start_hhmm, end_hhmm] 时间段内
    格式 HH:MM，仅支持同一天时段，不支持跨午夜
    """
    now = datetime.datetime.now()
    s_h, s_m = map(int, start_hhmm.split(":"))
    e_h, e_m = map(int, end_hhmm.split(":"))

    start_tm = datetime.time(hour=s_h, minute=s_m)
    end_tm = datetime.time(hour=e_h, minute=e_m)
    now_tm = now.time()

    return start_tm <= now_tm <= end_tm


if __name__ == "__main__":
    if time_is_between(TIME_START1, TIME_END1):
        run_python_script("open_plus_close_wifi", extra_args=["2"])
