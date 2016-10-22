import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from main import app, db

from flask.ext import migrate
import models
_migrate = migrate.Migrate(app, db)
manager = migrate.Manager(app)
manager.add_command('db', migrate.MigrateCommand)

from flask.ext.script import Shell
manager.add_command("shell", Shell(make_context = {"app": app, "db": db}))

if __name__ == '__main__':
    manager.run()

# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade