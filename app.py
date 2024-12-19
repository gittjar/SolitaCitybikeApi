from flask import Flask, render_template_string
from routes.stations import stations_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(stations_bp, url_prefix='/')

@app.route('/')
def hello():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to the API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f4f4f4;
            }
            .container {
                text-align: center;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
            }
            p {
                color: #666;
            }
            .endpoint {
                margin: 10px 0;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the API</h1>
            <p>This is the root page. Here are the available endpoints:</p>
            <div class="endpoint">/api/stations - Get all stations</div>
            <div class="endpoint">/api/stations/&lt;text&gt; - Get stations by name</div>
            <div class="endpoint">/api/station/&lt;id&gt; - Get a station by ID</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == "__main__":
    app.run()