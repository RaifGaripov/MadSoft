import os

from fastapi import FastAPI, UploadFile, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader

from minio import Minio
from minio.error import S3Error


app = FastAPI()

API_KEY = "Gx7xHqn1U5YqlhTQO6KnNmsf9UzWiE6M"
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
ENDPOINT = "127.0.0.1:9000"
client = Minio(
    "s3:9000",
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False
)

BUCKET_NAME = "memes"
found = client.bucket_exists(BUCKET_NAME)
if not found:
    client.make_bucket(BUCKET_NAME)


def get_api_key(access_token: str = Depends(api_key_header)):
    if access_token != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return access_token


def make_title_with_extension(filename, title):
    file_extension = filename.split(".")[-1]
    title = "".join([title, ".", file_extension])
    return title


@app.post("/memes/")
def save_meme_image(image: UploadFile, title: str, access_token: str = Depends(get_api_key)):
    file_size = os.fstat(image.file.fileno()).st_size
    title = make_title_with_extension(image.filename, title)
    try:
        client.put_object(BUCKET_NAME, title, image.file, file_size)
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"File with title: {title} already in S3 storage \n {e.message}")

    image_url = f"https://{ENDPOINT}/{BUCKET_NAME}/{title}"
    return {"image_url": image_url}


@app.put("/memes/")
def update_meme_image(image: UploadFile, new_title: str, old_title: str, access_token: str = Depends(get_api_key)):
    new_title = make_title_with_extension(image.filename, new_title)
    file_size = os.fstat(image.file.fileno()).st_size

    try:
        client.put_object(BUCKET_NAME, new_title, image.file, file_size)
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"File with title: {new_title} already in S3 storage \n {e.message}")

    try:
        client.remove_object(BUCKET_NAME, old_title)
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"No such file with title: {old_title} in S3 storage \n {e.message}")

    image_url = f"https://{ENDPOINT}/{BUCKET_NAME}/{new_title}"
    return {"image_url": image_url}


@app.delete("/memes/")
def delete_meme_image(title: str, access_token: str = Depends(get_api_key)):
    try:
        client.remove_object(BUCKET_NAME, title)
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"No such file with title: {title} in S3 storage \n {e.message}")
