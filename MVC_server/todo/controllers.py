from ..todo.utils import render_template
from ..todo.models import Todo
from ..todo.config import BASE_DIR
from ..todo.utils import Response
import os


def index():
    """首页视图函数"""
    todo_list = Todo.all(sort=True, reverse=True)
    context = {
        'todo_list': todo_list,
    }
    return render_template('index.html', **context)


def static(request):
    """读取静态资源试图函数"""
    # 能够处理的静态资源类型
    content_type = {
        'css': 'text/css',
        '.js': 'text/javascipt',
        'png': 'image/png',
        'jpg': 'image/jpeg',
    }
    # 根据请求路径中的文件中后缀判断静态文件类型，指定响应首部字段Content-Type
    headers = {
        'Content-type': content_type.get(request.path[-3:], 'text/plain'),
    }
    # 获取静态资源绝对路径
    path = request.path.lstrip('/')
    file_path = os.path.join(BASE_DIR, path)

    # 读取静态资源内容，构造响应对象并返回
    with open(file_path, 'r') as f:
        body = f.read()
        return Response(body, headers=headers)


routes = {
    '/': (index, ['GET']),
    '/index': (index, ['GET']),
}