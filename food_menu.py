from database import get_db_connection

def get_menu():
    """Fetches all food items from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_menu")
    menu = cursor.fetchall()
    cursor.close()
    conn.close()
    return menu
