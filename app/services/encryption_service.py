from pathlib import Path
from pypdf import PdfReader, PdfWriter

from app.core.loging import logger


def encrypt_pdf(path: Path, cnp: str) -> bool:
    try:
        if not path.exists():
            logger.error(f"File is missing for: {path}")
            return False

        reader = PdfReader(str(path))
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(cnp)

        with open(path, "wb") as f:
            writer.write(f)

        return True

    except Exception as e:
        logger.error(f"Encryption failed for file at: {path}, with {e}")
        return False
