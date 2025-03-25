from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session

from database import get_db_connection

from hom import routes
from menuu import all
from regi import reg
from logi import log , log_api
from oder import odd

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Required for flash messages & session handling
app.register_blueprint(routes)
app.register_blueprint(all, url_prefix='/menu')
app.register_blueprint(log, url_prefix='/login')
app.register_blueprint(log_api, url_prefix='/api')
app.register_blueprint(reg,url_prefix='/register')
app.register_blueprint(odd,url_prefix=( '/order '))




@app.route('/welcome')
def welcome():
    """Welcome page after login"""
    if 'user' in session:
        return render_template('welcome.html')
    return redirect(url_for('log.login'))

@app.route('/logout')
def logout():
    """Logout function"""
    session.pop('user',None)
    session.pop('user_id',None)
   # flash("Logged out successfully!", "info")
    return redirect(url_for('log.login'))

#  ADMIN DASHBOARD-----------------------------------------

@app.route('/admin')
def admin_dashboard():
    """Admin Dashboard"""
    if 'user' not in session or session.get('role') != 'admin':
        flash("access denied ! Admins only.""danger")
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')


# ------------------- USER MANAGEMENT -------------------
@app.route('/admin/users')
def manage_users():
     """View All Users"""
     if 'user' not in session or session.get('role') !='admin':
         flash("access denied!","danger")
         return redirect(url_for('login'))
     
     conn = get_db_connection()
     cursor = conn.cursor(dictionary=True)
     cursor.execute("SELECT id, username, role FROM users")
     users = cursor.fetchall()
     cursor.close()
     conn.close()

     return render_template('admin_users.html', users=users)

@app.route('/admin/users/promote/<int:user_id>')
def promote_user(user_id):
    """Promote User to Admin"""
    if 'user' not in session or session.get('role') != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = 'admin' WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("User promoted to admin!", "success")
    return redirect(url_for('manage_users'))


@app.route('/admin/users/delete/<int:user_id>')
def delete_user(user_id):
    """Delete User"""
    if 'user' not in session or session.get('role') != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("User deleted successfully!", "success")
    return redirect(url_for('manage_users'))

# ------------------- FOOD MANAGEMENT -------------------
@app.route('/admin/food')
def manage_food():
    """View All Food Items"""
    if 'user' not in session or session.get('role') != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM food_menu")
    food_items = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin_food.html', food_items=food_items)

@app.route('/admin/food/add', methods=['GET', 'POST'])
def add_food():
    """Add New Food Item"""
    if 'user' not in session or session.get('role') != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')

        if not name or not price:
            flash("Please provide both name and price!", "danger")
            return redirect(url_for('add_food'))  # Redirect back to the form

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO food_menu (name, price) VALUES (%s, %s)", (name, price))
            conn.commit()
            flash("Food item added successfully!", "success")
            #return redirect(url_for('manage_food'))  # Redirect after successful insert
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    return render_template('add_food.html')  # Show form on GET request


@app.route('/admin/food/delete/<int:food_id>')
def delete_food(food_id):
    """Delete Food Item"""
    if 'user' not in session or session.get('role') != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM food_menu WHERE id = %s", (food_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Food item deleted successfully!", "success")
    return redirect(url_for('manage_food'))
                         
@app.route('/admin/food/edit/<int:food_id>', methods=['GET', 'POST'])
def edit_food(food_id):
    """Edit Food Item"""
    if 'user' not in session or session.get('role') != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch existing food item
    cursor.execute("SELECT * FROM food_menu WHERE id = %s", (food_id,))
    food_item = cursor.fetchone()
    
    if not food_item:
        flash("Food item not found!", "danger")
        return redirect(url_for('manage_food'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        #description = request.form['description']
        
        # Update food item
        cursor.execute("UPDATE food_menu SET name = %s, price = %s  WHERE id = %s", 
                       (name, price,  food_id))
        conn.commit()
        flash("Food item updated successfully!", "success")
        return redirect(url_for('manage_food'))
    
    cursor.close()
    conn.close()
    
    return render_template('edit_food.html', food=food_item)
   



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
