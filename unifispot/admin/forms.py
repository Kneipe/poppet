from flask_wtf import Form
from wtforms import TextField, HiddenField,SelectField,FileField,BooleanField,PasswordField,TextAreaField,RadioField,SelectMultipleField,widgets,validators
from wtforms.validators import Required
from timezones import zones
from unifispot.const import ROLE_ADMIN,ROLE_CLIENT

        
class SettingsForm(Form):
    unifi_server            = TextField('Controller Host',validators = [Required()])   
    unifi_server_ip         = TextField('Controller IP',validators = [Required()])   
    unifi_port              = TextField('Controller  Port',validators = [Required()])   
    unifi_user              = TextField('Unifi Login',validators = [Required()])   
    unifi_pass              = PasswordField('Unifi Password',validators = [Required()])   

    def populate(self):
        pass


class UserForm(Form):
    email       = TextField('Email',validators = [Required()])
    displayname = TextField('Name',validators = [Required()])
    password    = PasswordField('Password') 
    repassword  = PasswordField('Confirm Password')
    
    def populate(self):
        pass

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.password and (self.password.data != self.repassword.data):
            self.password.errors.append("Entered passwords didn't match")
            return False
        return True

