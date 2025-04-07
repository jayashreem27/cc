from fastapi import APIRouter
from pydantic import BaseModel
from api.producer import send_log

router = APIRouter()

# Pydantic model for the POST body
class LogRequest(BaseModel):
    message: str

@router.get("/")
def root():
    return {"message": "API is running"}

@router.post("/log/info")
def log_info(data: LogRequest):
    send_log("info", data.message)
    return {"status": "sent", "level": "info", "message": data.message}

@router.post("/log/debug")
def log_debug(data: LogRequest):
    send_log("debug", data.message)
    return {"status": "sent", "level": "debug", "message": data.message}

@router.post("/log/error")
def log_error(data: LogRequest):
    send_log("error", data.message)
    return {"status": "sent", "level": "error", "message": data.message}

@router.post("/log/warning")
def log_warning(data: LogRequest):
    send_log("warning", data.message)
    return {"status": "sent", "level": "warning", "message": data.message}

# For custom/unspecified log levels
class CustomLogRequest(BaseModel):
    level: str
    message: str

@router.post("/log/")
def log_custom(data: CustomLogRequest):
    send_log(data.level, data.message)
    return {"status": "sent", "level": data.level, "message": data.message}
