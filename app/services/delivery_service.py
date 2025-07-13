from app.models import Delivery
from app.schemas import DeliveryCreate, DeliveryUpdate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_delivery(db: AsyncSession, delivery: DeliveryCreate):
    db_delivery = Delivery(**delivery.dict())
    db.add(db_delivery)
    await db.commit()
    await db.refresh(db_delivery)
    return db_delivery


async def list_deliveries(db: AsyncSession):
    result = await db.execute(select(Delivery))
    return result.scalars().all()


async def get_delivery(db: AsyncSession, delivery_id: int):
    return await db.get(Delivery, delivery_id)


async def update_delivery(db: AsyncSession, delivery_id: int, delivery: DeliveryUpdate):
    db_delivery = await db.get(Delivery, delivery_id)
    if not db_delivery:
        return None
    for key, value in delivery.dict(exclude_unset=True).items():
        setattr(db_delivery, key, value)
    await db.commit()
    await db.refresh(db_delivery)
    return db_delivery


async def delete_delivery(db: AsyncSession, delivery_id: int):
    db_delivery = await db.get(Delivery, delivery_id)
    if db_delivery:
        await db.delete(db_delivery)
        await db.commit()
