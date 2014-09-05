from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# Flask-Mail instance
mail = Mail()

# Flask-SQLAlchemy instance
db = SQLAlchemy(session_options={'autocommit': True, 'autoflush': False})

# Flask-Login instance
lm = LoginManager()
