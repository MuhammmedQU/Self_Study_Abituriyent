import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import Request

logger = logging.getLogger("lms")
logger.setLevel(logging.INFO)

log_path = Path("logs") / "error.log"
log_path.parent.mkdir(parents=True, exist_ok=True)
handler = RotatingFileHandler(log_path, maxBytes=1_048_576, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)


async def request_logging_middleware(request: Request, call_next):
    response = await call_next(request)
    logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)
    return response
