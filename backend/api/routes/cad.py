import configparser

from fastapi import APIRouter, Response

from backend.api import schemas

router = APIRouter()
'''
tags_metadata = [
    {
        "name": "CAD",
        "description": "Endpoints supporting the CAD page"
    }
]


router.get(
    "/dispatch",
    tags=["CAD"],
    response_model=schemas.CadSchema,
    status_code=200
)


async def dispatch():
    return
'''
