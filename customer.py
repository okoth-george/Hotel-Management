from database import get_db_connection

def add_customer(name, phone):
    """Adds a new customer and returns customer ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    customer_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return customer_id
