from app import db
from app.posts.models import Post




def load_posts():
    return Post.query.order_by(Post.posted.desc()).all()


def save_post(post: dict):
    new_post = Post(
        title=post['title'],
        content=post['content'],
        posted=post['posted'],
        is_active=post['is_active'],
        category=post['category'],
        author=post['author']
    )
    db.session.add(new_post)
    db.session.commit()  # Збереження в базі даних


def get_post(id: int):
    return Post.query.get(id)