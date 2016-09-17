from lib.handler import AssignableHander
from lib import preference
from extypes import list_find
from . import forms, menus, models

class ApplyHandler(AssignableHander):
	def oninit(self):
		self.assign('menus', menus.backend_side_menu)
		self.assign('thismenu', list_find(menus.backend_side_menu, lambda m: m.name == self.route[-1]))

	def setting(self):
		"""部门招新设置"""
		depart_id = self.request.args.get('id', '')
		if self.is_get:
			departments = models.Department.cache
			depart = list_find(departments, lambda x: x.id == depart_id)
			return self.render(departments = departments, this_depart = depart)
		else:
			data = self.get_args(('predict', 'intro'))
			models.Department.find(id=depart_id).update(data)
			models.dbcommit()
			models.Department.on_cache_data()
			return '', 204

	def info(self):
		applyinfo = preference.load(self, 'applyinfo')
		if self.is_get:
			return self.render(form = forms.ApplyInfoForm(applyinfo._data))
		else:
			form = forms.ApplyInfoForm(self.request.form)
			applyinfo.update(form.data)
			applyinfo.save()
			return '', 204

	def list(self):
		"""招新报名列表"""
		if self.is_get:
			depart_id = self.request.args.get('id', '')
			# if depart_id == 'wenyu':
			# 	children = (depart.id for depart in models.Department.cache if depart.parent == 'wenyu')
			# 	applicants = models.Applicant.query.filter(models.Applicant.first.in_(children))
			departments = (depart for depart in models.Department.cache if depart.id != 'wenyu')
			applicants = models.Applicant.find(first = depart_id)
			return self.render(departments = departments, applicants = applicants, depart_id = depart_id)
		else:
			action = self.request.form.get('action')
			fn = getattr(self, action, None)
			return fn() if fn else ('', 204)

	def detail(self):
		"""详细报名信息"""
		applicant_id = self.request.args.get('id', '')
		applicant = models.Applicant.query.get(applicant_id)
		del applicant.id
		del applicant.status
		applicant.to_read(True)
		datas = (item for item in applicant.iter_label_value() if item[1])
		return self.render(datas = datas)

	def export(self):
		"""导出名单"""
		checked_id = self.request.form.getlist('checked')
		applicants = models.Applicant.query.filter(models.Applicant.id.in_(checked_id))
		if not applicants.count():
			return '', 204
		filename   = self.request.form.get('filename', None)

		from io import BytesIO
		from xlsxwriter import Workbook
		fb = BytesIO()
		workbook   = Workbook(fb, {"in_memory": True})
		worksheet  = workbook.add_worksheet()
		# worksheet.set_column('A:A', len('hello world')+1)
		# 过滤的字段
		passed = ('status',)
		# 写入表头
		i = 0
		for key, doc in models.Applicant.iterdocs():
			if key in passed:
				continue
			worksheet.write(0, i, doc)
			i += 1
		worksheet.write(0, 0, '序号')
		i = 1
		# 写入内容
		for one in applicants:
			j = 0
			worksheet.write(i, j, i) # 序号
			one.to_read()
			one.id = j + 1
			for key, value in one:
				if key in passed:
					continue
				worksheet.write(i, j, value)
				j += 1
			i += 1
		workbook.close()
		# 下载
		if not filename:
			filename = one.first
		filename = filename.encode('UTF-8').decode("latin1") + '.xlsx'
		fb.seek(0)
		return fb.read(), 200, {"Content-Type": "application/vnd.ms-excel", "Content-Disposition": "attachment; filename=" + filename}

	def delete(self):
		checked_id = self.request.form.getlist('checked')
		if checked_id:
			# models.Applicant.query.filter(models.Applicant.id.in_(checked_id)).delete(synchronize_session=False)
			# models.dbcommit()
			return '', 200, {"Refresh": "0"}
		return '', 204

	def apply_count(self, depart):
		"""
		查询报名的人数
		:param depart: 部门对象
		"""
		return models.Applicant.find(first=depart.id).with_entities('*').count()

# 首页
def index_handle(handler):
	return handler.render()

# 登录
def login_handle(handler):
	return handler.render()