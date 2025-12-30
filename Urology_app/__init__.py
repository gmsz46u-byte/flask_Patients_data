from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
# from flask_ckeditor import CKEditor
# from flask_mail import Mail
# from flask_modals import Modal
import datetime
today = datetime.datetime.now().date()

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate(db)
admin = Admin()
login_manager = LoginManager()
login_manager.login_view = 'login_page.login'  ## equal to endpoint of ur login page >> in here it is in login_page.py >> def login function
login_manager.login_message_category = 'info'


from Urology_app.config import config

def create_app(config_class=config):
    Urology_app = Flask(__name__)
    Urology_app.config.from_object(config)
    from Urology_app.adminbp.routes import MyAdminIndexView
      
    db.init_app(Urology_app)
    bcrypt.init_app(Urology_app)
    # ckeditor.init_app(app)
    # modal.init_app(app)
    # mail.init_app(app)
    admin.init_app(Urology_app,index_view=MyAdminIndexView())
    login_manager.init_app(Urology_app)



    from Urology_app.adminbp.routes import adminbp
    from Urology_app.adding_page import adding_page
    # from Urology_app.deleting_page import deleting_page
    from Urology_app.editing_page import editing_page
    from Urology_app.login_page import login_page
    from Urology_app.view_page import view_page
    from Urology_app.errosbp.routes import errorsbp
    from Urology_app.home.routes import home

    Urology_app.register_blueprint(adminbp)
    Urology_app.register_blueprint(errorsbp)
    Urology_app.register_blueprint(adding_page)
    Urology_app.register_blueprint(editing_page)
    Urology_app.register_blueprint(login_page)
    Urology_app.register_blueprint(view_page)
    Urology_app.register_blueprint(home)





    ## to create db
    ### site at main init page at main app folder
    with Urology_app.app_context():
            # Code that requires application context goes here
            db.create_all()


    
    ## to create admin obj
    ### site at main init page at main app folder
    ## imported admin db from models
    from Urology_app.models import Admindb
    @login_manager.user_loader
    def load_user(admin):
        return Admindb.query.get(admin)









    ## must return app at end of function
    return Urology_app