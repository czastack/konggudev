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
	first.choices = tuple((depart.id, depart.name) for depart in models.Department.cache if depart.id != 'wenyu')
	second.choices = first.choices

class ApplyInfoForm(Form):
	common_class = 'form-control'
	interview_time  = fields.Input('面试时间')
	interview_place = fields.Input('面试地点')
	consult_time    = fields.Input('咨询时间')
	consult_place   = fields.Input('咨询地点')
	result_time     = fields.Input('公示时间')