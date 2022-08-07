from fastapi import APIRouter, Request, Form, status, Body, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from new.database.models import User, Posts
from new.newauth import AuthHandler
import boto3
from fastapi_cognito import CognitoToken, CognitoAuth, CognitoSettings

router = APIRouter()
templates = Jinja2Templates(directory="templates")


tags_metadata = [
    {
        "name": "User Manager",
        "description": "Endpoints for User CRUD"
    }
]

from pydantic import BaseSettings

class Settings(BaseSettings):
    check_expiration = True
    jwt_header_prefix = "Bearer"
    jwt_header_name = "Authorization"
    userpools = {
        "us": {
            "region": "us-east-1",
            "userpool_id": "us-east-1_Hnp8bwD9l",
            "app_client_id": "3nkbc749jbok1ntbt1b46occ8u"
        },
    }

settings = Settings()

auth_handler = AuthHandler()
users = []
cognito_us = CognitoAuth(settings=CognitoSettings.from_global_settings(settings), userpool_name="us")

@router.post(
    "/user/signup",
    tags=["User Manager"],
    status_code=201,
    description="Create a user"
)
def create_user(first_name: str = Form(), last_name: str = Form(), email: str = Form(), phone_number: str = Form(), password: str = Form()):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    print(str(f'+1{phone_number}'))
    username = str(f'{first_name[0]}{last_name}')
    response = client.sign_up(ClientId='3nkbc749jbok1ntbt1b46occ8u',Username=username,Password=password,
                              UserAttributes=[
                                  {'Name': 'given_name',
                                    'Value': first_name},
                                  {'Name': 'family_name',
                                      'Value': last_name},
                                  {'Name': 'email',
                                      'Value': email},
                                  {'Name': 'phone_number',
                                   'Value': str(f'+1{phone_number}')}
                              ])
    print(response)
    return RedirectResponse(url=f'/user/confirm/{username}' , status_code=status.HTTP_302_FOUND)

@router.get("/signuppage",
    tags=["User Manager"],
    status_code=200,
    description="Load signup page"
)
def user_signuppage(request: Request):
        context = {'request': request}
        return templates.TemplateResponse("/auth/signup.html", context)

@router.get(
    "/user/confirm/{username}",
    tags=["User Manager"],
    status_code=201,
    description="Create a user"
)
def confirm_user(username, request: Request):
    print(username)
    context = {'request': request, "username": username}
    return templates.TemplateResponse("/auth/confirm.html", context)

@router.post(
    "/user/send_confirmation/{username}",
    tags=["User Manager"],
    status_code=201,
    description="Create a user"
)
def send_confirmation(username, confirmation_code: str = Form()):
    print(username)
    print(confirmation_code)
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.confirm_sign_up(ClientId='3nkbc749jbok1ntbt1b46occ8u',Username=username, ConfirmationCode=confirmation_code)
    print(response)
    return RedirectResponse(url='/news', status_code=status.HTTP_302_FOUND)

@router.get(
    "/user/test",
    tags=["User Manager"],
    status_code=201,
    description="Create a user"
)
def user_test(auth: CognitoToken = Depends(cognito_us.auth_required)):
    print('Good Test')
    return RedirectResponse(url='/news', status_code=status.HTTP_302_FOUND)

@router.get(
    "/user/auth",
    tags=["User Manager"],
    status_code=201,
    description="Create a user"
)
def auth(username, password):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.initiate_auth(ClientId='3nkbc749jbok1ntbt1b46occ8u', AuthFlow='USER_PASSWORD_AUTH', AuthParameters={
        'USERNAME': username,
        'PASSWORD': password
    })
    return response

@router.get(
    "/user/login/",
    tags=["User Manager"],
    status_code=201,
    description="Create a user"
)
def login(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("/auth/login.html", context)


@router.post(
    "/user/process_login/",
    tags=["User Manager"],
    status_code=201,
    description="Create a user"
)
def process_login(username: str = Form(), password: str = Form()):
    authentication = auth(username, password)
    response = authentication['AuthenticationResult']['AccessToken']
    print(response)
    return RedirectResponse(url='/news', headers=response, status_code=status.HTTP_302_FOUND)

'''
@router.post("/user/login",
    tags=["User Manager"],
    status_code=200,
    description="Login a user"
)
def user_login():
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return {'token': token}
    try:
        user = User.objects.get(email=str.lower(email))
        print('exists')
    except:
        context = {'request': request}
        return templates.TemplateResponse("/auth/login.html", context)
    try:
        print(password)
        user.check_password(password)
        print(password)
        users.append(email)
        signJWT(email)
        context = {'request': request}
        return RedirectResponse(url='/news',status_code=status.HTTP_302_FOUND)
    except:
        print("login failed")
        context = {'request': request}
        return templates.TemplateResponse("/auth/login.html", context)
    '''