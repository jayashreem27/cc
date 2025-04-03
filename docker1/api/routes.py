from fastapi import APIRouter
from api.producer import send_log  # Ensure correct import

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API is running"}

@router.post("/log/")
def log_event(level: str, message: str):
    try:
        send_log(level, message)
        return {"status": "Log sent", "level": level, "message": message}
    except Exception as e:
        return {"error": str(e)}
