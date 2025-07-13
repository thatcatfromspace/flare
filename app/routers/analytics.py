from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import analytics_service
from app.schemas import AnalyticsRequest, CostCO2Out, DashboardOut
from app.dependencies import get_db, get_redis

router = APIRouter()


@router.post("/cost-co2-saved", response_model=CostCO2Out)
async def cost_co2_saved(
    req: AnalyticsRequest, db: AsyncSession = Depends(get_db), redis=Depends(get_redis)
):
    return await analytics_service.calculate_cost_co2_saved(db, redis, req)


@router.get("/dashboard", response_model=DashboardOut)
async def dashboard_metrics(
    db: AsyncSession = Depends(get_db), redis=Depends(get_redis)
):
    return await analytics_service.dashboard_metrics(db, redis)
