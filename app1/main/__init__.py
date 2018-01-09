# -*- coding:utf-8 -*-
from flask import Blueprint

from app1.models import Permission

main = Blueprint('main',__name__)

"""
程序的路由保存在包里的 app1/main/views.py 模块中，而错误处理程序保存在 app1/main/errors.py 模块中。导入这两个模块就能把路由和错误处理程序与蓝本关联起来
"""
from . import views,errors


"""
在模板中可能也需要检查权限，所以 Permission 类为所有位定义了常量以便于获取。为了
避免每次调用 render_template() 时都多添加一个模板参数，可以使用上下文处理器。上
下文处理器能让变量在所有模板中全局可访问
"""
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)