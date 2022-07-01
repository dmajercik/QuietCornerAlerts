import configparser
import logging

from fastapi import APIRouter, Response

from database.models import User
from backend.api import schemas

router = APIRouter()

tags_metadata = [
    {
        "name": "User Manager",
        "description": "Endpoints to manage the CRUD of users"
    }
]


@router.get(
    "/get_user/{user_id}",
    tags=["User Manager"],
    response_model=schemas.UserSchema,
    status_code=200,
    description="Return a single users information"
)
async def get_user(user_id):
    data = "test"
    return data

@router.get(
    "/get_all_users",
    tags=["User Manager"],
    response_model=schemas.UserSchema,
    status_code=200,
    description="Return all users information"
)
async def get_all_users():
    data = "test"
    return data

@router.post(
    "/create_user",
    tags=["User Manager"],
    response_model=schemas.UserSchema,
    status_code=200,
    description="Create a user"
)
async def create_user():
    data = "test"
    return data


@router.delete(
    "/delete_user",
    tags=["User Manager"],
    response_model=schemas.UserSchema,
    status_code=200,
    description="Delete a user"
)
async def delete_user():
    data = "test"
    return data

@router.put(
    "/update_user",
    tags=["User Manager"],
    response_model=schemas.UserSchema,
    status_code=200,
    description="Update a users information"
)
async def update_user():
    data = "test"
    return data