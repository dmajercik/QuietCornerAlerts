from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from new.database.models import User, Posts
from mongoengine.queryset.visitor import Q
import datetime
from pytz import timezone
from new.jwt_bearer import jwtBearer
from new.schemas import UserSchema, UserLoginSchema
#from database.models import User
from new import schemas
import types
router = APIRouter()
templates = Jinja2Templates(directory="templates")


tags_metadata = [
    {
        "name": "News",
        "description": "Endpoints for the News portion of the website"
    }
]

@router.get('/')
@router.get(
    "/news",
    tags=["News"],
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


@router.get(
    "/create",
    tags=["News"],
    status_code=200,
    dependencies=[Depends(jwtBearer())],
    description="Load the create article News page",
    response_class=HTMLResponse
)
async def create(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("/news/create.html", context)

@router.post(
    "/creat_post",
    tags=["News"],
    status_code=200,
    description="Post article to database",
    response_class=HTMLResponse
)
async def create_post(request: Request, title: str = Form(), keywords: str = Form(), editor1: str = Form() ):
    est = timezone('US/Eastern')
    dt = datetime.datetime.now(tz=est)
    time_str = dt.strftime('%H:%M')
    d3 = dt.strftime('%m/%d/%y')
    d4 = dt.strftime('%m/%d/%y, %H:%M:%S')
    post = Posts()
    user = "QCA001"
    print(title)
    post.title = title
    post.body = editor1
    post.username = 'QCA001'
    post.authorid = "Quiet Corner Alerts"
    post.created = d4
    keyword_list = []
    keywords = keywords.split('#')
    for word in keywords:
        stripped = word.strip()
        if stripped != '':
            keyword_list.append(stripped)
    post.keywords = keywords
    post.status = 'draft'
    print(keyword_list)
    print(editor1)
    post.save()
    context = {'request': request}
    response = RedirectResponse(url='/drafts',status_code=status.HTTP_302_FOUND)
    return response


@router.get(
    "/drafts",
    tags=["News"],
    status_code=200,
    description="Load the Drafts page",
    response_class=HTMLResponse
)
async def draft(request: Request):
    #user = User.objects.get(id=get_jwt_identity())
    posts = Posts.objects.filter((Q(status='draft') & Q(username='QCA001')))
    post_list = []
    for post in reversed(posts):
        post_list.append({'title': post.title, 'body': post.body, 'authorid': post.authorid, 'username': post.username,
                          'created': post.created, 'id': post.id, 'keywords': post.keywords})
    context = {'request': request, "posts": post_list}
    return templates.TemplateResponse("/news/news.html", context)