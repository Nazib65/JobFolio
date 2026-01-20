from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.router import api_router
from app.config import settings
import certifi

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo(app)
    yield
    await disconnect_from_mongo(app)

async def connect_to_mongo(app):
    from motor.motor_asyncio import AsyncIOMotorClient
    app.mongo_client = AsyncIOMotorClient(
        settings.DATABASE_URL,
        tlsCAFile=certifi.where(),
    )
    print(settings.DATABASE_URL)
    app.mongodb = app.mongo_client.get_database(settings.DB_NAME)
    print(settings.DB_NAME)
    print("Connected to MongoDB.")

async def disconnect_from_mongo(app):
    app.mongo_client.close()
    print("MongoDB connection closed.")

app = FastAPI(lifespan=lifespan)

# Configure CORS - allow all localhost origins for development
app.add_middleware(
    CORSMiddleware,
    # Explicit allowlist (works across Starlette versions)
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    # Regex for any localhost port (handy if you run Next on a different port)
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Hello World"}