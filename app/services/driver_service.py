from app.models import Driver
from app.schemas import DriverCreate, DriverUpdate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_driver(db: AsyncSession, driver: DriverCreate):
    db_driver = Driver(**driver.dict())
    db.add(db_driver)
    await db.commit()
    await db.refresh(db_driver)
    return db_driver


async def list_drivers(db: AsyncSession):
    result = await db.execute(select(Driver))
    return result.scalars().all()


async def get_driver(db: AsyncSession, driver_id: int):
    return await db.get(Driver, driver_id)


async def update_driver(db: AsyncSession, driver_id: int, driver: DriverUpdate):
    db_driver = await db.get(Driver, driver_id)
    if not db_driver:
        return None
    for key, value in driver.dict(exclude_unset=True).items():
        setattr(db_driver, key, value)
    await db.commit()
    await db.refresh(db_driver)
    return db_driver


async def delete_driver(db: AsyncSession, driver_id: int):
    db_driver = await db.get(Driver, driver_id)
    if db_driver:
        await db.delete(db_driver)
        await db.commit()
