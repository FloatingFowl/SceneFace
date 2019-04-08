# Import Flask related modules and functools
from flask import Flask, request, Response, \
        redirect, render_template,jsonify
#from flask_login import LoginManager, login_required,\
#                                login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.utils import secure_filename

# Create Flask object "app" and create database "db"
app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'server'
ALLOWED_EXTENSIONS = set(['mp4', 'png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Flask-login initialization
#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = "mod_user.register"

# 404 Error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('singlepage.html'), 200

# Import a module / component using its blueprint
# handler variable (mod_auth)
from app.user.controllers import mod_user

# Register blueprints
app.register_blueprint(mod_user)

# Build the database
# Create it using SQLAlchemy
db.create_all()
