from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import delivery_service
from app.schemas import DeliveryCreate, DeliveryUpdate, DeliveryOut
from app.dependencies import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=DeliveryOut)
async def create_delivery(delivery: DeliveryCreate, db: AsyncSession = Depends(get_db)):
    return await delivery_service.create_delivery(db, delivery)


@router.get("/", response_model=List[DeliveryOut])
async def list_deliveries(db: AsyncSession = Depends(get_db)):
    return await delivery_service.list_deliveries(db)


@router.get("/{delivery_id}", response_model=DeliveryOut)
async def get_delivery(delivery_id: int, db: AsyncSession = Depends(get_db)):
    delivery = await delivery_service.get_delivery(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery


@router.put("/{delivery_id}", response_model=DeliveryOut)
async def update_delivery(
    delivery_id: int, delivery: DeliveryUpdate, db: AsyncSession = Depends(get_db)
):
    return await delivery_service.update_delivery(db, delivery_id, delivery)


@router.delete("/{delivery_id}")
async def delete_delivery(delivery_id: int, db: AsyncSession = Depends(get_db)):
    await delivery_service.delete_delivery(db, delivery_id)
    return {"detail": "Delivery deleted"}
