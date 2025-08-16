from fastapi import APIRouter
from models.forecast_conditions import ForecastConditions
from schema.weather_forecast_schema import ForecastConditionsSchema
from models.constants import LAST_SEVEN_DAYS, LAST_THIRTY_DAYS,  TODAY, THIRTY_DAYS_FROM_LAST_WEEK_END


router = APIRouter()


@router.get("/forecast-conditions")
def get_forecast_condition():
    # Filter out documents with empty string values for key fields
    forecasts = ForecastConditions.objects(
        date__gte=LAST_SEVEN_DAYS,
        date__lte=TODAY,
        caused_by__ne="",
        impacts__ne="", 
        place__ne="",
        weather_condition__ne=""
    ).order_by("-date")
    result = []

    for forecast in forecasts:
        doc = forecast.to_mongo().to_dict()
        doc['_id'] = str(doc['_id'])
        result.append(doc)

    return result

@router.post("/forecast-conditions")
def create_forecast_condition(forecast: ForecastConditionsSchema):
    doc = ForecastConditions(**forecast.model_dump())
    doc.save()

    return { 'message': 'Forecast condition created successfully' }

@router.get("/forecast-conditions/{id}")
def get_forecast_condition_by_id(id: str):
    forecast = ForecastConditions.objects(id=id).first()

    if not forecast:
        return { 'message': 'Forecast condition not found' }

    doc = forecast.to_mongo().to_dict()
    doc['_id'] = str(doc['_id'])

    return doc

@router.delete("/forecast-conditions/prune")
def delete_all_forecast_conditions():
    ForecastConditions.objects().delete()

    return { 'message': 'All forecast conditions deleted successfully' }

@router.delete("/forecast-conditions/cleanup-empty")
def delete_empty_forecast_conditions():
    # Delete records where any of the key fields are empty
    deleted_count = ForecastConditions.objects(
        __raw__={
            "$or": [
                {"caused_by": ""},
                {"impacts": ""},
                {"place": ""},
                {"weather_condition": ""}
            ]
        }
    ).delete()

    return { 'message': f'Deleted {deleted_count} empty forecast conditions' }

@router.delete("/forecast-conditions/cleanup-old")
def delete_old_forecast_conditions():
    # Delete records from 7 days ago to 30 days before
    # This deletes data between LAST_THIRTY_DAYS and LAST_SEVEN_DAYS
    deleted_count = ForecastConditions.objects(
        date__gte=LAST_THIRTY_DAYS,
        date__lte=LAST_SEVEN_DAYS
    ).delete()

    return { 'message': f'Deleted {deleted_count} old forecast conditions (7-30 days ago)' }

