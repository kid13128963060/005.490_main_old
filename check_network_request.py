import requests


def check_network_request(timeout=3):
    try:
        # 请求国内网站，不容易超时
        res = requests.get("https://www.baidu.com", timeout=timeout)
        return res.status_code == 200
    except Exception:
        return False


if __name__ == "__main__":
    print(check_network_request())
