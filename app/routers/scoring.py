from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import scoring_service
from app.schemas import DeliveryScoreRequest, DriverScoreOut
from app.dependencies import get_db, get_redis
from typing import List

router = APIRouter()


@router.post("/top-drivers", response_model=List[DriverScoreOut])
async def get_top_drivers_for_delivery(
    req: DeliveryScoreRequest,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
):
    # Returns top 3 drivers for the delivery, with full driver payloads
    return await scoring_service.get_top_drivers(db, redis, req)
