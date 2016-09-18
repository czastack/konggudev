from . import forms, models
from lib import preference

# 展示部门介绍
def index_handle(handler):
	from flask import redirect
	return redirect(handler.action('apply'))
	# return handler.render('index', departments = models.Department.cache)

# 填写和处理报名表
def apply_handle(handler):
	if handler.is_get:
		return handler.render('apply', form=forms.ApplyForm(), applyinfo = preference.load(handler, 'applyinfo'))
	else:
		form = forms.ApplyForm(handler.request.form)
		applicant = models.Applicant(form.data)
		applicant.add_self().dbcommit()
		return handler.render('apply-success')