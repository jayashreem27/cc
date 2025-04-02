from fastapi import APIRouter
from api.producer import send_log

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API is running"}

@router.post("/log/")
def log_event(level: str, message: str):
    send_log(level, message)
    return {"status": "Log sent", "level": level, "message": message}
