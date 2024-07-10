import pytest
import httpx

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base
from app.models import Meme

POSTGRES_LOGIN = "postgres"
POSTGRES_PASSWORD = "postgres"
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@test_db/test_memes"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    # Setup test data
    db = TestingSessionLocal()
    db.add_all([
        Meme(title="Meme 1", description="Description 1", image_url="http://example.com/meme1"),
        Meme(title="Meme 2", description="Description 2", image_url="http://example.com/meme2"),
        Meme(title="Meme 3", description="Description 3", image_url="http://example.com/meme3"),
        Meme(title="Meme 4", description="Description 4", image_url="http://example.com/meme4"),
        Meme(title="Meme 5", description="Description 5", image_url="http://example.com/meme5")
    ])
    db.commit()
    yield
    db.close()
    # Clear the data after each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_get_memes(setup_database):
    response = client.get("/memes?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_meme_by_id(setup_database):
    response = client.get("/memes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Meme 1"
    assert data["description"] == "Description 1"
    assert data["image_url"] == "http://example.com/meme1"


def test_create_meme(mocker, setup_database):
    meme_data = {
        "title": "Meme 6",
        "description": "Description 6",
    }
    mocker.patch("httpx.AsyncClient.post", return_value=httpx.Response(
        status_code=200, json={"image_url": "http://example.com/meme6"}))

    response = client.post(url="/memes",
                           params=meme_data,
                           files={"image": ("filename", open("tests/test_image.jpg", "rb"), "image/jpg")})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Meme 6"
    assert data["description"] == "Description 6"


def test_update_meme(mocker, setup_database):
    meme_data = {
        "title": "Updated Meme 1",
        "description": "Updated Description 1",
    }
    mocker.patch("httpx.AsyncClient.put", return_value=httpx.Response(
        status_code=200, json={"image_url": "http://example.com/updated_meme1"}))

    response = client.put(url="/memes/1",
                          params=meme_data,
                          files={"image": ("filename", open("tests/test_image.jpeg", "rb"), "image/jpeg")})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Meme 1"
    assert data["description"] == "Updated Description 1"


def test_delete_meme(mocker, setup_database):
    mocker.patch("httpx.AsyncClient.delete", return_value=httpx.Response(status_code=200))
    response = client.delete("/memes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Meme 1"
    response = client.get("/memes/1")
    assert response.status_code == 404
