from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
import models


async def store_report_image(
    file_bytes: bytes,
    mime_type: str,
    report_id: int,
    db: AsyncSession,
) -> str:
    """Store a report image in PostgreSQL and return its API URL."""
    image = models.Image(
        report_id=report_id,
        mime_type=mime_type,
        data=file_bytes,
    )
    db.add(image)
    await db.flush()

    return f"{settings.API_URL}/api/images/{image.id}"
