from sqlalchemy import Column, Integer, String

from app.database import Base


class Meme(Base):
    __tablename__ = 'memes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, unique=True, nullable=False)

