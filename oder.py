from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session,Blueprint

from database import get_db_connection
from flask_restx import Api, Resource, fields

# create blue print 

odd= Blueprint('odd' , __name__ , template_folder='templates')

@odd.route('/',methods =['GET','POST'])
def order():
    """place an order """
    if 'user' not in session:
        flash("ypu must be logged in to place an order.","danger")
        return redirect('/login')
    if request.method == 'GET':
        return render_template('order.html')
    
    username=session['user']#Get logged-in username 
    food_id = request.form.get('food_id')
    quantity = request.form.get('quantity')

    if   not food_id or not quantity:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        #customer_id = int(customer_id)
        food_id = int(food_id)
        quantity = int(quantity)
    except ValueError:
        return jsonify({"error": "Invalid input type"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
 
    #fetch food details 
    cursor.execute("SELECT name, price FROM food_menu WHERE id = %s", (food_id,))
    food_item = cursor.fetchone()
    if not food_item:
        return jsonify({"error": "Invalid Food ID"}), 404
    
    total_price = food_item[1] * quantity
    try:
        cursor.execute(
            "INSERT INTO orders (username, food_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
            (username, food_id, quantity, total_price)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
    
    flash(f"Order placed successfully! You ordered :{quantity} , {food_item[0]}. Total: ${total_price}", "success")
    return redirect(url_for('odd.order'))

