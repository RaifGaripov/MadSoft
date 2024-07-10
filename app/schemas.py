from pydantic import BaseModel, HttpUrl


class Meme(BaseModel):
    id: int
    title: str
    description: str
    image_url: HttpUrl

    class Config:
        from_attributes = True
