# -*- coding: utf-8 -*-
# version: V1.0
import socket

def check_network_request(timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect(("www.baidu.com", 80))
        http_msg = b"GET / HTTP/1.1\r\nHost:www.baidu.com\r\nConnection:close\r\n\r\n"
        sock.sendall(http_msg)
        resp = sock.recv(1024).decode("utf‑8", errors="ignore")
        sock.close()
        return "200 OK" in resp
    except Exception:
        return False

if __name__ == "__main__":
    ret = check_network_request(timeout=3)
    print(f"NET_RET:{ret}")
