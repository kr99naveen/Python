from pydantic import BaseModel, Field
from random import randint


# pydantic provide the data validation along with type hints, this
# class will act like a DTO file like in js
class BaseShipment(BaseModel):
    content: str = Field(max_length=100)
    weight: float = Field(lt=20, gt=10)
    destination: int | None = Field(default=randint(11000, 11999))


class ReadShipment(BaseShipment):
    id: int
