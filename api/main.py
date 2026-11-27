from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database import pool
from api.routers import counterparties, transactions, users, budgets, pots, recurring_bills


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()      # startup
    yield
    await pool.close()     # shutdown


app = FastAPI(title="Finance API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://finance-app-eight-beta-54.vercel.app"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(counterparties.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(pots.router)
app.include_router(recurring_bills.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
