"""
Database connection module
"""
import pyodbc
from config import Config

def get_db_connection():
    """
    Create and return a database connection
    
    Returns:
        pyodbc.Connection: Database connection object or None if connection fails
    """
    try:
        conn = pyodbc.connect(Config.get_connection_string())
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None
