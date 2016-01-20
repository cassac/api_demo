import os
from app import create_app, db
from app.models import User, Friend, Message
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Friend=Friend, Message=Message)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False, test_name=None):
    """Run the unit test."""
    import unittest
    if test_name is None:
        tests = unittest.TestLoader().discover('tests')
    else:
        tests = unittest.TestLoader().loadTestsFromName('tests.' + test_name)
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()