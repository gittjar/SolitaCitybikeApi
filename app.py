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
        <title>City Bike API</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            .content {
                padding: 30px;
            }
            .query-section {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 25px;
                margin-bottom: 30px;
            }
            .query-section h2 {
                color: #333;
                margin-bottom: 20px;
                font-size: 1.5em;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: #555;
                font-weight: 600;
            }
            .form-group input,
            .form-group select {
                width: 100%;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 1em;
                transition: border-color 0.3s;
            }
            .form-group input:focus,
            .form-group select:focus {
                outline: none;
                border-color: #667eea;
            }
            .form-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 6px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
                margin-right: 10px;
            }
            .btn:hover {
                transform: translateY(-2px);
            }
            .btn-secondary {
                background: #6c757d;
            }
            .results {
                background: white;
                border-radius: 8px;
                padding: 20px;
                margin-top: 20px;
                border: 2px solid #e9ecef;
            }
            .results h3 {
                color: #333;
                margin-bottom: 15px;
            }
            .station-card {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 4px;
            }
            .station-card h4 {
                color: #333;
                margin-bottom: 8px;
            }
            .station-card p {
                color: #666;
                margin-bottom: 5px;
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: #667eea;
                font-size: 1.2em;
            }
            .error {
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 6px;
                border: 1px solid #f5c6cb;
            }
            .api-docs {
                background: #e7f3ff;
                border-radius: 8px;
                padding: 20px;
                margin-top: 20px;
            }
            .api-docs h3 {
                color: #0066cc;
                margin-bottom: 15px;
            }
            .endpoint {
                background: white;
                padding: 10px 15px;
                margin: 8px 0;
                border-radius: 4px;
                border-left: 3px solid #0066cc;
                font-family: 'Courier New', monospace;
            }
            @media (max-width: 768px) {
                .form-row {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚴 City Bike Stations API</h1>
                <p>Search, filter, and explore bike stations</p>
            </div>
            
            <div class="content">
                <div class="query-section">
                    <h2>Search Stations</h2>
                    
                    <div class="form-group">
                        <label for="searchText">Search by Name:</label>
                        <input type="text" id="searchText" placeholder="Enter station name...">
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="cityFilter">Filter by City:</label>
                            <select id="cityFilter">
                                <option value="">All Cities</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="sortBy">Sort By:</label>
                            <select id="sortBy">
                                <option value="Nimi">Name (Nimi)</option>
                                <option value="Kaupunki">City (Kaupunki)</option>
                                <option value="Kapasiteet">Capacity (Kapasiteet)</option>
                                <option value="Osoite">Address (Osoite)</option>
                                <option value="ID">ID</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="sortOrder">Sort Order:</label>
                        <select id="sortOrder">
                            <option value="ASC">Ascending (A-Z, 0-9)</option>
                            <option value="DESC">Descending (Z-A, 9-0)</option>
                        </select>
                    </div>
                    
                    <div>
                        <button class="btn" onclick="searchStations()">🔍 Search</button>
                        <button class="btn btn-secondary" onclick="clearSearch()">🔄 Clear</button>
                    </div>
                </div>
                
                <div id="results" class="results" style="display: none;">
                    <h3>Results (<span id="resultCount">0</span>)</h3>
                    <div id="stationsList"></div>
                </div>
                
                <div class="api-docs">
                    <h3>📚 API Endpoints</h3>
                    <div class="endpoint">GET /api/stations</div>
                    <div class="endpoint">GET /api/stations?city=Helsinki</div>
                    <div class="endpoint">GET /api/stations?sort_by=Kapasiteet&order=DESC</div>
                    <div class="endpoint">GET /api/cities</div>
                    <div class="endpoint">GET /api/stations/&lt;text&gt;</div>
                    <div class="endpoint">GET /api/station/&lt;id&gt;</div>
                </div>
            </div>
        </div>
        
        <script>
            // Load cities on page load
            window.onload = function() {
                fetch('/api/cities')
                    .then(response => response.json())
                    .then(cities => {
                        const select = document.getElementById('cityFilter');
                        cities.forEach(city => {
                            const option = document.createElement('option');
                            option.value = city;
                            option.textContent = city;
                            select.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error loading cities:', error));
            };
            
            function searchStations() {
                const searchText = document.getElementById('searchText').value.trim();
                const city = document.getElementById('cityFilter').value;
                const sortBy = document.getElementById('sortBy').value;
                const sortOrder = document.getElementById('sortOrder').value;
                
                const resultsDiv = document.getElementById('results');
                const stationsList = document.getElementById('stationsList');
                
                resultsDiv.style.display = 'block';
                stationsList.innerHTML = '<div class="loading">⏳ Loading stations...</div>';
                
                let url = '/api/stations';
                const params = new URLSearchParams();
                
                if (city) params.append('city', city);
                if (sortBy) params.append('sort_by', sortBy);
                if (sortOrder) params.append('order', sortOrder);
                
                if (searchText) {
                    url = `/api/stations/${encodeURIComponent(searchText)}`;
                    if (params.toString()) {
                        url += '?' + params.toString();
                    }
                } else if (params.toString()) {
                    url += '?' + params.toString();
                }
                
                fetch(url)
                    .then(response => response.json())
                    .then(stations => {
                        if (stations.error) {
                            stationsList.innerHTML = `<div class="error">❌ ${stations.error}</div>`;
                            return;
                        }
                        
                        document.getElementById('resultCount').textContent = stations.length;
                        
                        if (stations.length === 0) {
                            stationsList.innerHTML = '<p>No stations found.</p>';
                            return;
                        }
                        
                        stationsList.innerHTML = stations.map(station => `
                            <div class="station-card">
                                <h4>${station.Nimi || station.Name || 'N/A'}</h4>
                                <p><strong>Address:</strong> ${station.Osoite || station.Adress || 'N/A'}</p>
                                <p><strong>City:</strong> ${station.Kaupunki || 'N/A'}</p>
                                <p><strong>Capacity:</strong> ${station.Kapasiteet || 'N/A'} bikes</p>
                                <p><strong>Operator:</strong> ${station.Operaattor || 'N/A'}</p>
                            </div>
                        `).join('');
                    })
                    .catch(error => {
                        stationsList.innerHTML = `<div class="error">❌ Error: ${error.message}</div>`;
                    });
            }
            
            function clearSearch() {
                document.getElementById('searchText').value = '';
                document.getElementById('cityFilter').value = '';
                document.getElementById('sortBy').value = 'Nimi';
                document.getElementById('sortOrder').value = 'ASC';
                document.getElementById('results').style.display = 'none';
            }
            
            // Allow Enter key to trigger search
            document.getElementById('searchText').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchStations();
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == "__main__":
    app.run()