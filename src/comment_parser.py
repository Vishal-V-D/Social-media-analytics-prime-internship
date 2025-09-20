from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.schema import Comment
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)

def get_engagement_depth(comment, depth=0):
    if not comment.replies:
        return depth
    return max(get_engagement_depth(reply, depth + 1) for reply in comment.replies)

if __name__ == "__main__":
    session = Session()
    comments = session.query(Comment).all()
    for c in comments:
        depth = get_engagement_depth(c)
        print(f"Comment {c.comment_id} depth: {depth}")
    session.close()
