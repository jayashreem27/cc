from fastapi import FastAPI
from api.routes import router  # Ensure correct import

app = FastAPI(title="Log API")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
