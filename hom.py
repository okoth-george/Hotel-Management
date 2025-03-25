from flask import Blueprint ,render_template
#create a blue print 
routes = Blueprint ('routes',__name__)
@routes.route('/')
def home():
    '''home page '''
    return render_template('home.html')