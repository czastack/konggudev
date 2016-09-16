from . import forms, models

# 展示部门介绍
def index_handle(handler):
	return handler.render('index', departments = models.Department.cache)

# 填写和处理报名表
def apply_handle(handler):
	if handler.is_get:
		return handler.render('apply', form=forms.ApplyForm())
	else:
		form = forms.ApplyForm(handler.request.form)
		applicant = models.Applicant(form.data)
		# applicant.addself().dbcommit()
		return handler.render('apply-success')