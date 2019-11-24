# 使用[Flask](https://flask.palletsprojects.com/en/1.1.x/)开发一个JSON Web服务

# 安装依赖

    pip install Flask
    pip install pytest
    pip install coverage

# 启动flask web服务器

    export FLASK_APP=calculate/__init__.py
    flask run

终端显示，默认在5000端口监听

> \* Serving Flask app "calculate/__init__.py" <br>
> \* Environment: production <br>
> WARNING: This is a development server. Do not use it in a production deployment. <br>
> Use a production WSGI server instead. <br>
> \* Debug mode: off <br>
> \* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) <br>

# 测试服务
可能使用任何web客户端和浏览器测试服务。推荐使用[Postman](https://www.getpostman.com/).

    curl -L 'http://127.0.0.1:5000/cal/add/10/30'

显示JSON格式响应
    
> {"ok":true,"result":40}

# Test and Coverage

可通过在根目录打开cmd

通过执行

```shell
p
```

进行pytest测试

执行

```shell
c
```

进行coverage测试

利用[pytest](http://www.pytest.org/en/latest/)和[coverage](https://coverage.readthedocs.io/en/v4.5.x/)测试和评估代码

执行单元测试
    
    pytest

覆盖率测试:

    coverage run -m pytest

报告覆盖率:

    coverage report

显示覆盖率报告:

> Name                    Stmts   Miss Branch BrPart  Cover <br>
> --------------------------------------------------------- <br>
> calculate\__init__.py       6      0      0      0   100% <br>
> calculate\cal.py           20      0      8      0   100% <br>
> --------------------------------------------------------- <br>
> TOTAL                      26      0      8      0   100% <br>
