from pydantic import BaseModel
from typing import Optional, List


class DriverBase(BaseModel):
    name: str
    lat: float
    lon: float
    vehicle_type: str
    mpg: Optional[float]
    kWh_per_100km: Optional[float]
    acceptance_rate: float
    reliability: float
    average_pay: float
    capacity_lbs: float


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    vehicle_type: Optional[str]
    mpg: Optional[float]
    kWh_per_100km: Optional[float]
    acceptance_rate: Optional[float]
    reliability: Optional[float]
    average_pay: Optional[float]
    capacity_lbs: Optional[float]


class DriverOut(DriverBase):
    id: int


class StoreBase(BaseModel):
    name: str
    lat: float
    lon: float


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: Optional[str]
    lat: Optional[float]
    lon: Optional[float]


class StoreOut(StoreBase):
    id: int


class DeliveryBase(BaseModel):
    pickup_lat: float
    pickup_lon: float
    drop_lat: float
    drop_lon: float
    size_lbs: float
    traffic_delay_min: Optional[float]


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryUpdate(BaseModel):
    pickup_lat: Optional[float]
    pickup_lon: Optional[float]
    drop_lat: Optional[float]
    drop_lon: Optional[float]
    size_lbs: Optional[float]
    traffic_delay_min: Optional[float]


class DeliveryOut(DeliveryBase):
    id: int


class DeleteResponse(BaseModel):
    detail: str


class DeliveryScoreRequest(BaseModel):
    delivery_id: int


class DriverScoreOut(BaseModel):
    driver: DriverOut
    score: float


class AnalyticsRequest(BaseModel):
    start_date: Optional[str]
    end_date: Optional[str]


class CostCO2Out(BaseModel):
    cost_saved: float
    co2_saved: float


class DashboardOut(BaseModel):
    total_deliveries: int
    total_drivers: int
    total_cost_saved: float
    total_co2_saved: float
