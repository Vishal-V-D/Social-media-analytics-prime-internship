from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100))
    join_date = Column(TIMESTAMP, server_default=func.now())
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    content = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user = relationship("User", back_populates="posts")
    hashtags = relationship("PostHashtag", back_populates="post")
    comments = relationship("Comment", back_populates="post")

class Hashtag(Base):
    __tablename__ = "hashtags"
    hashtag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(100), unique=True)
    posts = relationship("PostHashtag", back_populates="hashtag")

class PostHashtag(Base):
    __tablename__ = "post_hashtags"
    post_id = Column(Integer, ForeignKey("posts.post_id"), primary_key=True)
    hashtag_id = Column(Integer, ForeignKey("hashtags.hashtag_id"), primary_key=True)
    post = relationship("Post", back_populates="hashtags")
    hashtag = relationship("Hashtag", back_populates="posts")

class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    parent_comment_id = Column(Integer, ForeignKey("comments.comment_id"), nullable=True)
    content = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[comment_id])
