from flask import Flask
from routes.stations import stations_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(stations_bp, url_prefix='/routes')

@app.route('/')
def hello():
    return "Hello, World! 111"

if __name__ == "__main__":
    app.run()