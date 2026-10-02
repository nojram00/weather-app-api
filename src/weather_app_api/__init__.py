from .routers import wind_coastal_waters, weather_forecast
from .schema import WindAndCoastalWatersSchema, ForecastConditionsSchema

__all__ = [
    'wind_coastal_waters',
    'weather_forecast',
    'WindAndCoastalWatersSchema',
    'ForecastConditionsSchema'
]