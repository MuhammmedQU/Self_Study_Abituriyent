"""Refresh token repository."""

from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    """Refresh token repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, RefreshToken)

    async def get_by_token_hash(self, token_hash: str) -> RefreshToken | None:
        """Get token by hash."""
        stmt = select(self.model).where(self.model.token_hash == token_hash)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_token(self, token_hash: str) -> RefreshToken | None:
        """Revoke refresh token."""
        token = await self.get_by_token_hash(token_hash)
        if token:
            token.revoked_at = datetime.utcnow()
            self.db.add(token)
            await self.db.flush()
        return token

    async def revoke_all_user_tokens(self, user_id: int) -> None:
        """Revoke all tokens for user."""
        from sqlalchemy import update
        stmt = (
            update(self.model)
            .where(
                and_(
                    self.model.user_id == user_id,
                    self.model.revoked_at.is_(None),
                )
            )
            .values(revoked_at=datetime.utcnow())
        )
        await self.db.execute(stmt)
        await self.db.flush()

    async def get_active_tokens(self, user_id: int) -> list[RefreshToken]:
        """Get active tokens for user."""
        stmt = select(self.model).where(
            and_(
                self.model.user_id == user_id,
                self.model.revoked_at.is_(None),
                self.model.expires_at > datetime.utcnow(),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
