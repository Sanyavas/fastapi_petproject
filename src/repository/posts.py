from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.schemas import PostModel
from src.database.models import Post


async def get_posts(limit: int, offset: int, db: Session):
    posts = db.query(Post).limit(limit).offset(offset).all()
    return posts


async def get_post_id(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    return post


async def create(body: PostModel, db: Session):
    post = Post(**body.dict())
    db.add(post)
    db.commit()
    return post


async def update(post_id: int, body: PostModel, db: Session):
    post = await get_post_id(post_id, db)
    if post:
        post.title = body.title
        post.post = body.post
        post.image_url = body.image_url
        db.commit()
    return post


async def update_like_post(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.likes += 1
        db.commit()
    return post


async def update_dislike_post(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        if post.dislikes is None:
            post.dislikes = 0
        post.dislikes += 1
        db.commit()
    return post


async def remove(post_id: int, db: Session):
    post = await get_post_id(post_id, db)
    if post:
        db.delete(post)
        db.commit()
    return post
