FILE_EXT = '.html'
handle_fn_suffix = '_handle'
handle_class_suffix = 'Handler'
JQ = 'jquery-3.1.0.min'

config = {
	# sql
	"SQLALCHEMY_DATABASE_URI": "mysql+pymysql://root:root@localhost/join_us?charset=utf8",
	"SQLALCHEMY_ECHO": False,
	"SQLALCHEMY_TRACK_MODIFICATIONS": True,
	# form
	"CSRF_ENABLED": True,
	"SECRET_KEY": "yanfa_2016_csrf",
}