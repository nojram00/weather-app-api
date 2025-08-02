from pydantic import BaseModel
from typing import Optional

class ForecastConditionsSchema(BaseModel):
    date: str
    place: str
    caused_by: str
    impacts: str
    weather_condition: str
    