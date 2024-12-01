#!/bin/bash
#
# 
# chmod +x startup.sh 
# ./startup.sh

# Install ODBC driver
apt-get update && \
    apt-get install -y curl apt-transport-https gnupg && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev && \
    apt-get clean

# Install Python dependencies
pip install -r requirements.txt

# Start the application
gunicorn --bind=0.0.0.0 --timeout 600 app:app