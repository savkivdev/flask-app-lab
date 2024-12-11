from flask_bcrypt import Bcrypt
from app import db, login_manager
from flask_login import UserMixin
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        """Метод для хешування пароля"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Метод для перевірки пароля"""
        return bcrypt.check_password_hash(self.password, password)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))