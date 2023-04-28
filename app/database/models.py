from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.dialects.postgresql import JSONB

from .engine import Base


class YoutubeResultModel(Base):
    __tablename__ = "youtube_result"
    id = Column(Integer, primary_key=True)
    videoId = Column(String)
    result = Column(JSONB)
    at = Column(Date)


class YoutubeCommentModel(Base):
    __tablename__ = "comment_storage"
    id = Column(Integer, primary_key=True)
    videoId = Column(String)
    comments = Column(JSONB)
