from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import Response
from loguru import logger

from src.dependencies import config

admin_router = APIRouter()
tag = ["_Admin Controller"]


@admin_router.patch("/configure", tags=tag)
async def configure(body: Any = Body(None)):
    if type(body) is not dict:
        raise HTTPException(400, "body is not dict")
    for k, v in body.items():
        config.set(k, str(v))
        logger.debug(f"Changed {k} to {v}")


@admin_router.get("/logs", tags=tag)
async def logs():
    files = [file.name for file in (Path().absolute() / "logs").glob("*.log")]
    files.sort(reverse=True)
    if len(files) == 0:
        return None
    with open(Path().absolute() / "logs" / files[0], "rb") as fin:
        return Response(
            content=fin.read(),
            media_type="text/plain"
        )
