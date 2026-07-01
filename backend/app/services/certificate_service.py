"""Certificate service."""
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode
import io
from app.repositories import CertificateRepository, UserRepository
from app.utils.storage import storage_service

class CertificateService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.cert_repo = CertificateRepository(db)
        self.user_repo = UserRepository(db)

    async def generate_module_certificate(self, user_id: int, module_id: int, module_title: str, score: int):
        existing = await self.cert_repo.get_module_certificate(user_id, module_id)
        if existing:
            return existing

        unique_id = str(uuid.uuid4())[:12].upper()
        qr_path = f"certificates/qr_{unique_id}.png"
        pdf_path = f"certificates/{unique_id}.pdf"

        verification_url = f"https://lms.example.com/verify/{unique_id}"
        qr_code = qrcode.make(verification_url)
        qr_buffer = io.BytesIO()
        qr_code.save(qr_buffer, format="PNG")
        await storage_service.save_file(qr_path, qr_buffer.getvalue())

        user = await self.user_repo.get(user_id)
        self._create_pdf(user.full_name, module_title, score, pdf_path, qr_path)

        cert = await self.cert_repo.create({
            "user_id": user_id,
            "module_id": module_id,
            "certificate_type": "module",
            "unique_id": unique_id,
            "qr_code_path": qr_path,
            "pdf_path": pdf_path,
            "score": score,
        })
        await self.cert_repo.commit()
        return cert

    def _create_pdf(self, user_name: str, title: str, score: int, pdf_path: str, qr_path: str):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, 700, "Certificate of Completion")
        c.setFont("Helvetica", 14)
        c.drawString(100, 650, f"This is to certify that {user_name}")
        c.drawString(100, 620, f"has successfully completed {title}")
        c.drawString(100, 590, f"Score: {score}%")
        c.drawString(100, 560, f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}")
        c.save()
        buffer.seek(0)
