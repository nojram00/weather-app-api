from fastapi import APIRouter
from models.wind_and_coastals import WindAndCoastalWaters
from schema.wind_and_coastal_schema import WindAndCoastalWatersSchema

router = APIRouter()

@router.get("/wind-and-coastal-waters")
def get_wind_and_coastal_waters():
    waters = WindAndCoastalWaters.objects()
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