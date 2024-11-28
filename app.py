from flask import Flask, render_template
from routes.stations import stations_bp
import datetime

app = Flask(__name__)
app.register_blueprint(stations_bp)

@app.route('/')
def index():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)