# app.py
from flask import Flask

gunicorn_app = Flask(__name__)

@gunicorn_app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    gunicorn_app.run(host='0.0.0.0', port=8000)