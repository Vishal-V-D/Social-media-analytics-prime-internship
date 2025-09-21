from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db.schema import PostHashtag, Hashtag
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

def get_related_hashtags(base_tag, min_cooccurrence=0.3):
    session = Session()
    
    base = session.query(Hashtag).filter(Hashtag.tag == base_tag).first()
    if not base:
        session.close()
        return []

    base_posts = session.query(PostHashtag.post_id).filter(PostHashtag.hashtag_id == base.hashtag_id).all()
    base_post_ids = [p.post_id for p in base_posts]
    total_base_posts = len(base_post_ids)
    if total_base_posts == 0:
        session.close()
        return []

    candidate_hashtags = session.query(
        Hashtag.tag,
        func.count(PostHashtag.post_id).label("freq")
    ).join(PostHashtag).filter(
        PostHashtag.post_id.in_(base_post_ids),
        Hashtag.tag != base_tag
    ).group_by(Hashtag.hashtag_id).all()

    filtered = [(tag, freq) for tag, freq in candidate_hashtags if freq / total_base_posts >= min_cooccurrence]
    filtered.sort(key=lambda x: x[1], reverse=True)
    session.close()
    return filtered[:3]

if __name__ == "__main__":
    for tag, freq in get_related_hashtags("#AI"):
        print(tag, freq)
