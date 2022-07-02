from typing import Any, Dict, List, Optional, Union

import pydantic
from pydantic.fields import Field
from pydantic import EmailStr


class CadSchema(pydantic.BaseModel):
    test: str

'''
class UserSchema(pydantic.BaseModel):
    email: str
    password: str
    password2: str
    salt: str
    permission: str
    name: str
    dispatcher: str
    lastconnection: str
'''

class UserSchema(pydantic.BaseModel):
    fullname : str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)


class UserLoginSchema(pydantic.BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)


class PostSchema(pydantic.BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)

