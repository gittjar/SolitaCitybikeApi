# app.py
from flask import Flask
from routes.stations import stations_bp

gunicorn_app = Flask(__name__)
gunicorn_app.register_blueprint(stations_bp)

@gunicorn_app.route('/')
def hello():
    return "Hello, World! This is server root"

if __name__ == "__main__":
    gunicorn_app.run(host='0.0.0.0', port=8000)