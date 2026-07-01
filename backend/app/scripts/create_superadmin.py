"""Create superadmin script."""
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from getpass import getpass
from app.core.config import settings
from app.models.base import Base
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_superadmin():
    engine = create_async_engine(settings.database_url, echo=False)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        full_name = input("Full Name: ")
        email = input("Email: ")
        password = getpass("Password (min 8 chars): ")

        if len(password) < 8:
            print("Password too short")
            await engine.dispose()
            return

        user = User(
            full_name=full_name,
            email=email,
            password_hash=pwd_context.hash(password),
            role="admin",
            status="active"
        )
        session.add(user)
        await session.commit()
        print(f"Admin user {email} created successfully")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_superadmin())


if __name__ == "__main__":
    main()
