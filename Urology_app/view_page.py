from flask import Blueprint, render_template,request,jsonify
from flask_login import login_required,current_user
from Urology_app import db
from Urology_app.models import Patient,deletedPatient
import time
from datetime import datetime


view_page = Blueprint("view_page",__name__)

names_to_delete = []
@view_page.route("/delete_patient",methods=['POST']) ## post function return data in request.data as bytes >> convert to str using request.data.decode('utf-8) >> result == 'name=ahmed' >> split and choose ur element;
def delete():
    if request.is_json:
        if request.get_json().get('name'):
            name_to_delete= request.get_json().get('name')
            names_to_delete.append(name_to_delete)
            patient = Patient.query.filter_by(name=name_to_delete).first()
            if patient:
                return jsonify(patient.name)
            else:
                return jsonify('no such patient in db')
        elif request.get_json().get('order') == 'submit delete':
            try:
                patient = Patient.query.filter_by(name=names_to_delete[0]).first()
                names_to_delete.clear()
                names_to_delete.append(patient)
                # delete pt from Patient db
                db.session.delete(patient)
                db.session.commit()
                return jsonify('success')
            except :
                print('no pt in db')
    else:
        print('not is_json now')

@view_page.route("/backup_data",methods=['POST'])
def deletedDB():
    # add pt to deletedPatient 
    if request.is_json :
        patient = names_to_delete[0]
        deleted_pt = deletedPatient(operation=patient.operation,name=patient.name,age=patient.age,gender=patient.gender,complaint=patient.complaint,pmh=patient.pmh,psh=patient.psh,labs=patient.labs,rads=patient.rads,admin=current_user.id)
        db.session.add(deleted_pt)
        db.session.commit()
        names_to_delete.clear()
        return jsonify('sucess')


@view_page.route("/dismiss_deleting",methods=['POST'])
def dismiss():
    ## this method just to clear names_to_delete lis
    names_to_delete.clear()
    return jsonify('success')



@view_page.route("/view_check",methods=['GET','POST']) ## get function return data in request.args
def check():
    ## when first viewing all patients
    all_pts_data = []
    page = (request.args.get('page',1,int))
    all_patients = Patient.query.order_by(Patient.updated_at.desc()).paginate(per_page=6,page=page) ## get all patients in asc order
    from sqlalchemy import func
    for pt in all_patients:
        pt_data = {
            'operation':pt.operation,
            'name':pt.name,
            'age':pt.age,
            'complaint':pt.complaint,
            'pmh':pt.pmh,
            'psh':pt.psh,
            'date': datetime.strftime((pt.updated_at),'%Y/%m/%d'),
        }
        all_pts_data.append(pt_data)
    if request.method == 'GET':
        return (render_template("view_check.html",checked=True,cards_data=all_pts_data,patients_raw=all_patients)) ## returns render_template(whole html file)
        
    if request.method == 'POST':
        btn_id = (request.get_data(as_text=True).split("="))[1]
        if btn_id == 'btnradio1':
            checked=True
        elif btn_id == 'btnradio2' :
            checked= False
        return (render_template("view_check.html",checked=checked,cards_data=all_pts_data,patients_raw=all_patients)) ## returns render_template(whole html file)
            

@view_page.route("/view_page",methods=['POST','GET'])
@login_required
def index():
    ## when searching for single patient
    if request.is_json:
        received_data = request.get_json(force=True, silent=True) ### returns data as text form bytes ## {'name_to_search': 'احمد محمد عبدالله'}
        name_to_search = received_data.get('name_to_search')  ## == احمد محمد عبدالله
        patient = Patient.query.filter_by(name=name_to_search).first()
        if patient: ## patient is class from Patient which is not jsonifiable
            pt_data = {
                'operation':patient.operation,
                'age':patient.age,
                'gender':patient.gender,
                'name':patient.name,
                'complaint':patient.complaint,
                'pmh':patient.pmh,
                'psh':patient.psh,
                'labs':patient.labs,
                'rads':patient.rads,
            }
            time.sleep(1) ## wait for html to load
            return jsonify(pt_data),200 ## server https request succeded 
        else :
            return jsonify([]),200
    return render_template("view_page.html")



