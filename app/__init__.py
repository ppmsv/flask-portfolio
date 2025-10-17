import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # SECRET_KEY
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_secret')
    
    # DATABASE
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:ppgpQgsyYbMypYtKNNOPDNTkFeVMgrWL@postgres.railway.internal:5432/railway'
     )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.debug = True

    from .routes import main
    app.register_blueprint(main)

    return app


app = create_app()