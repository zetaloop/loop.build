def wrapper(default):
    def format_datetime(datetime=None, format="medium", **kwargs):
        if datetime and format == "__LOOP__ACCURATETIME":
            time = default(datetime, "Y-M-d-HH-mm-ss", **kwargs)
            Y, M, d, H, m, s = time.split("-")
            if H == m == s == "00":
                return f"{Y}年{M}月{d}日"
            return f"{Y}年{M}月{d}日 {H}:{m}"
        # 00:00:00 视作未填写时间，如需显示请将秒设为非零

        return default(datetime, format, **kwargs)

    return format_datetime


import babel.dates

babel.dates.format_datetime = wrapper(babel.dates.format_datetime)

print("\033[32mINFO    -  Datetime patched (babel.dates.format_datetime)")
