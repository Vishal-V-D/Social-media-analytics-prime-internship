from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.schema import Base, Comment

from db_layer import get_trending_hashtags
from hashtag_engine import get_related_hashtags
from comment_parser import get_engagement_depth

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)

def analyze_comments(session):
    comments = session.query(Comment).all()
    depths = {}
    for c in comments:
        depths[c.comment_id] = get_engagement_depth(c)
    return depths

if __name__ == "__main__":
    session = Session()

    print("=== Trending Hashtags ===")
    for tag, freq in get_trending_hashtags():
        print(f"{tag}: {freq} posts")

    print("\n=== Top 3 Related Hashtags for #AI ===")
    for tag, freq in get_related_hashtags("#AI"):
        print(f"{tag}: {freq} co-occurrences")

    print("\n=== Comment Engagement Depth ===")
    depths = analyze_comments(session)
    for comment_id, depth in depths.items():
        print(f"Comment {comment_id}: Depth {depth}")

    session.close()
