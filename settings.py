handle_fn_suffix = '_handle'
handle_class_suffix = 'Handler'
handle_fn_default = 'default' + handle_fn_suffix
handle_class_default = 'Default' + handle_class_suffix

FILE_EXT = '.html'
FAKE_STATIC = False # 伪静态
FAKE_STATIC_EXT = FILE_EXT

JQ = 'jquery-3.1.0.min'

DB = {'host': 'localhost', 'user': 'root', 'passwd': 'root'}

config = {
	"TEMPLATES_AUTO_RELOAD": True,
	"JSON_AS_ASCII": False,
	"SECRET_KEY": "an_sesstion_secret",

	# sql
	# "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://root:root@localhost/join_us?charset=utf8",
	# "SQLALCHEMY_BINDS": {},
	# "SQLALCHEMY_ECHO": False,
	# "SQLALCHEMY_TRACK_MODIFICATIONS": True,
}