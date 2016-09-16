from lib.handler import AssignableHander
from extypes import list_find
from . import menus, models

class ApplyHandler(AssignableHander):
	def oninit(self):
		self.assign('menus', menus.backend_side_menu)

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
			models.Department.dbcommit()
			models.Department.on_cache_data()
			return '', 204

	def list(self):
		"""招新报名列表"""
		depart_id = self.request.args.get('id', '')
		applicants = models.Applicant.find(first = depart_id)
		return self.render(departments = models.Department.cache, applicants = applicants, depart_id = depart_id)

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

	def apply_count(self, depart):
		"""
		查询报名的人数
		:param depart: 部门对象
		"""
		return models.Applicant.find(first=depart.id).count()

# 首页
def index_handle(handler):
	return handler.render()

# 登录
def login_handle(handler):
	return handler.render()