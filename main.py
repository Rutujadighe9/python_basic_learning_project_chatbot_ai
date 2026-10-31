
from contextlib import asynccontextmanager

from fastapi import FastAPI
    
from app.api_routes.auth_routes import router as auth_router
from app.core.database import Base, engine, test_connection
from app.models.user import User
from app.api_routes.chat_router import router as chat_router
from app.api_routes.gemini_ai_routes import router as gemini_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="User Registration API", lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(gemini_router,prefix="/api/v1")
@app.get("/")
def home():
    return {"message": "User Registration API is running"}


@app.get("/db-check")
def check_database():
    return test_connection()


@app.get("/health")
def health_check():
    return {"status": "healthy"}
