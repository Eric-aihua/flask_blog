# -*- coding:utf-8 -*-

from flask import Blueprint
"""
 主要演示如果通过api的方式来提供功能
"""

api = Blueprint('api', __name__)

from . import authentication, comments, decorators, users, posts, errors
