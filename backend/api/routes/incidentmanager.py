import configparser

from fastapi import APIRouter, Response

from backend.api import schemas

router = APIRouter()

tags_metadata = [
    {
        "name": "Incident Manager",
        "description": "Endpoints to manage the CRUD of incidents"
    }
]

@router.get(
    "/get_qued_incidents",
    tags=["Incident Manager"],
    response_model=schemas.CadSchema,
    status_code=200
)
async def dispatch(self):
    data = "test"
    return data

@router.get(
    "/get_all_incidents",
    tags=["Incident Manager"],
    response_model=schemas.CadSchema,
    status_code=200
)
async def dispatch(self):
    data = "test"
    return data
@router.get(
    "/get_24hr_incidents",
    tags=["Incident Manager"],
    response_model=schemas.CadSchema,
    status_code=200
)
async def dispatch(self):
    data = "test"
    return data
@router.get(
    "/get_incident",
    tags=["Incident Manager"],
    response_model=schemas.CadSchema,
    status_code=200
)
async def dispatch(self):
    data = "test"
    return data
@router.post(
    "/create_incident",
    tags=["Incident Manager"],
    response_model=schemas.CadSchema,
    status_code=200
)

async def dispatch(self):
    data = "test"
    return data

@router.post(
    "/edit_incident",
    tags=["CAD"],
    response_model=schemas.CadSchema,
    status_code=200
)
async def dispatch(self):
    data = "test"
    return data
@router.delete(
    "/delete_incident",
    tags=["Incident Manager"],
    response_model=schemas.CadSchema,
    status_code=200
)
async def dispatch(self):
    data = "test"
    return data
@router.post(
    "/update_incident",
    tags=["Incident Manager"],
    response_model=schemas.CadSchema,
    status_code=200
)
async def dispatch(self):
    data = "test"
    return data