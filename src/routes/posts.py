from typing import Optional

from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, status, Query, Path, HTTPException, Form
from sqlalchemy.orm import Session
# from fastapi_limiter.depends import RateLimiter

from src.schemas import PostModel, PostResponse
from src.services.auth import auth_service
from src.database.db import get_db
from src.database.models import User, Role
from src.repository import posts as rep_posts

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[PostResponse])
async def get_posts(limit: int = Query(10, le=300), offset: int = 0, db: Session = Depends(get_db)):
    posts = await rep_posts.get_posts(limit, offset, db)
    return posts


# @router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
# async def create_post(body: PostModel, db: Session = Depends(get_db)):
#
#     post = await rep_posts.create(body, db)
#     return post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
        # використовується Form з FastAPI для передачі дані як 'application/x-www-form-urlencoded'
        title: str = Form(...),
        post: str = Form(...),
        image_url: Optional[str] = Form('https://i.pinimg.com/564x/95/9f/c0/959fc04bbd062c84ed00b28d2c3d1467.jpg'),
        db: Session = Depends(get_db)):
    post_data = PostModel(title=title, post=post, image_url=image_url)
    post = await rep_posts.create(post_data, db)
    if post:
        return RedirectResponse(url="/", status_code=303)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(body: PostModel, post_id: int = Path(ge=0), db: Session = Depends(get_db),
                      _: User = Depends(auth_service.get_current_user)):
    post = await rep_posts.update(post_id, body, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return post


@router.patch("/{post_id}/like", response_model=PostResponse)
async def like_post(post_id: int = Path(ge=0), db: Session = Depends(get_db)):
    post = await rep_posts.update_like_post(post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return post


@router.patch("/{post_id}/dislike", response_model=PostResponse)
async def dislike_post(post_id: int = Path(ge=0), db: Session = Depends(get_db)):
    post = await rep_posts.update_dislike_post(post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return post


@router.delete("/{post_id}", response_model=PostResponse)
async def delete_post(post_id: int = Path(ge=0), db: Session = Depends(get_db),
                      _: User = Depends(auth_service.get_current_user)):
    post = await rep_posts.remove(post_id, db)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found!")
    return post
