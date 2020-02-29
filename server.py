from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "<h1 style='text-align: center'>This is first version code!</h1>"


if __name__ == '__main__':
    app.run()
