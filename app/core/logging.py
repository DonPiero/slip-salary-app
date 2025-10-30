import logging
from pathlib import Path

try:
    LOG_DIR = Path("/data/logs")
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    LOG_FILE = LOG_DIR / "app.log"

    logger = logging.getLogger("slip_salary_app")
    logger.setLevel(logging.WARN)

    formatter = logging.Formatter("%(levelname)s - %(message)s")

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
except Exception as e:
    print(f"Logging setup failed: {e}")