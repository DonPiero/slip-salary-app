from datetime import datetime


idempotency_checker: set[str] = set()

def check_duplicate(manager_id: int, file_type: str, action: str) -> bool:
    now = datetime.now()
    key = f"{manager_id}_{action}_{file_type}_{now.year}_{now.month:02d}"
    if key in idempotency_checker:
        return True

    idempotency_checker.add(key)
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