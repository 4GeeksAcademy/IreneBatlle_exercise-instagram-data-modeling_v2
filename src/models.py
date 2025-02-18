import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from eralchemy2 import render_er


db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class User(BaseModel):
    __tablename__ = 'user'
    ID = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    email = Column(String(20), nullable=False, unique=True)

    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='author')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='following')
    following = relationship('Follower', foreign_keys='Follower.user_from_id', back_populates='follower')

class Follower(BaseModel):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.ID'), primary_key=True, nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.ID'), primary_key=True, nullable=False)

    follower = relationship('User', foreign_keys=[user_from_id], back_populates='following')
    following = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

class Post(BaseModel):
    __tablename__ = 'post'
    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.ID'), nullable=False)

    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Comment(BaseModel):
    __tablename__ = 'comment'
    ID = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('user.ID'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.ID'), nullable=False)

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Media(BaseModel):
    __tablename__ = 'media'
    ID = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_types'), nullable=False)
    url = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey('post.ID'), nullable=False)

    post = relationship('Post', back_populates='media')

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

try:
    result = render_er(db.Model, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
