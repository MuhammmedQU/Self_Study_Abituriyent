from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id: Mapped[int | None] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=True)
    module_id: Mapped[int | None] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), nullable=True)
    certificate_type: Mapped[str] = mapped_column(String(50), nullable=False)  # module, course
    unique_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    qr_code_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    pdf_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    score: Mapped[int | None] = mapped_column(nullable=True)  # overall score if applicable
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="certificates")
    course: Mapped["Course | None"] = relationship("Course", back_populates="certificates")
    module: Mapped["Module | None"] = relationship("Module", back_populates="certificates")
