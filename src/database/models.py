import enum

from sqlalchemy import Column, Integer, String, DateTime, func, Enum, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255))
    refresh_token = Column(String(255), nullable=True)
    role = Column('role', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    post = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    author = relationship('User', backref='posts')
    views = Column(Integer, default=0)
    image_url = Column(String)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    # comments = relationship('Comment', backref='post')
    # tags = relationship('Tag', secondary=post_tags_table, back_populates='posts')
    # status = Column(String, default="draft")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
