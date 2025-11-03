import asyncio
from sqlalchemy import insert

from app.core.security import hash_password
from app.db.session import session
from app.db.models import Manager, Employee, SalaryRecord, User


async def seed():
    async with session() as seed_session:
        managers = [
            {"id": 1, "name": "Petru", "surname": "Razvan", "email": "razvan.petru.leonte@gmail.com", "cnp": "1111111111"},
            {"id": 2, "name": "Jane", "surname": "Smith", "email": "jane.smith@corp.com", "cnp": "2222222222"},
        ]
        await seed_session.execute(insert(Manager), managers)

        employees = [
            {"id": 1, "name": "Leonte", "surname": "Razvan", "email": "razvan-petru.leonte@endava.com", "cnp": "3333333333", "manager_id": 1},
            {"id": 2, "name": "Bob", "surname": "Brown", "email": "bob.brown@corp.com", "cnp": "4444444444", "manager_id": 2},
            {"id": 3, "name": "Charlie", "surname": "Miller", "email": "charlie.miller@corp.com", "cnp": "5555555555", "manager_id": 2},
        ]
        await seed_session.execute(insert(Employee), employees)

        salaries = [
            {"employee_id": 1, "month": 11, "year": 2025, "working_days": 22, "vacation_days": 2, "base_salary": 4500, "bonuses": 500},
            {"employee_id": 2, "month": 11, "year": 2025, "working_days": 22, "vacation_days": 2, "base_salary": 4500, "bonuses": 500},
            {"employee_id": 3, "month": 11, "year": 2025, "working_days": 22, "vacation_days": 2, "base_salary": 4500, "bonuses": 500},
        ]
        await seed_session.execute(insert(SalaryRecord), salaries)

        users = [
            {"id": 1, "email": "razvan.petru.leonte@gmail.com", "password": hash_password("1111111111"), "role": "manager", "manager_id": 1},
            {"id": 2, "email": "jane.smith@corp.com", "password": hash_password("2222222222"), "role": "manager", "manager_id": 2},
            {"id": 3, "email": "razvan-petru.leonte@endava.com", "password": hash_password("3333333333"), "role": "employee", "employee_id": 1},
            {"id": 4, "email": "bob.brown@corp.com", "password": hash_password("4444444444"), "role": "employee", "employee_id": 2},
            {"id": 5, "email": "charlie.miller@corp.com", "password": hash_password("5555555555"), "role": "employee", "employee_id": 3},
        ]
        await seed_session.execute(insert(User), users)

        await seed_session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
