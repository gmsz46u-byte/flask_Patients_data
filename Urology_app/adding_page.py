from flask import render_template, Blueprint,flash,redirect
from flask_login import login_required,current_user
from Urology_app.forms import RegistrationForm
from Urology_app import db, bcrypt 
from Urology_app.models import Patient

adding_page = Blueprint("adding_page",__name__)

## adding route
@adding_page.route("/adding_page",methods=['POST','GET'])
@login_required
def add():
    form = RegistrationForm()
    if form.validate_on_submit():
            ## check if name is is db
            check = check_name(form.name.data)
            if check :
                ## add data to db
                pmh = "&".join(form.pmh.data)
                pt = Patient(operation=form.operation.data,name=form.name.data.strip(),age=form.age.data,gender=form.gender.data,complaint=form.complaint.data,pmh=pmh,psh=form.psh.data,labs=form.labs.data,rads=form.rads.data,admin=current_user.id)
                db.session.add(pt)
                db.session.commit()
                ## flashing success msg and redirect for new pt adding
                flash('Successfully added {0}'.format(form.name.data),'success')
                return redirect('/adding_page')
    return render_template("adding_page.html",
                           form=form)


## function to check if name is in db
## not working properly
def check_name(name):
            ## check if name in db
            pt = Patient.query.filter_by(name=name).first()
            if not pt :
                return name
            else:
                flash('Name is already in db','danger')
                  
    