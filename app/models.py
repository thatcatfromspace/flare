from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    vehicle_type = Column(String, nullable=False)
    mpg = Column(Float, nullable=True)
    kWh_per_100km = Column(Float, nullable=True)
    acceptance_rate = Column(Float, nullable=False)
    reliability = Column(Float, nullable=False)
    average_pay = Column(Float, nullable=False)
    capacity_lbs = Column(Float, nullable=False)


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)


class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    pickup_lat = Column(Float, nullable=False)
    pickup_lon = Column(Float, nullable=False)
    drop_lat = Column(Float, nullable=False)
    drop_lon = Column(Float, nullable=False)
    size_lbs = Column(Float, nullable=False)
    traffic_delay_min = Column(Float, nullable=True)
