from fastapi import APIRouter

from new import schemas

router = APIRouter()

tags_metadata = [
    {
        "name": "CAD",
        "description": "Endpoints supporting the CAD page"
    }
]


@router.get(
    "/connect",
    tags=["CAD"],
    response_model=schemas.CadSchema,
    status_code=200
)

async def connect():
    return

