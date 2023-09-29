import logging
from typing import Optional

# from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.schemas import UserModel
from src.database.models import User
from src.services.random_avatars import random_avatar


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


async def get_user_by_username(username: str, db: Session) -> User | None:
    return db.query(User).filter(User.username == username).first()


async def create_user(body: UserModel, db: Session) -> User:
    user_data = body.dict()
    # user_data['avatar'] = random_avatar()
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# async def create_user(username: str, email: str, password: str, db: Session, avatar: Optional[str] = None) -> User:
#
#     user_data = {
#         "username": username,
#         "email": email,
#         "password": password,
#         "avatar": avatar or random_avatar()
#     }
#
#     new_user = User(**user_data)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()

