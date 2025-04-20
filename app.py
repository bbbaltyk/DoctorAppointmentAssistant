from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./doctors.db/'

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    from routes import register_routes
    register_routes(app, db)
    migrate = Migrate(app, db)

    return app