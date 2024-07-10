from sqlalchemy.orm import Session

from app import models


def get_meme_by_id(db: Session, meme_id: int):
    return db.query(models.Meme).filter(models.Meme.id == meme_id).first()


def get_meme_by_title(db: Session, title: str):
    return db.query(models.Meme).filter(models.Meme.title == title).first()


def get_memes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Meme).offset(skip).limit(limit).all()


def create_meme(db: Session, title: str, description: str, image_url: str):
    db_meme = models.Meme(title=title, description=description, image_url=image_url)
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme


def update_meme(db: Session, title: str, description: str, image_url: str, db_meme: models.Meme):
    db_meme.title = title
    db_meme.description = description
    db_meme.image_url = image_url
    db.commit()
    return db_meme


def delete_meme(db: Session, meme_id: int):
    db_meme = get_meme_by_id(db, meme_id)
    if db_meme:
        db.delete(db_meme)
        db.commit()
    return db_meme
