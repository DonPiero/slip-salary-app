import shutil
from datetime import datetime
from pathlib import Path
import zipfile
from app.core.loging import logger


def archive_exported_files(manager_id: int) -> Path | None:
    try:
        root_directory = Path(__file__).resolve().parents[2]
        export_directory = root_directory / "data" / "export" / f"manager_{manager_id}"

        if not export_directory.exists():
            logger.warning(f"Export folder for manager_{manager_id} does not exist.")
            return None

        now = datetime.now()
        zip_name = f"{now.year}_{now.month:02d}"
        archive_directory = root_directory / "data" / "archive" / f"manager_{manager_id}"
        archive_directory.mkdir(parents=True, exist_ok=True)

        archive_path = archive_directory / f"archived_files_{zip_name}.zip"

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in export_directory.rglob("*"):
                if file.is_file():
                    zipf.write(file, arcname=file.relative_to(export_directory))

        logger.warning(f"Archive triggered for manager {manager_id}.")
        shutil.rmtree(export_directory)
        return archive_path

    except Exception as e:
        logger.error(f"Failed to archive exported files: {e}")
        return None