from lib.form import Form, fields
from . import models
 
class LoginForm(Form):
	common_class = 'form-control'
	common_attrs = {'required': True}
	username = fields.Input('用户账号')
	password = fields.Password('用户密码')