from lib.form import Form, fields
from . import models
 
class PersonInfoForm(Form):
	__label__    = models.User.get_label
	common_attrs = {'required': True}
	username     = fields.Input('用户名', attrs={"readonly": True, 'class': 'text'})
	nickname     = fields.Input(attrs={'class': 'text'})
	gender       = fields.SexChoice()
	email        = fields.Email(attrs={'class': 'text'})
	phone        = fields.Phone(attrs={'class': 'text'})