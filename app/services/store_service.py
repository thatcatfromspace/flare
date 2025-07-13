from app.models import Store
from app.schemas import StoreCreate, StoreUpdate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_store(db: AsyncSession, store: StoreCreate):
    db_store = Store(**store.dict())
    db.add(db_store)
    await db.commit()
    await db.refresh(db_store)
    return db_store

async def list_stores(db: AsyncSession):
    result = await db.execute(select(Store))
    return result.scalars().all()

async def get_store(db: AsyncSession, store_id: int):
    return await db.get(Store, store_id)

async def update_store(db: AsyncSession, store_id: int, store: StoreUpdate):
    db_store = await db.get(Store, store_id)
    if not db_store:
        return None
    for key, value in store.dict(exclude_unset=True).items():
        setattr(db_store, key, value)
    await db.commit()
    await db.refresh(db_store)
    return db_store

async def delete_store(db: AsyncSession, store_id: int):
    db_store = await db.get(Store, store_id)
    if db_store:
        await db.delete(db_store)
        await db.commit()
