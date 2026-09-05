from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Parking Lot API")

app.include_router(router)
