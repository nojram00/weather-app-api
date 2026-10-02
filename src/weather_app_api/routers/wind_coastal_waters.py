from fastapi import APIRouter
from simple_mongo_2 import SimpleMongo
from ..schema import WindAndCoastalWatersSchema
from .constants import LAST_SEVEN_DAYS, LAST_THIRTY_DAYS, MONGO_URI,  TODAY, THIRTY_DAYS_FROM_LAST_WEEK_END

router = APIRouter()

@router.get("/wind-and-coastal-waters")
def get_wind_and_coastal_waters():    
    with SimpleMongo(MONGO_URI) as client:
        waters = (client
         .database('pagasa-weather-forecast')
         .wind_and_coastal_waters
         .find({
             "date": {
                 "$gte": LAST_SEVEN_DAYS,
                 "$lte": TODAY
             },
             "place": {
                "$exists": True,
                "$ne": ""
             },
             "speed": {
                "$exists": True,
                "$ne": ""
             },
             "direction": {
                "$exists": True,
                "$ne": ""
             },
             "coastal_water": {
                "$exists": True,
                "$ne": ""
             },
         }))
    
    result = []

    for water in waters:
        doc = water
        doc['_id'] = str(doc['_id'])
        result.append(doc)

    return result

@router.post("/wind-and-coastal-waters")
def create_wind_and_coastal_waters(water: WindAndCoastalWatersSchema):
    with SimpleMongo(MONGO_URI) as client:
        inserted = (client
            .database('pagasa-weather-forecast')
            .wind_and_coastal_waters.insert_one(water.model_dump()))

    return { 'message': 'Wind and coastal waters created successfully', "inserted_id" : inserted.inserted_id }

@router.get("/wind-and-coastal-waters/{id}")
def get_wind_and_coastal_waters_by_id(id: str):
    with SimpleMongo(MONGO_URI) as client:
        water = (client
            .database('pagasa-weather-forecast')
            .wind_and_coastal_waters.find_one({
                "_id" : id
            }))

    if not water:
        return { 'message': 'Wind and coastal waters not found' }
    
    doc = water
    doc['_id'] = str(doc['_id'])

    return doc

@router.delete("/wind-and-coastal-waters/prune")
def delete_all_wind_and_coastal_waters():
    
    with SimpleMongo(MONGO_URI) as client:
        (client
        .database('pagasa-weather-forecast')
        .wind_and_coastal_waters.delete_many({}))

    return { 'message': 'All wind and coastal waters deleted successfully' }


@router.delete("/wind-and-coastal-waters/cleanup-empty")
def delete_empty_wind_and_coastal_waters():
    # Delete records where any of the key fields are empty
    
    with SimpleMongo(MONGO_URI) as client:
        deleted_count =(client
            .database('pagasa-weather-forecast')
            .wind_and_coastal_waters
            .delete_many({
                "$or": [
                    { "place" : "" },
                    {"speed": ""},
                    {"direction": ""},
                    {"coastal_water": ""}
                ]
            })).deleted_count

    return { 'message': f'Deleted {deleted_count} empty forecast conditions' }

@router.delete("/wind-and-coastal-waters/cleanup-old")
def delete_old_wind_and_coastal_waters():
    """
    - Delete records from 7 days ago to 30 days before.
    - This deletes data between LAST_THIRTY_DAYS and LAST_SEVEN_DAYS
    """
    with SimpleMongo(MONGO_URI) as client:
        deleted_count = (
            client.database("pagasa-weather-forecast")
            .wind_and_coastal_waters
            .delete_many({
                "date": {
                    "$gte": LAST_THIRTY_DAYS,
                    "$lte": LAST_SEVEN_DAYS
                }
            })
        ).deleted_count

    return { 'message': f'Deleted {deleted_count} old forecast conditions (7-30 days ago)' }