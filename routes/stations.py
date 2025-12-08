# routes/stations.py
from flask import Blueprint, jsonify, request
import pyodbc
import os
from dotenv import load_dotenv
from models import Station

# Load environment variables from .env file
load_dotenv()

stations_bp = Blueprint('stations', __name__)

# Database connection details from environment variables
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
driver = os.getenv('DB_DRIVER')

# Create a database connection
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};'
            f'SERVER={server},1433;'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
            'Encrypt=yes;'
            'TrustServerCertificate=yes;'
            'Connection Timeout=30;'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Route to get all stations with optional city filter and sorting
@stations_bp.route('/api/stations', methods=['GET'])
def get_stations():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        # Get query parameters
        city = request.args.get('city')
        sort_by = request.args.get('sort_by', 'Nimi')  # Default sort by name
        order = request.args.get('order', 'ASC')  # ASC or DESC
        
        # Validate sort_by to prevent SQL injection
        valid_columns = ['ID', 'Nimi', 'Name', 'Kaupunki', 'Kapasiteet', 'Osoite']
        if sort_by not in valid_columns:
            sort_by = 'Nimi'
        
        # Validate order
        if order.upper() not in ['ASC', 'DESC']:
            order = 'ASC'
        
        cursor = conn.cursor()
        
        if city:
            # Filter by city
            query = f'SELECT * FROM Station WHERE Kaupunki LIKE ? ORDER BY {sort_by} {order}'
            cursor.execute(query, ('%' + city + '%',))
        else:
            # Get all stations
            query = f'SELECT * FROM Station ORDER BY {sort_by} {order}'
            cursor.execute(query)
        
        rows = cursor.fetchall()
        stations = [Station(*row).__dict__ for row in rows]
        conn.close()
        return jsonify(stations)
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Route to get unique cities
@stations_bp.route('/api/cities', methods=['GET'])
def get_cities():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT Kaupunki FROM Station WHERE Kaupunki IS NOT NULL ORDER BY Kaupunki')
        rows = cursor.fetchall()
        cities = [row[0] for row in rows]
        conn.close()
        return jsonify(cities)
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
        cursor.execute('UPDATE Station SET Adress = ?, FID = ?, Kapasiteet = ?, Kaupunki = ?, Kuva = ?, Name = ?, Namn = ?, Nimi = ?, Operaattor = ?, Osoite = ?, Stad = ?, x = ?, y = ? WHERE ID = ?',
                       (data['Adress'], data['FID'], data['Kapasiteet'], data['Kaupunki'], data.get('Kuva'), data['Name'], data['Namn'], data['Nimi'], data['Operaattor'], data['Osoite'], data.get('Stad'), data['x'], data['y'], id))
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

# Custom error handlers for the blueprint
@stations_bp.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@stations_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@stations_bp.errorhandler(Exception)
def handle_exception(e):
    response = {
        'error': 'An unexpected error occurred',
        'message': str(e)
    }
    return jsonify(response), 500