from ..todo.utils import render_template
from ..todo.models import Todo


def index():
    """首页视图函数"""
    todo_list = Todo.all(sort=True, reverse=True)
    context = {
        'todo_list': todo_list,
    }
    return render_template('index.html', **context)


routes = {
    '/': (index, ['GET']),
    '/index': (index, ['GET']),
}