# -*- coding:utf-8 -*-
from flask import Blueprint

auth = Blueprint('auth',__name__)

"""
程序的路由保存在包里的 app1/main/views.py 模块中，而错误处理程序保存在 app1/main/errors.py 模块中。导入这两个模块就能把路由和错误处理程序与蓝本关联起来
"""
from . import views