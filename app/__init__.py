from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
# Оголошення базового класу для моделей
class Base(DeclarativeBase):
    pass

# Ініціалізація компонентів
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name="config"):
    # Створення Flask додатку
    app = Flask(__name__)
    app.config.from_object(config_name)  # Завантажуємо конфігурацію
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/images/profile_pics')
    # Ініціалізація bcrypt, бази даних та міграцій
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Налаштування login_manager
    login_manager.login_view = "users.login"  # Маршрут для входу
    login_manager.login_message = "Будь ласка, увійдіть, щоб отримати доступ до цієї сторінки."
    login_manager.login_message_category = "info"

    # Імпорт Blueprint та моделей
    with app.app_context():
        from .users.models import User  # Переконайтесь, що ваша модель 'User' імпортується тут
        from .posts import post_bp
        from .users import users_bp
        app.register_blueprint(post_bp)
        app.register_blueprint(users_bp, url_prefix="/users")

    return app
