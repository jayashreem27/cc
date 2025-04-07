# File: /cc/docker1/api/routes.py
from fastapi import APIRouter, Body
from api.producer import send_log
from pydantic import BaseModel

router = APIRouter()

class LogMessage(BaseModel):
    level: str
    message: str

@router.get("/")
def root():
    return {"message": "API is running"}

@router.post("/log/")
def log_event(log: LogMessage = Body(...)):
    try:
        send_log(log.level, log.message)
        return {"status": "Log sent", "level": log.level, "message": log.message}
    except Exception as e:
        return {"error": str(e)}

