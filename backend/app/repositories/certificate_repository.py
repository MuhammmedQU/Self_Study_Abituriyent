"""Certificate repository."""

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.certificate import Certificate
from app.repositories.base import BaseRepository


class CertificateRepository(BaseRepository[Certificate]):
    """Certificate repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Certificate)

    async def get_user_certificates(self, user_id: int) -> list[Certificate]:
        """Get all certificates for user."""
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_unique_id(self, unique_id: str) -> Certificate | None:
        """Get certificate by unique ID."""
        stmt = select(self.model).where(self.model.unique_id == unique_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_module_certificate(
        self, user_id: int, module_id: int
    ) -> Certificate | None:
        """Get module certificate for user."""
        stmt = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.module_id == module_id,
                self.model.certificate_type == "module",
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_course_certificate(
        self, user_id: int, course_id: int
    ) -> Certificate | None:
        """Get course certificate for user."""
        stmt = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.course_id == course_id,
                self.model.certificate_type == "course",
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
