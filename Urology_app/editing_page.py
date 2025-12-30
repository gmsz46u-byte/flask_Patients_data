from flask import Blueprint,render_template,request,jsonify
from flask_login import login_required,current_user
from Urology_app import db
from Urology_app.models import Patient
editing_page = Blueprint("editing_page",__name__)


redirected_name = []
names_to_update = []

@editing_page.route("/save_update",methods=['POST'])
@login_required
def update():
    if request.is_json:
        pt_updated_data = []
        data_dict = request.get_json()
        print(data_dict)
        for key,value in data_dict.items():
            pt_updated_data.append(value)
        try:
            patient = Patient.query.filter_by(name=names_to_update[0]).first()
            patient.operatoin = pt_updated_data[0]
            patient.name = pt_updated_data[1]
            patient.age = pt_updated_data[2]
            patient.gender = pt_updated_data[3]
            patient.complaint = pt_updated_data[4]
            patient.pmh = pt_updated_data[5]
            patient.psh = pt_updated_data[6]
            patient.labs = pt_updated_data[7]
            patient.rads = pt_updated_data[8]
            patient.admin = current_user.id
            db.session.commit()
        except:
            print('failed')
        else:
            return jsonify('success')
        finally:
            names_to_update.clear()

@editing_page.route("/editing_page",methods=['POST','GET'])
@login_required
def index():
    if request.is_json:
        name_to_update = request.get_json().get('name_to_update')
        print(name_to_update)
        try:
            names_to_update.clear()
            print(name_to_update)
            patient = Patient.query.filter_by(name=name_to_update).first()
            print(patient)
            pt_data = {
                'operation':patient.operation,
                'name':patient.name,
                'age':patient.age,
                'gender':patient.gender,
                'complaint':patient.complaint,
                'pmh':patient.pmh,
                'psh':patient.psh,
                'labs':patient.labs,
                'rads':patient.rads,
            }
            names_to_update.append(patient.name)
            return render_template("editing_form.html",pt_data=pt_data)
        except :
                print('no patient')
    else :
        stored_name = redirected_name[0] if redirected_name else ''
        redirected_name.clear()
        return render_template("editing_page.html",stored_name=stored_name)
    

# for switching bet pages
@editing_page.route("/switch_pgs",methods=['POST'])
def store_data():
    if request.method == 'POST': ## means it is receiving name from view page
        redirected_name.clear()
        name_to_store = request.get_json().get('name_to_store')
        redirected_name.append(name_to_store)
        return jsonify('success'),200
    ###  not needed below block of code as name is sent immediately using above /editing page route by inserting name as variable into input value
    # elif request.method == 'GET': ## to receive data once redirected
    #     name_to_send = redirected_name[0]
    #     redirected_name.clear()
    #     return jsonify(name_to_send),200
        

