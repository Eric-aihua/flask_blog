# flask_beginning
使用Flask构建一个Blog，该Blog主要基于Template实现。通过还提供了Restful的API接口

# 初始化数据库
- python manange.py db migrate
- python manange.py db upgrade

# 启动服务
python manage.py runserver

# 启动shell
ipython manage.py shell

# API 测试
## httpie

### 匿名访问
http --json --auth : GET http://127.0.0.1:5000/api/v1.0/posts/

### 授权访问
(venv) $ http --auth <email>:<password> --json POST \
> http://127.0.0.1:5000/api/v1.0/posts/ \
> "body=I'm adding a post from the *command line*."


## 单元测试


