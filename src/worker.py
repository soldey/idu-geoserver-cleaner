import asyncio
import os
import shutil
from datetime import datetime
from pathlib import Path

from loguru import logger

from src.dependencies import config, redis_service


async def delete_layer(layer: str):
    try:
        shutil.rmtree(
            Path().absolute() / config.get("GEOSERVER_WORKSPACES_PATH") / config.get("GEOSERVER_WORKSPACE") / layer
        )
    except FileNotFoundError as e:
        logger.info(e)


async def main_worker_task():
    last_ping = datetime.now()
    ping_freq = 300

    pid = os.getpid()
    while True:
        if (datetime.now() - last_ping).total_seconds() > ping_freq:
            logger.info(f"{pid}: ping")
            last_ping = datetime.now()

        if "clear-task" in [task.get_name() for task in asyncio.all_tasks()]:
            await asyncio.sleep(2)
            continue

        msg = await redis_service.get_message("clear_geoserver_layer")
        if msg:
            asyncio.create_task(delete_layer(msg), name="clear-task")
        await asyncio.sleep(2)
