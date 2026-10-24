from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from routers import auth_router, detection_router, analytics_router, authority_router
from auth import get_current_user
from config import settings
import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="CivicSafe AI API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(detection_router.router)
app.include_router(analytics_router.router)
app.include_router(authority_router.router)


@app.get("/api/images/{image_id}")
async def get_image(
    image_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Retrieve a report image for its owner or an authorized staff role."""
    result = await db.execute(
        select(models.Image, models.Report.user_id)
        .join(models.Report, models.Image.report_id == models.Report.id)
        .where(models.Image.id == image_id)
    )
    row = result.one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Image not found")

    image, report_owner_id = row
    if (
        report_owner_id != current_user.id
        and current_user.role not in {models.UserRole.admin, models.UserRole.authority}
    ):
        raise HTTPException(status_code=403, detail="Not authorized to view this image")
    
    return StreamingResponse(
        iter([image.data]),
        media_type=image.mime_type,
        headers={"Content-Disposition": f"inline; filename=image_{image_id}"}
    )


@app.get("/")
async def root():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
