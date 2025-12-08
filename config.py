"""
Configuration module for database connections and app settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    # Database settings
    DB_SERVER = os.getenv('DB_SERVER')
    DB_DATABASE = os.getenv('DB_DATABASE')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DRIVER = os.getenv('DB_DRIVER')
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    @staticmethod
    def get_connection_string():
        """Build database connection string"""
        return (
            f'DRIVER={Config.DB_DRIVER};'
            f'SERVER={Config.DB_SERVER},1433;'
            f'DATABASE={Config.DB_DATABASE};'
            f'UID={Config.DB_USERNAME};'
            f'PWD={Config.DB_PASSWORD};'
            'Encrypt=yes;'
            'TrustServerCertificate=yes;'
            'Connection Timeout=30;'
        )
