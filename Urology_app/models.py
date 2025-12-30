from flask_login import UserMixin
from sqlalchemy import Column,Integer,String,DateTime,func,create_engine
from Urology_app import db






### create db table for patients :
class Patient(db.Model,UserMixin):
    id = Column(Integer,primary_key=True)
    operation = Column(String,nullable=False)
    name = Column(String,unique=True,nullable=False)
    age = Column(Integer,nullable=False)
    gender = Column(String,nullable=False)
    complaint = Column(String,nullable=False)
    # pmh = db.Column(MutableList.as_mutable(PickleType),default=[],nullable=False)
    pmh = Column(String,nullable=False)
    psh = Column(String,nullable=False)
    labs = Column(String,nullable=False)
    rads = Column(String,nullable=False)
    ## for automatically update time added
    updated_at = Column(DateTime,default=func.now(),onupdate=func.now())
    admin = Column(Integer,db.ForeignKey('admindb.id'),nullable=False)

    def __repr__(self):
        return f"Patient('{self.operation}','{self.age}','{self.gender}',{self.name}','{self.complaint}')"

### create db table for deleted patients :
class deletedPatient(db.Model,UserMixin):
    id = Column(Integer,primary_key=True)
    operation = Column(String,nullable=False)
    name = Column(String,unique=True,nullable=False)
    age = Column(Integer,nullable=False)
    gender = Column(String,nullable=False)
    complaint = Column(String,nullable=False)
    # pmh = db.Column(MutableList.as_mutable(PickleType),default=[],nullable=False)
    pmh = Column(String,nullable=False)
    psh = Column(String,nullable=False)
    labs = Column(String,nullable=False)
    rads = Column(String,nullable=False)
    created_at = Column(DateTime,server_default=func.now())
    admin = Column(Integer,db.ForeignKey('admindb.id'),nullable=False)

    def __repr__(self):
        return f"Patient('{self.operation}','{self.age}','{self.gender}',{self.name}','{self.complaint}')"

### create db table for admin
class Admindb(db.Model,UserMixin):
    id = Column(Integer,primary_key=True)
    username = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    patients = db.relationship("Patient",lazy=True,backref='hx_pt')
    deletedpatients = db.relationship("deletedPatient",lazy=True,backref='hx_pt')

    def __repr__(self):
         return f"Admindb('{self.username}','{self.password}')"

## setting engine
engine = create_engine('sqlite:////D:\\zPASS\\TOOL\\major_python_proj\\flask\\history_app\\instance\\Urology_app.db')
