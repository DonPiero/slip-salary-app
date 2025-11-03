import json
from datetime import datetime
from pathlib import Path

from app.core.loging import logger

IDEMPOTENCY_FILE = Path(__file__).resolve().parents[2] / "data" / "idempotency" /"idempotency.json"

def save_checker():
    try:
        IDEMPOTENCY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(IDEMPOTENCY_FILE, "w", encoding="utf-8") as f:
            json.dump(list(idempotency_checker), f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save idempotency checker: {e}")

def load_checker() -> set[str]:
    try:
        if not IDEMPOTENCY_FILE.exists():
            return set()
        with open(IDEMPOTENCY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data)
    except Exception as e:
        logger.error(f"Failed to load idempotency checker: {e}")
        return set()

idempotency_checker: set[str] = load_checker()

def check_duplicate(manager_id: int, file_type: str, action: str) -> bool:
    now = datetime.now()
    key = f"{manager_id}_{action}_{file_type}_{now.year}_{now.month:02d}"
    if key in idempotency_checker:
        return True

    idempotency_checker.add(key)
    save_checker()

    return False

def check_creation(manager_id: int, file_type: str) -> bool:
    now = datetime.now()
    key = f"{manager_id}_create_{file_type}_{now.year}_{now.month:02d}"
    if key not in idempotency_checker:
        return False

    return True

def check_archivable(manager_id: int) -> bool:
    now = datetime.now()
    time_key = f"{now.year}_{now.month:02d}"

    csv_checker = f"{manager_id}_send_csv_{time_key}" in idempotency_checker
    pdf_checker = f"{manager_id}_send_pdf_{time_key}" in idempotency_checker

    if csv_checker and pdf_checker:
        return True

    return False