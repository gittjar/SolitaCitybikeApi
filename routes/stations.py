from flask import Flask, Blueprint, jsonify, request
import pyodbc
from models import Station

app = Flask(__name__)
stations_bp = Blueprint('stations', __name__)

# Database connection details
server = 'tcp:stone900.database.windows.net,1433'
database = 'GreenlizardDb'
username = 'kingdat4'
password = 'SecretPassword2023'
driver = '{ODBC Driver 18 for SQL Server}'

# Create a database connection
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=tcp:stone900.database.windows.net,1433;'
            'DATABASE=GreenlizardDb;'
            'UID=kingdat4;'
            'PWD=SecretPassword2023;'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Route to get all stations
@stations_bp.route('/api/stations', methods=['GET'])
def get_stations():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Station')
        rows = cursor.fetchall()
        stations = [Station(*row).__dict__ for row in rows]
        conn.close()
        return jsonify(stations)
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Route to get stations by name
@stations_bp.route('/api/stations/<text>', methods=['GET'])
def get_stations_by_name(text):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Station WHERE Nimi LIKE ?', ('%' + text + '%',))
        rows = cursor.fetchall()
        stations = [Station(*row).__dict__ for row in rows]
        conn.close()
        return jsonify(stations)
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Route to get a station by ID
@stations_bp.route('/api/station/<int:id>', methods=['GET'])
def get_station_by_id(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Station WHERE ID = ?', (id,))
        row = cursor.fetchone()
        if row:
            station = Station(*row).__dict__
            conn.close()
            return jsonify(station)
        else:
            conn.close()
            return jsonify({'error': 'Station not found'}), 404
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Route to create a new station
@stations_bp.route('/api/stations', methods=['POST'])
def create_station():
    data = request.get_json()
    required_fields = ['Adress', 'FID', 'Kapasiteet', 'Kaupunki', 'Name', 'Namn', 'Nimi', 'Operaattor', 'Osoite', 'x', 'y']
    
    # Check for missing required fields
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Station (Adress, FID, Kapasiteet, Kaupunki, Kuva, Name, Namn, Nimi, Operaattor, Osoite, Stad, x, y) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (data['Adress'], data['FID'], data['Kapasiteet'], data['Kaupunki'], data.get('Kuva'), data['Name'], data['Namn'], data['Nimi'], data['Operaattor'], data['Osoite'], data.get('Stad'), data['x'], data['y']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Station created successfully'}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Route to update an existing station
@stations_bp.route('/api/station/<int:id>', methods=['PUT'])
def update_station(id):
    data = request.get_json()
    required_fields = ['Adress', 'FID', 'ID', 'Kapasiteet', 'Kaupunki', 'Name', 'Namn', 'Nimi', 'Operaattor', 'Osoite', 'x', 'y']
    
    # Check for missing required fields
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE Station SET Adress = ?, FID = ?, ID = ?, Kapasiteet = ?, Kaupunki = ?, Kuva = ?, Name = ?, Namn = ?, Nimi = ?, Operaattor = ?, Osoite = ?, Stad = ?, x = ?, y = ? WHERE ID = ?',
                       (data['Adress'], data['FID'], data['ID'], data['Kapasiteet'], data['Kaupunki'], data.get('Kuva'), data['Name'], data['Namn'], data['Nimi'], data['Operaattor'], data['Osoite'], data.get('Stad'), data['x'], data['y'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Station updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Route to delete a station
@stations_bp.route('/api/station/<int:id>', methods=['DELETE'])
def delete_station(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Station WHERE ID = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Station deleted successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Custom error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        'error': 'An unexpected error occurred',
        'message': str(e)
    }
    return jsonify(response), 500

# Register your blueprint
app.register_blueprint(stations_bp)

if __name__ == '__main__':
    app.run(debug=True)