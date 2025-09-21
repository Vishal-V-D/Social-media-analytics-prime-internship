from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from db.schema import Hashtag, PostHashtag
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from src.cache import get_from_cache, set_cache
from src.utils import retry  

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
SessionLocal = sessionmaker(bind=engine)

@retry(max_attempts=3, delay=1, backoff=2)   
def get_trending_hashtags():
    cache_key = "trending_hashtags"
    cached = get_from_cache(cache_key)
    if cached:
        return cached

    session = SessionLocal()
    try:
        results = session.query(
            Hashtag.tag,
            func.count(PostHashtag.post_id).label("freq")
        ).join(PostHashtag).group_by(Hashtag.hashtag_id).order_by(func.count(PostHashtag.post_id).desc()).limit(5).all()
        set_cache(cache_key, results)
        return results
    finally:
        session.close()

if __name__ == "__main__":
    for tag, freq in get_trending_hashtags():
        print(tag, freq)

    for tag, freq in get_trending_hashtags():
        print(tag, freq)
