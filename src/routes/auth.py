from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status, Security, Request, BackgroundTasks, Form
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from src.database.db import get_db
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.random_avatars import random_avatar

# from src.services.email import send_email

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        avatar: Optional[str] = Form(random_avatar()),
        db: Session = Depends(get_db)
):
    exist_user = await repository_users.get_user_by_email(email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")

    hashed_password = auth_service.get_password_hash(password)
    user_data = UserModel(username=username, email=email, password=hashed_password, avatar=avatar)
    new_user = await repository_users.create_user(user_data, db)
    # background_tasks.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    if new_user:
        return RedirectResponse(url="/", status_code=303)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="registration error")


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_username(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    # if not user.confirmed:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# @router.get('/confirmed_email/{token}')
# async def confirmed_email(token: str, db: Session = Depends(get_db)):
#
#     email = await auth_service.get_email_from_token(token)
#     user = await repository_users.get_user_by_email(email, db)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
#     if user.confirmed:
#         return {"message": "Your email is already confirmed"}
#     await repository_users.confirmed_email(email, db)
#     return {"message": "Email confirmed"}
#
#
# @router.post('/request_email')
# async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
#                         db: Session = Depends(get_db)):
#
#     user = await repository_users.get_user_by_email(body.email, db)
#
#     if user.confirmed:
#         return {"message": "Your email is already confirmed"}
#     if user:
#         background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
#     return {"message": "Check your email for confirmation."}
