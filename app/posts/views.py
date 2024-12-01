from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
import json
import os
from datetime import datetime

from .forms import PostForm
from .models import Post
from app import db
from .utils import save_post, load_posts, get_post





@post_bp.route('/<int:id>')
def detail_post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)  # Якщо пост не знайдено, кидаємо помилку 404
    return render_template("detail_post.html", post=post)

@post_bp.route('/')
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post_new = Post(
            title=title,
            content=content,
            posted=datetime.now(),
            is_active=form.is_active.data,
            category=form.category.data,
            author=form.author.data
        )
        db.session.add(post_new)
        db.session.commit()
        flash(f'Post "{title}" added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))
    elif form.errors:
        flash(f"Enter the correct data in the form!", "danger")

    return render_template("add_post.html", form=form)
@post_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    flash(f'Post "{post.title}" has been successfully deleted!', 'success')
    return redirect(url_for('posts.get_posts'))

@post_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get(id)
    if post is None:
        abort(404)  # Якщо пост не знайдено, повертаємо 404

    form = PostForm(obj=post)  # Передаємо поточні дані поста в форму

    if form.validate_on_submit():
        # Оновлюємо дані поста
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.author = form.author.data
        #post.posted = datetime.now()  # Оновлюємо час публікації, якщо потрібно

        db.session.commit()  # Зберігаємо зміни в базі даних
        flash(f'Post "{post.title}" has been updated!', 'success')
        return redirect(url_for('posts.get_posts'))  # Перенаправляємо на список постів після збереження

    return render_template('edit_post.html', form=form, post=post)

@post_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404