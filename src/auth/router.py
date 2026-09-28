from fastapi import APIRouter, Response
from auth import schemas


router = APIRouter(prefix="/auth", tags=['Authentication'])