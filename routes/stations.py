from flask import Blueprint, jsonify
import pyodbc
from models import Station

stations_bp = Blueprint('stations', __name__)

# Database connection details
server = 'tcp:stone900.database.windows.net,1433'
database = 'GreenlizardDb'
username = 'kingdat4'
password = 'SecretPassword2023'
driver = '{ODBC Driver 18 for SQL Server}'

# Create a database connection
def get_db_connection():
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

# Route to get all stations
@stations_bp.route('/api/stations', methods=['GET'])
def get_stations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Station')
    rows = cursor.fetchall()
    stations = [Station(*row).__dict__ for row in rows]
    conn.close()
    return jsonify(stations)

# Route to get stations by name
@stations_bp.route('/api/stations/<text>', methods=['GET'])
def get_stations_by_name(text):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Station WHERE Nimi LIKE ?', ('%' + text + '%',))
    rows = cursor.fetchall()
    stations = [Station(*row).__dict__ for row in rows]
    conn.close()
    return jsonify(stations)

# Route to get a station by ID
@stations_bp.route('/api/station/<int:id>', methods=['GET'])
def get_station_by_id(id):
    conn = get_db_connection()
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