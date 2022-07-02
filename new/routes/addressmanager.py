from fastapi import APIRouter

from new import schemas

router = APIRouter()

tags_metadata = [
    {
        "name": "Address Manager",
        "description": "Endpoints to manage the CRUD of users"
    }
]

@router.get(
    "/get_address",
    tags=["Address Manager"],
    response_model=schemas.CadSchema,
    status_code=200,
    description="test"
)
async def address(self):
    data = "test"
    return data