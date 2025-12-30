from flask import render_template, Blueprint,flash,redirect,request
from Urology_app.forms import LoginForm
from Urology_app.models import Admindb
from flask_login import login_user

login_page = Blueprint("login_page",__name__)

@login_page.route("/login",methods=['POST','GET'])
def login():
    # if current_user.is_authenticated:
    #     return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admindb.query.filter_by(username=form.username.data).first()
        # if admin and bcrypt.check_password_hash(admin.password,form.password.data):
        if admin and (form.password.data == admin.password) :
            login_user(admin,remember=form.remember.data)
            flash('Welcome %s'%(admin.username))
            next_page = request.args.get('next')
            return redirect((next_page) if (next_page) else '/')
        else : flash('No user with this name please check ur username')
    return render_template('login_page.html',
                            form=form)

# Source - https://stackoverflow.com/a
# Posted by K4C, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-11, License - CC BY-SA 4.0


