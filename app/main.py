from fastapi import FastAPI, HTTPException, status
from typing import Any

from .schemas import BaseShipment

app = FastAPI()


@app.get("/shipment")
def get_shipment():
    return {"content": "wooden table", "status": "in transit"}


@app.get("/shipment/{id}")
def get_shipment_by_id(id: int) -> dict[str, str]:
    return {"id": str(id), "content": "wooden table", "status": "in transit"}


@app.get("/shipment-by-query", status_code=status.HTTP_200_OK)
def get_shipment_by_query(
    qp1: int | None = None, qp2: int | None = None
) -> dict[str, str]:
    if qp1 is not None and qp2 is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": True, "message": "Both fields are required or None"},
        )
    print("variables ::: ", qp1, " : ", qp2)
    return {"content": "wooden table", "status": "in transit"}


@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(data: BaseShipment) -> dict[str, Any]:
    print("body received ::: ", data)
    if "key1" not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Required field missing"},
        )
    return {
        "error": False,
        "message": "shipment created",
        "data": data,
    }


@app.post("/shipment/create")
def create_shipment_fun(shipment: BaseShipment) -> dict[str, Any]:
    print("body received ::: ", shipment)
    return {"error": False, "msg": "Shipment data added", "data": shipment}
