from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base, User, Post, Hashtag, PostHashtag, Comment
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

u1 = User(name="Alice", email="alice@mail.com")
u2 = User(name="Bob", email="bob@mail.com")
u3 = User(name="Charlie", email="charlie@mail.com")

p1 = Post(user=u1, content="Loving #AI and #Python")
p2 = Post(user=u2, content="Exploring #Tech and #AI")
p3 = Post(user=u3, content="Learning #Python for data science")

h1 = Hashtag(tag="#AI")
h2 = Hashtag(tag="#Python")
h3 = Hashtag(tag="#Tech")
h4 = Hashtag(tag="#DataScience")

session.add_all([u1, u2, u3, p1, p2, p3, h1, h2, h3, h4])
session.commit()

session.add_all([
    PostHashtag(post=p1, hashtag=h1),
    PostHashtag(post=p1, hashtag=h2),
    PostHashtag(post=p2, hashtag=h3),
    PostHashtag(post=p2, hashtag=h1),
    PostHashtag(post=p3, hashtag=h2),
    PostHashtag(post=p3, hashtag=h4),
])
session.commit()

c1 = Comment(post=p1, user=u2, content="Great post!")
c2 = Comment(post=p1, user=u1, parent=c1, content="Thanks!")
c3 = Comment(post=p1, user=u2, parent=c2, content="You're welcome!")
c4 = Comment(post=p2, user=u3, content="Nice insights")

session.add_all([c1, c2, c3, c4])
session.commit()
