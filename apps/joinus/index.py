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
		return handler.render('apply', form=forms.ApplyForm(), applyinfo=preference.load(handler, 'applyinfo'))
	else:
		err = None
		form = forms.ApplyForm(handler.request.form)
		if models.Applicant.find().where(name=form.data.name, phone=form.data.phone).count():
			err = '报名信息已存在'
		else:
			applicant = models.Applicant.create(**form.data)
		return handler.render('apply-result', err=err)