from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from flask_migrate import Migrate
import logging
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

load_dotenv()

app = Flask(__name__)

# Load configuration from Config object
from config import Config
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail(app)

# Migration management
migrate = Migrate(app, db)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Register blueprints
from core.routes.main_routes import main
from core.routes.auth_routes import auth
from core.routes.operator_routes import operator
from core.routes.agent_routes import agent
from core.routes.job_routes import job
from core.routes.support_routes import support
from core.routes.admin_routes import admin_bp, MyAdminIndexView, MyModelView

admin = Admin(app, name='Tractor Operator Admin Panel', template_mode='bootstrap4', index_view=MyAdminIndexView())

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(operator)
app.register_blueprint(agent)
app.register_blueprint(job)
app.register_blueprint(support)
app.register_blueprint(admin_bp)

# Add admin views for models
from core.models import User, Operator, Job, Admin as AdminModel, FAQ

admin.add_view(MyModelView(User, db.session, endpoint='user_admin'))
admin.add_view(MyModelView(Operator, db.session, endpoint='operator_admin'))
admin.add_view(MyModelView(Job, db.session, endpoint='job_admin'))
admin.add_view(MyModelView(FAQ, db.session, endpoint='faq_admin'))
admin.add_view(MyModelView(AdminModel, db.session, endpoint='admin_admin'))

# Setup scheduler for background tasks (for example job management)
scheduler = BackgroundScheduler()
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
