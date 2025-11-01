from fastapi import FastAPI
from app.api.routers import login, create_excel, send_excel, create_pdf, send_pdf

app = FastAPI(title="Slip Salary App")

app.include_router(login.router)
app.include_router(create_excel.router)
app.include_router(send_excel.router)
app.include_router(create_pdf.router)
app.include_router(send_pdf.router)