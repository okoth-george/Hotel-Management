from flask import Flask, render_template, request,  redirect, url_for, flash, session,Blueprint
from database import get_db_connection
from werkzeug.security import generate_password_hash
import mysql.connector
from flask_restx import Api, Resource, fields,Namespace



#creating blue print 
reg=Blueprint('reg',__name__,template_folder='templates',)


@reg.route('/', methods=['GET', 'POST'])
def register_customer():
    '''reigister new customers '''
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')


        # Hash the password before storing

        if not  username.replace(" ", "").isalpha():
            flash("username should contain only letters ","danger")
            return redirect(url_for('reg.register_customer'))
            
       
        if not password or not password.isdigit()or len(password) !=4:
            flash("usikuwe umbwa password ni 4 digits pekee kama mpesa pin ","danger")
            return redirect(url_for('reg.register_customer'))
        hashed_password=generate_password_hash(password)

        conn =get_db_connection()
        cursor=conn.cursor()
        try :
            cursor.execute("INSERT INTO users (username,password_hash) VALUES (%s ,%s )", (username,hashed_password))
            conn.commit()
            flash("Registration succeful ! please log in. ","success")
        except mysql.connector.Error as e:
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')                


         





