from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from app.database import engine
from app.routes.auth_routes import router as auth_router
from app.routes.ticket_routes import router as ticket_router
from app.middleware.timer import timing_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Support_desk", lifespan=lifespan)

app.middleware("http")(timing_middleware)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"])

app.include_router(auth_router)
app.include_router(ticket_router)





