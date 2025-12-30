from flask import Blueprint,render_template

home = Blueprint("homepage",__name__)


@home.route("/")
# @login_required
def main_page():
    from sqlalchemy import func
    from Urology_app.models import Patient
    patients_added_today_obj = Patient.query.filter((func.date(Patient.updated_at))==(func.current_date())).order_by(Patient.name.asc()).all()
    patients_added_today = []
    # print(dir(func.date(Patient.updated_at)))
    for pt in patients_added_today_obj:
        single_dic = {
            'operation':pt.operation,
            # 'name':pt.name,
            'age':pt.age,
            'complaint':pt.complaint,
            'labs':[x.split(":") for x in ((pt.labs).split("\n"))],
            'rads':[x.split(":") for x in ((pt.rads).split("\n"))],
        }
        patients_added_today.append(single_dic)
    return render_template("homepage.html",cards_data=patients_added_today)