from lib.form import Form, fields

from . import models
 
class ApplyForm(Form):
	__label__    = lambda k: getattr(models.Applicant, k).doc
	common_class = 'form-control'
	common_attrs = {'required': True}
	name    = fields.Input()
	sex     = fields.SexChoice()
	age     = fields.Number(attrs={'min':17, 'max': 22})
	college = fields.Select() # AutoCompleteInput
	major   = fields.Input()
	home    = fields.Input()
	phone   = fields.Phone()
	qq      = fields.Number()
	hobby   = fields.TextArea()
	reason  = fields.TextArea()
	first   = fields.Select()
	second  = fields.Select()

	# college.choices = ('collegelist', tuple(col.name for col in models.College.query))
	college.choices = tuple((col.id, col.name) for col in models.College.query)
	first.choices = tuple((depart.id, depart.name) for depart in models.Department.cache)
	second.choices = first.choices
