from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db.schema import User, Post, Hashtag, PostHashtag, Comment

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

def get_trending_hashtags():
    session = Session()
    results = session.query(
        Hashtag.tag,
        func.count(PostHashtag.post_id).label("freq")
    ).join(PostHashtag).group_by(Hashtag.hashtag_id).order_by(func.count(PostHashtag.post_id).desc()).limit(5).all()
    session.close()
    return results

if __name__ == "__main__":
    for tag, freq in get_trending_hashtags():
        print(tag, freq)
