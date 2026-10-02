from fastapi import APIRouter
from .constants import LAST_SEVEN_DAYS, LAST_THIRTY_DAYS, MONGO_URI,  TODAY, THIRTY_DAYS_FROM_LAST_WEEK_END
from simple_mongo_2 import SimpleMongo
from ..schema import ForecastConditionsSchema

router = APIRouter()

@router.get("/forecast-conditions")
def get_forecast_condition():
    with SimpleMongo(MONGO_URI) as client:
        # Filter out documents with empty string values for key fields
        forecasts = client.database('pagasa-weather-forecast').forecast_conditions.find({
            "date": {
                "$gte": LAST_SEVEN_DAYS,
                "$lte": TODAY
            },
            "caused_by": {
                "$exists": True,
                "$ne": ""
            },
            "impacts": {
                "$exists": True,
                "$ne": ""
            },
            "place": {
                "$exists": True,
                "$ne": ""
            },
            "weather_condition": {
                "$exists": True,
                "$ne": ""
            },
        }, {
            "_id" : 0
        }).sort({
            "date": -1
        })
        result = []

    for forecast in forecasts:
        doc = forecast
        doc['_id'] = str(doc['_id'])
        result.append(doc)

    return result

@router.post("/forecast-conditions")
def create_forecast_condition(forecast: ForecastConditionsSchema):
    with SimpleMongo(MONGO_URI) as client:
        inserted = (client.database("pagasa-weather-forecast")
         .forecast_conditions.insert_one(forecast.model_dump()))

    return { 'message': 'Forecast condition created successfully', "id" : inserted.inserted_id }

@router.get("/forecast-conditions/{id}")
def get_forecast_condition_by_id(id: str):
    with SimpleMongo(MONGO_URI) as client:
        forecast = (client.database('pagasa-weather-forecast')
                    .forecast_conditions
                    .find_one({ "_id": id }))

    if not forecast:
        return { 'message': 'Forecast condition not found' }

    doc = forecast
    doc['_id'] = str(doc.get('_id'))

    return doc

@router.delete("/forecast-conditions/prune")
def delete_all_forecast_conditions():
    with SimpleMongo(MONGO_URI) as client:
        (client.database('pagasa-weather-forecast')
                    .forecast_conditions
                    .delete_many({}))

    return { 'message': 'All forecast conditions deleted successfully' }

@router.delete("/forecast-conditions/cleanup-empty")
def delete_empty_forecast_conditions():
    """
    - Delete records where any of the key fields are empty
    """
    with SimpleMongo(MONGO_URI) as client:
        deleted_count =(client
                        .database('pagasa-weather-forecast')
                        .forecast_conditions
                        .delete_many({
                            "$or": [
                                { "caused_by" : "" },
                                {"impacts": ""},
                                {"place": ""},
                                {"weather_condition": ""}
                            ]
                        })).deleted_count

    return { 'message': f'Deleted {deleted_count} empty forecast conditions' }

@router.delete("/forecast-conditions/cleanup-old")
def delete_old_forecast_conditions():
    """
    - Delete records from 7 days ago to 30 days before.
    - This deletes data between LAST_THIRTY_DAYS and LAST_SEVEN_DAYS
    """
    with SimpleMongo(MONGO_URI) as client:
        deleted_count = (
            client.database("pagasa-weather-forecast")
            .forecast_conditions
            .delete_many({
                "date": {
                    "$gte": LAST_THIRTY_DAYS,
                    "$lte": LAST_SEVEN_DAYS
                }
            })
        ).deleted_count
    
    return { 'message': f'Deleted {deleted_count} old forecast conditions (7-30 days ago)' }

