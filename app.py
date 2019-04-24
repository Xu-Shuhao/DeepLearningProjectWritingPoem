from flask import Flask

app = Flask(__name__)#表示当前调用它的模块的名字


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.debug = True
    app.run()
