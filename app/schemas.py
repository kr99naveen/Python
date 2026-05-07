# from datetime import datetime
# from enum import Enum
# from random import randint

# from pydantic import BaseModel, Field

# from app.database.models import ShipmentStatusEnum


# # APIs schema for validating Req/Res data
# # pydantic provide the data validation along with type hints, this
# # class will act like a DTO file like in js
# class BaseShipment(BaseModel):
#     content: str = Field(max_length=100)
#     weight: float = Field(lt=20, gt=10)
#     destination: int | None = Field(default=randint(11000, 11999))


# class ReadShipment(BaseShipment):
#     id: int
#     status: ShipmentStatusEnum = Field(default=ShipmentStatusEnum.placed)
#     estimated_delivery: datetime


# class UpdateShipment(BaseModel):
#     status: ShipmentStatusEnum | None = Field(default=None)
#     estimated_delivery: datetime | None = Field(default=None)
