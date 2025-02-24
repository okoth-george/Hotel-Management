from database import get_db_connection
from food_menu import get_menu

def place_order(customer_id, food_id, quantity):
    """Places an order and calculates the bill."""
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, price FROM food_menu WHERE id = %s", (food_id,))
    food_item = cursor.fetchone()

    if not food_item:
        return "Invalid Food ID!"

    total_price = food_item[1] * quantity

    # Insert into database
    cursor.execute(
        "INSERT INTO orders (customer_id, food_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
        (customer_id, food_id, quantity, total_price)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"food": food_item[0], "quantity": quantity, "total_price": total_price}
