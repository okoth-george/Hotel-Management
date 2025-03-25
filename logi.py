from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session,Blueprint
from database import get_db_connection
from werkzeug.security import  check_password_hash
from flask_restx import Api, Resource, fields,namespace


#create blueprint 

log = Blueprint('log' , __name__ , template_folder='templates')
log_api = Blueprint('log_api', __name__)



#web login page 
@log.route('/', methods=['GET', 'POST'])
def login():
    """login page """
    if request.method=='POST':
        username = request.form['username']
        password= request.form['password']  

        conn = get_db_connection()
        cursor= conn.cursor(dictionary=True) 

        # check if username exists in the database 

        cursor.execute("SELECT * FROM users WHERE username = %s ",(username,))
        user= cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'],password):
            session['user'] = username
            session['role'] = user['role']

            if user ['role'] =='admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('welcome'))
            
        else:
            flash("Invalid username or password. Try again.", "danger")
            return redirect (url_for('log.login'))
    return render_template('login.html')  
# api set up 
# Initialize Flask-RESTx API
api = Api(log_api, title="Login API", description="API for User Login", doc='/swagger/')

# define user model for  login 
login_model =api.model('login',{
   'username': fields.String(required=True, description="User's username"),
    'password': fields.String(required=True, description="User's password")
})

 
# add end point for login 

ns = api.namespace('auth', description="Authentications API Endpoints")

@ns.route('/login')
class LoginApi(Resource):
    @api.expect(login_model) #swager ui will show required fields 
    def post(self):
        """Api for user login """
        data=request.json #get json data from request
        username=data.get('username')
        password=data.get('password')

        conn=get_db_connection()
        cursor=conn.cursor(dictionary= True)

        cursor.execute("SELECT * FROM users WHERE username =%s ",(username,))
        user=cursor.fetchone()

        conn.close()
        cursor.close()

        if user and check_password_hash(user['password_hash'], password):
            return jsonify({
                "message":"login successful !",
                "user" :username,
                "role": user['role']
            })
        else:
            return jsonify({"message": "Invalid username or password"}),401






