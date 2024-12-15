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
from flask import render_template, redirect, url_for, flash

from app.users import users_bp
@users_bp.route('/account', methods=['GET', 'POST'])
@login_required  # Захищаємо маршрут від неавторизованих користувачів
def account():
    # Передаємо current_user при створенні форми
    form = UpdateAccountForm(current_user=current_user)
    change_password_form = ChangePasswordForm()  # Додано форма для зміни пароля

    if form.validate_on_submit():  # Перевіряємо, чи була форма надіслана та є валідною
        # Оновлення даних користувача
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data  # Оновлення опису

        if form.profile_picture.data:
            # Обробка нового профільного зображення
            picture_file = save_picture(form.profile_picture.data)  # Припустимо, у вас є функція save_picture для обробки файлів
            current_user.profile_picture = picture_file

        db.session.commit()  # Збереження змін у базі даних
        flash("Ваші дані були успішно оновлені!", "success")
        return redirect(url_for('users.account'))

    return render_template("account.html", user=current_user, form=form, change_password_form=change_password_form)

from flask import current_app

from flask_login import logout_user

@users_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('users.login'))
import os

    
@users_bp.route('/users_list')
@login_required  # Перевірка, що користувач увійшов
def users_list():
    users = User.query.all()  # Отримуємо всіх користувачів з бази даних
    if not users:
        flash("Немає зареєстрованих користувачів.", "info")
    return render_template('users_list.html', users=users, users_count=len(users))
from app.users.forms import UpdateAccountForm
@users_bp.route('/update_account', methods=['POST'])
@login_required
def update_account():
    form = UpdateAccountForm(current_user=current_user)

    if form.validate_on_submit():
        # Оновлення даних профілю користувача
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        # Завантаження нового фото профілю
        if form.profile_picture.data:  # Використовуємо profile_picture замість picture
            picture_file = save_picture(form.profile_picture.data)  # Викликаємо функцію для збереження фото
            current_user.profile_image = picture_file

        # Збереження змін у базу даних
        db.session.commit()
        flash('Ваш профіль оновлено!', 'success')
        return redirect(url_for('users.account'))  # Повертаємо на сторінку профілю
    
    # Якщо форма не пройшла валідацію, повертаємо на сторінку профілю з помилками
    return render_template('users/update_profile.html', title='Оновити профіль', form=form)



from app.users.forms import ChangePasswordForm
@users_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        # Перевірка поточного пароля
        if not check_password_hash(current_user.password, form.old_password.data):
            flash('Неправильний поточний пароль.', 'danger')
            return redirect(url_for('users.account'))
        
        # Перевірка нового пароля та підтвердження
        if form.new_password.data != form.confirm_password.data:
            flash('Новий пароль і підтвердження не збігаються.', 'danger')
            return redirect(url_for('users.account'))
        
        # Оновлення пароля користувача
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        
        # Повторне входження користувача після зміни пароля
        login_user(current_user)
        
        flash('Ваш пароль успішно змінено!', 'success')
        return redirect(url_for('users.account'))
    
    # Якщо форма недійсна, повертаємо помилки
    flash('Не вдалося змінити пароль. Перевірте введені дані.', 'danger')
    return redirect(url_for('users.account'))




from werkzeug.utils import secure_filename
def save_picture(picture):
    # Створюємо унікальне ім'я для файлу, щоб уникнути конфліктів
    picture_fn = secure_filename(picture.filename)
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)
    
    # Збереження фото в зазначену директорію
    picture.save(picture_path)
    
    # Повертаємо ім'я файлу для подальшого використання
    return picture_fn