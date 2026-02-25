import logging
import sys
from services.core.config import settings

def setup_logging():
    logging.basicConfig(
        level=logging.INFO if not settings.DEBUG else logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    # Silence chatty libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

logger = logging.getLogger(settings.APP_NAME)
setup_logging()
