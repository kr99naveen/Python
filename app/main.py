from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager

from typing import Any
from .schemas import BaseShipment,ReadShipment, UpdateShipment
from .db import Database
from app.database.session import create_db_tables
from rich import print, panel


@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    print(panel.Panel("Server started...",border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("Server stopped...",border_style="red"))

app = FastAPI(lifespan=lifespan_handler)

db = Database()

@app.get("/shipment")
def get_shipment(id:int)->ReadShipment:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist"
        )
    return shipment

@app.get("/shipment/{id}")
def get_shipment_by_id(id: int) -> ReadShipment:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id does not exist"
        )
    return shipment

@app.get("/all-shipments")
def get_all_shipments() -> list[ReadShipment]:
    shipments = db.getAll()
    print("shipments :::::::: ",shipments)
    if shipments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No shipments found"
        )
    return shipments


@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(data: BaseShipment) -> int:
    return db.create(data)
    

@app.patch("/shipment")
def update_shipment(id:int, data: UpdateShipment)->ReadShipment|None:
    res = db.update(id, data)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= {
                "msg": "Shipment with given id not found",
                "error": True
            }
        )
    return res


@app.delete("/shipment")
def update_shipment(id:int)->int|None:
    return db.delete(id)
