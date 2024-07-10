import httpx

from fastapi import FastAPI, UploadFile, Depends, HTTPException, Query

from typing import List
from typing_extensions import Annotated

from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas
from app.database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

API_KEY = "Gx7xHqn1U5YqlhTQO6KnNmsf9UzWiE6M"


@app.get("/memes", response_model=List[schemas.Meme], description="List all memes")
def get_memes(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    db_memes = crud.get_memes(db, skip=skip, limit=limit)
    return db_memes


@app.get("/memes/{meme_id}", response_model=schemas.Meme, description="Get meme by id")
def get_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.get_meme_by_id(db, meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail=f"Meme with id: {meme_id} not found")
    return db_meme

@app.post("/memes", response_model=schemas.Meme, description="Create meme with title, description and image")
async def create_meme(
        title: Annotated[str, Query(description="Title of meme", min_length=3, max_length=100)],
        description: Annotated[str, Query(description="Description of meme", min_length=3, max_length=500)],
        image: UploadFile,
        db: Session = Depends(get_db)):
    db_meme = crud.get_meme_by_title(db, title)
    if db_meme:
        raise HTTPException(status_code=400, detail=f"Meme with this title: {title} already exists")

    async with httpx.AsyncClient() as client:
        files = {'image': (image.filename, image.file, image.content_type)}
        params = {"title": title}
        headers = {"access_token": API_KEY}
        response = await client.post("http://private_api:8000/memes/", params=params, headers=headers, files=files)
        if response.status_code == 200:
            image_url = response.json().get("image_url")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

    return crud.create_meme(db, title, description, image_url)


@app.put("/memes/{meme_id}", response_model=schemas.Meme,
         description="Update meme with new: title, description and image")
async def update_meme(meme_id: int,
                      title: Annotated[str, Query(description="New title of meme", min_length=3, max_length=100)],
                      description: Annotated[
                          str, Query(description="New description of meme", min_length=3, max_length=500)],
                      image: UploadFile,
                      db: Session = Depends(get_db)):
    db_meme = crud.get_meme_by_id(db, meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail=f"Meme with id: {meme_id} not found")

    async with httpx.AsyncClient() as client:
        title_of_image = db_meme.image_url.split("/")[-1]
        files = {'image': (image.filename, image.file, image.content_type)}
        headers = {"access_token": API_KEY}
        params = {"new_title": title, "old_title": title_of_image}
        response = await client.put("http://private_api:8000/memes/", params=params, headers=headers, files=files)
        if response.status_code == 200:
            image_url = response.json().get("image_url")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

    return crud.update_meme(db, title, description, image_url, db_meme)


@app.delete("/memes/{meme_id}", response_model=schemas.Meme, description="Delete meme")
async def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.delete_meme(db, meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail=f"Meme with id: {meme_id} not found")

    async with httpx.AsyncClient() as client:
        title_of_image = db_meme.image_url.split("/")[-1]
        headers = {"access_token": API_KEY}
        params = {"title": title_of_image}
        response = await client.delete("http://private_api:8000/memes/", params=params, headers=headers)

    return db_meme
