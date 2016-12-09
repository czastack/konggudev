import sys, os
sys.path.insert(0, os.getcwd())

from main import app, db

import flask_migrate

try:
	import models
except ImportError:
	print('请在apps内的子目录执行以支持migrate')

_migrate = flask_migrate.Migrate(app, db)
manager = flask_migrate.Manager(app)
manager.add_command('db', flask_migrate.MigrateCommand)

from flask_script import Shell
manager.add_command("shell", Shell(make_context=lambda:{"app": app, "db": db}))

if __name__ == '__main__':
    manager.run()

# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade