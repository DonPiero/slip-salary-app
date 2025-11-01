import smtplib
from pathlib import Path
from email.message import EmailMessage

from app.core.config import settings
from app.core.loging import logger


def send_email(role: str, to: str, manager_id: int, entity_id: int) -> bool:
    try:
        base_directory = Path(__file__).resolve().parents[2] / "data" / "export" / f"manager_{manager_id}"

        if role.lower().strip() == "manager":
            subject = "Monthly Employee Report"
            body = (
                "Dear Manager,\n\n"
                "You can find attached to this email the aggregated employee data for this current month.\n"
                "Please review the details and act accordingly.\n\n"
                "Best regards,\n"
                "Slip Salary App"
            )
            path = base_directory / "csv" / f"manager_{entity_id}.csv"

        elif role.lower() == "employee":
            subject = "Monthly Payslip"
            body = (
                "Dear Employee,\n\n"
                "You can find attached to this email your payslip for this current month.\n"
                "The attached pdf file is password protected, please use your CNP to open it.\n\n"
                "Best regards,\n"
                "Slip Salary App"
            )
            path = base_directory / "pdf" / f"employee_{entity_id}.pdf"

        else:
            logger.warning(f"Unknown role {role} can't be recognized")
            return False

        msg = EmailMessage()
        msg["From"] = settings.smtp_user
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        if path.exists():
            with open(path, "rb") as f:
                data = f.read()
                msg.add_attachment(
                    data,
                    maintype="application",
                    subtype="octet-stream",
                    filename=path.name,
                )
        else:
            logger.warning(f"Path does not exist to attach to email for: {to}")
            return False

        with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)

        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to}, error: {e}")
        return False
