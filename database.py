import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Alagu@2004",
        database="addiction_recovery_system"
    )
    return connection
# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def check_admin(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return True
    return False
