from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import driver_service
from app.schemas import DriverCreate, DriverUpdate, DriverOut
from app.dependencies import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=DriverOut)
async def create_driver(driver: DriverCreate, db: AsyncSession = Depends(get_db)):
    return await driver_service.create_driver(db, driver)


@router.get("/", response_model=List[DriverOut])
async def list_drivers(db: AsyncSession = Depends(get_db)):
    return await driver_service.list_drivers(db)


@router.get("/{driver_id}", response_model=DriverOut)
async def get_driver(driver_id: int, db: AsyncSession = Depends(get_db)):
    driver = await driver_service.get_driver(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.put("/{driver_id}", response_model=DriverOut)
async def update_driver(
    driver_id: int, driver: DriverUpdate, db: AsyncSession = Depends(get_db)
):
    return await driver_service.update_driver(db, driver_id, driver)


@router.delete("/{driver_id}")
async def delete_driver(driver_id: int, db: AsyncSession = Depends(get_db)):
    await driver_service.delete_driver(db, driver_id)
    return {"detail": "Driver deleted"}
