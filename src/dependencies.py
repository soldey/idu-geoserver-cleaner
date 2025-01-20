import sys
from datetime import datetime

from iduconfig import Config
from iduredis import RedisManager
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}.{function}</cyan> - "
    "<level>{message}</level>",
    level="INFO",
    colorize=True,
)
config = Config()
logger.add(
    f"{config.get('LOGS_DIR')}/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
    format="<green>{time:MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}.{function}</cyan> - "
    "<level>{message}</level>",
)

redis_service = RedisManager(config)
