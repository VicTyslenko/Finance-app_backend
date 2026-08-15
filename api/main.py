from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database import pool
from api.routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()      # startup
    yield
    await pool.close()     # shutdown


app = FastAPI(title="Finance API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
