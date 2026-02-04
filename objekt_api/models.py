from pydantic import BaseModel, Field
from typing import List

class Slug(BaseModel):
    slugId: str = Field(alias='id')
    createdAt: str 
    slugString: str = Field(alias='slug')
    collectionId: str
    season: str 
    member: str 
    artist: str 
    collectionNo: str 
    className: str = Field(alias='class') 
    frontImage: str 
    backImage: str 
    backgroundColor: str 
    textColor: str 
    onOffline: str 
    bandImageUrl: str | None=None

class Collection(BaseModel):
    collections: List[Slug]

class Metadata(BaseModel):
    total: int
    spin: int
    transferable: int
