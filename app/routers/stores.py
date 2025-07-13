from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import store_service
from app.schemas import StoreCreate, StoreUpdate, StoreOut
from app.dependencies import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=StoreOut)
async def create_store(store: StoreCreate, db: AsyncSession = Depends(get_db)):
    return await store_service.create_store(db, store)


@router.get("/", response_model=List[StoreOut])
async def list_stores(db: AsyncSession = Depends(get_db)):
    return await store_service.list_stores(db)


@router.get("/{store_id}", response_model=StoreOut)
async def get_store(store_id: int, db: AsyncSession = Depends(get_db)):
    store = await store_service.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.put("/{store_id}", response_model=StoreOut)
async def update_store(
    store_id: int, store: StoreUpdate, db: AsyncSession = Depends(get_db)
):
    return await store_service.update_store(db, store_id, store)


@router.delete("/{store_id}")
async def delete_store(store_id: int, db: AsyncSession = Depends(get_db)):
    await store_service.delete_store(db, store_id)
    return {"detail": "Store deleted"}
