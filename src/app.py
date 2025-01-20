import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.admin_controller import admin_router
from src.worker import main_worker_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(main_worker_task(), name="main-worker-task")
    yield


app = FastAPI(
    root_path="/api",
    version="1.0.0",
    lifespan=lifespan
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router, prefix="/admin")
