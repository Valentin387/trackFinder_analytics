from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

# Define ObjectId as a valid type for Pydantic to handle
class ObjectIdField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if isinstance(v, ObjectId):
            return str(v)
        return v

class Song(BaseModel):
    id: ObjectIdField = Field(..., alias="_id")
    name: Optional[str] = None
    title: str
    sub_title: Optional[str] = None
    bitrate: int
    commentaries: str
    main_artist: str
    collaborators: str
    album_artist: str
    album: str
    year: str
    track_number: str
    genre: str
    duration: int