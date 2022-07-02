from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#from database.models import User
from new import schemas
router = APIRouter()

templates = Jinja2Templates(directory="templates")


tags_metadata = [
    {
        "name": "Website",
        "description": "Endpoints for the website"
    }
]


@router.get(
    "/about",
    tags=["Website"],
    status_code=200,
    description="Load the About Us / Contact Us page",
    response_class=HTMLResponse
)
async def about(request: Request):
    context = {'request':request}
    return templates.TemplateResponse("/website/about.html", context)


@router.get(
    "/firecategories",
    tags=["Website"],
    status_code=200,
    description="Load the Fire Categories page",
    response_class=HTMLResponse
)
async def firecategories(request: Request):
    context = {'request':request}
    return templates.TemplateResponse("/website/firecategories.html", context)

@router.get(
    "/policecategories",
    tags=["Website"],
    status_code=200,
    description="Load the Police Categories page",
    response_class=HTMLResponse
)
async def policecategories(request: Request):
    context = {'request':request}
    return templates.TemplateResponse("/website/policecategories.html", context)

@router.get(
    "/weathercategories",
    tags=["Website"],
    status_code=200,
    description="Load the Weather Categories page",
    response_class=HTMLResponse
)
async def weathercategories(request: Request):
    context = {'request':request}
    return templates.TemplateResponse("/website/weathercategories.html", context)

@router.get(
    "/abbreviations",
    tags=["Website"],
    status_code=200,
    description="Load the abbreviations page",
    response_class=HTMLResponse
)
async def abbreviations(request: Request):
    context = {'request':request}
    return templates.TemplateResponse("/website/abbreviations.html", context)
