import logging
from pathlib import Path

try:
    logs_directory = Path(__file__).resolve().parents[2] / "data" / "logs"
    logs_directory.mkdir(parents=True, exist_ok=True)

    logs_file = logs_directory / "app.log"

    logger = logging.getLogger("slip_salary_app")
    logger.setLevel(logging.WARN)

    formatter = logging.Formatter("%(levelname)s - %(message)s")

    file_handler = logging.FileHandler(logs_file)
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
except Exception as e:
    print(f"Logging setup failed: {e}")