import mysql.connector

def get_db_connection():
    """Establish a connection to MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="George@20",  # Your MySQL password
        database="hotel_db"
    )



   
    


