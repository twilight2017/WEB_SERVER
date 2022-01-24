# 定义一个Request用于专门解析请求报文
from ..todo.config import BASE_DIR
import os


class Request(object):
    """请求类"""
    def __init__(self, request_message):
        method, path, headers = self.parse_data(request_message)
        self.method = method  # 请求方式定义
        self.path = path  # 请求路径定义
        self.headers = headers  # 请求头{‘HOST’: '127.0.0.1:8000'}

    # 解析请求报文函数
    def parse_data(self, data):
        """解析请求报文数据"""
        # 解析方法：分割'\r\n\r\n'，将得到请求头和请求体
        head, body = data.split('\r\n\r\n', 1)
        method, path, headers = self.parse_header(head)
        return method, path, headers

    # 解析请求报文头
    def parse_header(self, data):
        """解析请求头"""
        # 拆分请求行和请求首部
        request_line, request_header = data.split('\r\n', 1)
        # 请求行拆包示例：
        # ‘GET /index HTTP/1.1’ -> ['GET'. '/index', 'HTTP/1.1']
        # HTTP版本号在本例中无用，用下划线接收
        method, path, _ = request_line.split()

        # 解析请求首部中包含的所有键值对，组装成字典
        headers = {}
        for header in request_header.split('\r\n'):
            k, v = header.split(':', 1)
            headers[k] = v
        return method, path, headers


def render_template(template):
    """读取html内容"""
    template_dir = os.path.join(BASE_DIR, 'templates')
    path = os.path.join(template_dir, template)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    return html


class Response(object):
    """响应类"""
    # 根据状态码获取原因短语
    reason_phrase = {
        200: 'OK',
        405: 'METHOD NOT ALLOWED'
    }

    def __init__(self, body, headers=None, status=200):
        # 默认响应首部字段， 制定响应内容的类型为HTML
        _headers = {'COntent-type': 'text/html; charset=utf-8',
        }

        if headers is not None:
            _headers.update(headers)
        self.headers = _headers  # 设置响应头
        self.body = body  # 设置响应体
        self.status = status  # 设置响应状态码

    def __bytes__(self):
        """构造响应报文"""
        # 状态行 ’HTTP/1.1 200 OK\r\n‘
        header = f'HTTP/1.1 {self.status} {self.reason_phrase.get(self.status, "")}\r\n'
        # 响应首部
        header += ''.join(f'{k}: {v}\r\n' for k,v in self.headers.items())
        # 空行
        blank_line = '\r\n'
        # 响应体
        body = self.body

        response_message = header + blank_line + body
        return response_message.encode('utf-8')