from datetime import datetime
from enum import Enum

from sqlmodel import SQLModel, Field

class ShipmentStatusEnum(str,Enum):
    placed="placed"
    in_transit="in_transit"
    out_for_delivery="out_for_delivery"
    delivered="delivered"

class Shipment(SQLModel, table=True):
    __tablename__="shipments2"

    id : int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatusEnum
    estimated_delivery: datetime 