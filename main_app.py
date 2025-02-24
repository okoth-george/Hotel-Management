from flask import Flask, render_template, request,  jsonify
from customer import add_customer
from food_menu import get_menu
from order import place_order
from database import get_db_connection


app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    """Homepage"""
    return render_template('index.html')

@app.route('/menu')
def menu():
    """Show food menu"""
    menu_items = get_menu()
    return render_template('menu.html', menu=menu_items)

@app.route('/register', methods=['POST'])
def register_customer():
    """Register a new customer"""
    name = request.form['name']
    phone = request.form['phone']
    customer_id = add_customer(name, phone)
    return jsonify({"message": "Customer registered", "customer_id": customer_id})



@app.route('/order', methods=['GET', 'POST'])
def order():
    """Place an order"""
    if request.method == 'GET':
        return render_template('order.html')
    
    customer_id = request.form.get('customer_id')
    food_id = request.form.get('food_id')
    quantity = request.form.get('quantity')
    
    if not customer_id or not food_id or not quantity:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        customer_id = int(customer_id)
        food_id = int(food_id)
        quantity = int(quantity)
    except ValueError:
        return jsonify({"error": "Invalid input type"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM food_menu WHERE id = %s", (food_id,))
    food_item = cursor.fetchone()
    if not food_item:
        return jsonify({"error": "Invalid Food ID"}), 404
    
    total_price = food_item[1] * quantity
    cursor.execute(
        "INSERT INTO orders (customer_id, food_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
        (customer_id, food_id, quantity, total_price)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"food": food_item[0], "quantity": quantity, "total_price": total_price})
if __name__ == '__main__':
    app.run(debug=True)
