import logging

# from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.schemas import UserModel
from src.database.models import User


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_user(email: str, body: UserModel , db: Session) -> None:
    user = await get_user_by_email(email, db)
    if user:
        user.username = body.username
        user.avatar = body.avatar
        db.commit()
    return user

