from __future__ import annotations
from decimal import Decimal
from typing import List
from sqlalchemy import String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(255), nullable=False)

    manager_id: Mapped[int | None] = mapped_column(ForeignKey("managers.id"), nullable=True, unique=True)
    employee_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"), nullable=True, unique=True)

class Manager(Base):
    __tablename__ = "managers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    cnp: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    employees: Mapped[List["Employee"]] = relationship(back_populates="manager")


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    cnp: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"))

    manager: Mapped["Manager"] = relationship(back_populates="employees")
    salary_records: Mapped[List["SalaryRecord"]] = relationship(back_populates="employee",
                                                                cascade="all, delete-orphan",
                                                                passive_deletes=True)


class SalaryRecord(Base):
    __tablename__ = "salary_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    working_days: Mapped[int] = mapped_column(Integer, nullable=False)
    vacation_days: Mapped[int] = mapped_column(Integer, nullable=False)
    base_salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    bonuses: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)

    employee: Mapped["Employee"] = relationship(back_populates="salary_records")