FILE_EXT = '.html'

handle_fn_suffix = '_handle'
handle_class_suffix = 'Handler'
handle_fn_default = 'default' + handle_fn_suffix
handle_class_default = 'Default' + handle_class_suffix

JQ = 'jquery-3.1.0.min'

config = {
	"TEMPLATES_AUTO_RELOAD": True,
	"JSON_AS_ASCII": False,
	# sql
	"SQLALCHEMY_DATABASE_URI": "mysql+pymysql://root:root@localhost/join_us?charset=utf8",
	"SQLALCHEMY_ECHO": False,
	"SQLALCHEMY_TRACK_MODIFICATIONS": True,
	# form
	"CSRF_ENABLED": True,
	"SECRET_KEY": "yanfa_2016_csrf",
}