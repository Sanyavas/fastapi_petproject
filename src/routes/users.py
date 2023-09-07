from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from src.schemas import UserResponse
from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users


router = APIRouter(prefix="/users", tags=["users"])

