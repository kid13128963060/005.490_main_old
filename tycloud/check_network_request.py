import socket


def check_network_request(timeout=3):
    # 请求国内网站，不容易超时（socket原生实现，不依赖requests）
    try:
        # 创建TCP套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        # 连接百度http 80端口
        sock.connect(("www.baidu.com", 80))
        # 构造简单HTTP GET报文
        http_msg = b"GET / HTTP/1.1\r\nHost:www.baidu.com\r\nConnection:close\r\n\r\n"
        sock.sendall(http_msg)
        # 接收响应头部
        resp = sock.recv(1024).decode("utf‑8", errors="ignore")
        sock.close()
        # 判断是否收到200成功状态码
        return "200 OK" in resp
    except Exception:
        return False


if __name__ == "__main__":
    print(check_network_request())
