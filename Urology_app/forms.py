from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,IntegerField,TextAreaField,SelectMultipleField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,ValidationError,NumberRange
from Urology_app.models import Patient

## adding form
class RegistrationForm(FlaskForm):
    operation = SelectField('Operation',validators=[DataRequired()],choices=['TURP','TURP&Crushing','TVP','Cystolithotripsy','Cystolithotomy','Ureterolithotomy','URS','DJ removal','JJ fix','D cysto(TURBT)','D cysto & proceed','Pyeloplasty','Nephrectomy(partial)','Nephrectomy(total)'])
    name = StringField('Name',validators=[DataRequired(),Length(min=2,max=32)])
    age = IntegerField('Age',validators=[DataRequired(),NumberRange(min=0,max=100,message='Please enter age (0-100)')])
    gender = SelectField('Gender',choices=[('male','Male'),('female','Female'),('child','Child')],validators=[DataRequired()])
    complaint = TextAreaField('Complaint',validators=[DataRequired(),Length(min=3)])
    pmh = SelectMultipleField('PMH',choices=['free','Anticoagulants(stents)','CKD','NIDDM','IDDM','HTN','IHD','PU','hepatic'])
    psh = TextAreaField('PSH',)
    labs = TextAreaField('Labs')
    rads = TextAreaField('Rad')
    submit = SubmitField('Add Patient')

    ## checking if name in db 
    def validate_username(self,name):
        user = Patient.query.filter_by(username=user.data).first()
        if user:    
            raise ValidationError('This username already exists')


## admins login form
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

