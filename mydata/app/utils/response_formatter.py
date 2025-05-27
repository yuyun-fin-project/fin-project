from datetime import datetime

def pack_response(data_key: str, data: list, count_key: str = None, extra: dict = None):
    base = {
        "rsp_code": "00000",
        "rsp_msg": "정상처리",
        "search_timestamp": datetime.now().strftime("%Y%m%d%H%M%S")
    }

    if count_key:
        base[count_key] = len(data)

    base[data_key] = data

    if extra:
        base.update(extra)

    return base
