from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Flask-Mail instance
mail = Mail()

# Flask-SQLAlchemy instance
db = SQLAlchemy(session_options={'autocommit': True, 'autoflush': False})

# Flask-Login instance
lm = LoginManager()
