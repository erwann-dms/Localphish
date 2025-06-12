import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import yaml

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Load config from YAML
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    app.config['SECRET_KEY'] = config.get("secret_key", os.urandom(24))
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get("database_uri", "sqlite:///localphish.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "info"
    
    from .auth import auth_bp
    from .campaigns import campaigns_bp
    from .dns_spoof import dns_spoof_bp
    from .proxy import proxy_bp
    from .smtp_sender import smtp_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(campaigns_bp)
    app.register_blueprint(dns_spoof_bp)
    app.register_blueprint(proxy_bp)
    app.register_blueprint(smtp_bp)
    
    @app.route('/')
    def index():
        return "<h1>LocalPhish-Advanced: GoPhish-like local phishing platform</h1><p>Go to /login to start.</p>"
    
    return app
