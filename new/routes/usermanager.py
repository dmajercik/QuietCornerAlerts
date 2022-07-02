from fastapi import APIRouter, Request, Form, status, Body
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from new.database.models import User, Posts
from new.jwt_handler import signJWT
from new.schemas import UserSchema, UserLoginSchema

router = APIRouter()
templates = Jinja2Templates(directory="templates")


tags_metadata = [
    {
        "name": "User Manager",
        "description": "Endpoints for User CRUD"
    }
]

users = []


@router.post(
    "/user/signup",
    tags=["User Manager"],
    response_model=UserSchema,
    status_code=200,
    description="Create a user"
)
def create_user(user : UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            return False

@router.post("/user/login",
    tags=["User Manager"],
    response_model=UserLoginSchema,
    status_code=200,
    description="Login a user"
)
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return { "error" : "Invalid login details!"}
