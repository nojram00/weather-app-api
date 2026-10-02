from pydantic import BaseModel
from typing import Optional

class WindAndCoastalWatersSchema(BaseModel):
    date: str
    place: str
    speed: str
    direction: str
    coastal_water: str
    