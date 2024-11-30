from flask import Flask
from routes.stations import stations_bp

app = Flask(__name__)
app.register_blueprint(stations_bp)

@app.route('/')
def hello_world():
    return "This is API root"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)