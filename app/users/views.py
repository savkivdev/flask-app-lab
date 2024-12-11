from . import users_bp
from flask import render_template, abort, request, url_for, redirect, make_response, session
from datetime import datetime, timedelta
from flask import flash, Flask
from werkzeug.security import generate_password_hash
from app.users.models import User
from app.users.forms import RegistrationForm
from app.users.forms import LoginForm

@users_bp.route("hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None)  # Вік може бути None, якщо не передано
    return render_template("hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)


@users_bp.route("/profile")
def get_profile():
    if "username" in session:
        cookies = request.cookies
        username_value = session["username"]
        color_scheme = request.cookies.get('color_scheme', 'light')  # За замовчуванням світла тема
        return render_template("profile.html", username=username_value, cookies=cookies, color_scheme=color_scheme)
    flash("Сесія недійсна. Увійдіть знову.", "danger")
    return redirect(url_for("users.login"))






@users_bp.route("/set_cookie", methods=['POST'])
def set_cookie():
    key = request.form['key_cookie']
    value = request.form['value_cookie']
    max_age = int(request.form['time_cookie'])

    if not key:
        flash("Ключ кукі не може бути пустим!", "danger")
        return redirect(url_for('users.get_profile'))

    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie(key, value, max_age=max_age)
    flash("Кука успішно встановлена!", "success")
    return response


@users_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
        return f'Користувач: {username}'
    else:
        return 'Кука не знайдена'


@users_bp.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    key = request.form.get('value_delete_cookie')
    response = make_response(redirect(url_for('users.get_profile')))
    if key and key in request.cookies:
        response.set_cookie(key, '', expires=0)
        flash(f'Кука "{key}" видалена!', 'success')
    else:
        flash(f'Кука "{key}" не існує або ключ не вказано!', 'danger')
    return response


@users_bp.route('/delete_all_cookie', methods=['POST'])
def delete_all_cookie():
    response = make_response(redirect(url_for('users.get_profile')))
    for key in request.cookies.keys():
        response.set_cookie(key, '', expires=0)
    flash('Всі куки видалені!', 'success')
    return response


@users_bp.route("/set_color_scheme", methods=["POST"])
def set_color_scheme():
    scheme = request.form.get('color_scheme', 'light')  # За замовчуванням світла тема
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie('color_scheme', scheme)
    return response





from app import bcrypt
from flask_bcrypt import check_password_hash, generate_password_hash
from app import db

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))  # Перехід на сторінку входу
    return render_template('register.html', form=form,title='Register',)



from flask_login import login_user
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Ви зайшли успішно!", "success")
            return redirect(url_for('users.account'))  # Переходимо на сторінку аккаунту після успішного входу
        else:
            flash("Невірний email або пароль.", "danger")
    return render_template('login.html', form=form)

from flask_login import current_user, login_required
@users_bp.route('/account')
@login_required  # Захищаємо маршрут від неавторизованих користувачів
def account():
    if current_user.is_authenticated:
        flash("Ви зайшли успішно!", "success")
        return render_template("account.html", user=current_user)
    else:
        flash("Спочатку увійдіть у аккаунт.", "warning")
        return redirect(url_for("users.login"))

    
from flask_login import logout_user

@users_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('users.login'))

    
@users_bp.route('/users_list')
@login_required  # Перевірка, що користувач увійшов
def users_list():
    users = User.query.all()  # Отримуємо всіх користувачів з бази даних
    if not users:
        flash("Немає зареєстрованих користувачів.", "info")
    return render_template('users_list.html', users=users, users_count=len(users))