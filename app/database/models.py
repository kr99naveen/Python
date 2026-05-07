from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field, Column

class ShipmentStatusEnum(str,Enum):
    placed="placed"
    in_transit="in_transit"
    out_for_delivery="out_for_delivery"
    delivered="delivered"

class Shipment(SQLModel, table=True):
    __tablename__="shipments"

    id : int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatusEnum = Field(default=ShipmentStatusEnum.placed)
    estimated_delivery: datetime | None