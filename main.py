
from contextlib import asynccontextmanager

from fastapi import FastAPI
    
from app.api_routes.auth_routes import router as auth_router
<<<<<<< HEAD
=======
from app.api_routes.chat_router import router as chat_router
>>>>>>> 837080ba1c9676de85cb97aa502aca34904281f6
from app.core.database import Base, engine, test_connection
from app.models.user import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="User Registration API", lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
@app.get("/")
def home():
    return {"message": "User Registration API is running"}


@app.get("/db-check")
def check_database():
    return test_connection()


@app.get("/health")
def health_check():
    return {"status": "healthy"}
