
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

from db.schema import Base, Comment
from src.db_layer import get_trending_hashtags
from src.hashtag_engine import get_related_hashtags
from src.comment_parser import get_engagement_depth

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)

app = FastAPI(title="Social Media Analytics API", version="1.0")

@app.get("/trending-hashtags")
def trending_hashtags():
    try:
        results = get_trending_hashtags()
        return [{"tag": tag, "frequency": freq} for tag, freq in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/related-hashtags/{base_tag}")
def related_hashtags(base_tag: str):
    try:
        results = get_related_hashtags(base_tag)
        return [{"tag": tag, "co_occurrences": freq} for tag, freq in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/comment-engagement")
def comment_engagement():
    session = Session()
    try:
        comments = session.query(Comment).all()
        result = []
        for c in comments:
            result.append({
                "comment_id": c.comment_id,
                "content": c.content,
                "depth": get_engagement_depth(c),
                "replies": [r.comment_id for r in c.replies] 
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
