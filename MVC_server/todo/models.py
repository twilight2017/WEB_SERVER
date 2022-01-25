import os
import json

from MVC_server.todo.config import BASE_DIR


class Todo(object):
    """Todo模型类"""

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.content = kwargs.get('content', '')

    @classmethod
    def _db_path(cls):
        """获取存储todo数据文件的绝对路径"""
        path = os.path.join(BASE_DIR, 'db/todo.json')
        return path

    @classmethod
    def _load_db(cls):
        """加载JSON文件中的所有todo数据"""
        path = cls._db_path()
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def all(cls, sort=False, reverse=False):
        """获取全部Todo"""
        """这一步可将所有从JSON文件中读取的todo数据转换为Todo实例化对象"""
        todo_list = [cls(**todo_dict) for todo_dict in cls._load_db()]
        if sort:
            todo_list = sorted(todo_list, key=lambda x: x.id, reverse=reverse)
        return todo_list
