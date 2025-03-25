from flask import Blueprint ,render_template
from food_menu import get_menu
#create a blue print 
all= Blueprint ('all',__name__,template_folder='templates', )
@all .route('/')
def menu():
    '''menu interface..show food menu  '''
    menu_items=get_menu()
    return render_template('menu.html',menu = menu_items)