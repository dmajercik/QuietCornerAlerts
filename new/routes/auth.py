from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from new.database.models import User, Posts

from new.schemas import UserSchema, UserLoginSchema

router = APIRouter()
templates = Jinja2Templates(directory="templates")


tags_metadata = [
    {
        "name": "Auth",
        "description": "Endpoints for User Scrum"
    }
]

@router.get(
    "/user_signup",
    tags=["Auth"],
    status_code=200,
    description="Load the News Main page",
    response_class=HTMLResponse
)
async def news(request: Request):
    posts = Posts.objects.filter(status='live')
    post_list = []
    for post in reversed(posts):
        post_list.append(
            {'title': post.title, 'body': post.body[0:500], 'username': post.username, 'created': post.created,
             'keywords': post.keywords, 'authorid': post.authorid, 'id': post.id})
        context = {'request': request, "posts": post_list}
    return templates.TemplateResponse("/news/news.html", context)