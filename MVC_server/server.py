# to_do list/server.py

import socket
import threading

from todo.config import HOST, PORT, BUFFER_SIZE


# 处理客户端请求
def process_client_request(client):
    """处理客户端请求"""
    # 接收请求报文数据
    request_bytes = b''
    while True:
        chunk = client.recv(BUFFER_SIZE)
        request_bytes += chunk
        if len(chunk) < 1024:
            break

    # 请求报文
    request_message = request_bytes.decode('utf-8')
    print(f'request_message: {request_message}')

    # TODO:解析请求
    # TODO：返回响应

    # 关闭请求
    client.close()


def main():
    """入口函数"""
    with socket.socket() as s:
        # 保证端口的可复用性
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定ip和端口号
        s.bind((HOST, PORT))
        # 设置监听上限
        s.listen(5)
        print(f'running on http:{HOST}:{PORT}')

        while True:
            # 客户端建立socket连接和地址
            client, address = s.accept()
            print(f'client address:{address}')
            # 创建新的线程来处理客户端连接
            # 一个客户端连接由一个线程负责管理
            t = threading.Thread(target=process_client_request, args=(client,))