from fastapi import FastAPI, Path, Query, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import requests
from starlette.middleware.cors import CORSMiddleware

from src.routes import posts, users, auth
from src.routes.posts import get_posts, create_post

app = FastAPI()
app.include_router(posts.router, prefix="/api")
app.include_router(users.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

templates = Jinja2Templates(directory='templates')
# BASE_DIR = Path(__file__).parent
# app.mount('/static', StaticFiles(directory=BASE_DIR / 'static'), name='static')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.25.0.1:5500', "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, form=Depends(get_posts)):
    return templates.TemplateResponse('index.html', {'request': request, 'posts': form})


@app.get("/form_post", response_class=HTMLResponse)
async def form_post(request: Request):
    return templates.TemplateResponse('form_post.html', {'request': request})


@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse('signup.html', {'request': request})


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    return templates.TemplateResponse('logout.html', {'request': request})
