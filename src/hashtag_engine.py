from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db.schema import PostHashtag, Hashtag

from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)

def get_related_hashtags(base_tag):
    session = Session()
    base = session.query(Hashtag).filter(Hashtag.tag == base_tag).first()
    if not base:
        return []
    posts = session.query(PostHashtag.post_id).filter(PostHashtag.hashtag_id == base.hashtag_id).all()
    post_ids = [p.post_id for p in posts]
    if not post_ids:
        return []
    results = session.query(
        Hashtag.tag,
        func.count(PostHashtag.post_id).label("freq")
    ).join(PostHashtag).filter(PostHashtag.post_id.in_(post_ids), Hashtag.tag != base_tag).group_by(Hashtag.hashtag_id).order_by(func.count(PostHashtag.post_id).desc()).limit(3).all()
    session.close()
    return results

if __name__ == "__main__":
    for tag, freq in get_related_hashtags("#AI"):
        print(tag, freq)
