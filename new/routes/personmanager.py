from fastapi import APIRouter

from new import schemas

router = APIRouter()

tags_metadata = [
    {
        "name": "Person Manager",
        "description": "Endpoints to manage the CRUD of users"
    }
]

@router.get(
    "/get_person",
    tags=["Person Manager"],
    response_model=schemas.CadSchema,
    status_code=200,
    description="test"
)
async def person(self):
    data = "test"
    return data