from fastapi import APIRouter
from models.wind_and_coastals import WindAndCoastalWaters
from schema.wind_and_coastal_schema import WindAndCoastalWatersSchema
from models.constants import LAST_SEVEN_DAYS, LAST_THIRTY_DAYS,  TODAY, THIRTY_DAYS_FROM_LAST_WEEK_END

router = APIRouter()

@router.get("/wind-and-coastal-waters")
def get_wind_and_coastal_waters():
    waters = WindAndCoastalWaters.objects(
        date__gte=LAST_SEVEN_DAYS,
        date__lte=TODAY,
        place__ne="",
        speed__ne="",
        direction__ne="",
        coastal_water__ne=""
    ).order_by("-date")
    result = []

    for water in waters:
        doc = water.to_mongo().to_dict()
        doc['_id'] = str(doc['_id'])
        result.append(doc)

    return result

@router.post("/wind-and-coastal-waters")
def create_wind_and_coastal_waters(water: WindAndCoastalWatersSchema):
    doc = WindAndCoastalWaters(**water.model_dump())
    doc.save()

    return { 'message': 'Wind and coastal waters created successfully' }

@router.get("/wind-and-coastal-waters/{id}")
def get_wind_and_coastal_waters_by_id(id: str):
    water = WindAndCoastalWaters.objects(id=id).first()

    if not water:
        return { 'message': 'Wind and coastal waters not found' }
    
    doc = water.to_mongo().to_dict()
    doc['_id'] = str(doc['_id'])

    return doc

@router.delete("/wind-and-coastal-waters/prune")
def delete_all_wind_and_coastal_waters():
    WindAndCoastalWaters.objects().delete()

    return { 'message': 'All wind and coastal waters deleted successfully' }


@router.delete("/wind-and-coastal-waters/cleanup-empty")
def delete_empty_wind_and_coastal_waters():
    # Delete records where any of the key fields are empty
    deleted_count = WindAndCoastalWaters.objects(
        __raw__={
            "$or": [
                {"place": ""},
                {"speed": ""},
                {"direction": ""},
                {"coastal_water": ""}
            ]
        }
    ).delete()

    return { 'message': f'Deleted {deleted_count} empty forecast conditions' }

@router.delete("/wind-and-coastal-waters/cleanup-old")
def delete_old_wind_and_coastal_waters():
    # Delete records from 7 days ago to 30 days before
    # This deletes data between LAST_THIRTY_DAYS and LAST_SEVEN_DAYS
    deleted_count = WindAndCoastalWaters.objects(
        date__gte=LAST_THIRTY_DAYS,
        date__lte=LAST_SEVEN_DAYS
    ).delete()

    return { 'message': f'Deleted {deleted_count} old forecast conditions (7-30 days ago)' }