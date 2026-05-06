from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status
from rich import panel, print
from sqlalchemy import select
from sqlmodel import Session

from app.database.models import Shipment
from app.database.session import create_db_tables, get_session, sessionDep

from .db import Database
from .schemas import BaseShipment, ReadShipment, UpdateShipment


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server started...", border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("Server stopped...", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)

db = Database()


@app.get("/shipment")
def get_shipment(id: int) -> ReadShipment:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist"
        )
    return shipment


@app.get("/shipment/{id}")
def get_shipment_by_id(id: int) -> ReadShipment:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist"
        )
    return shipment


@app.get("/all-shipments")
def get_all_shipments() -> list[ReadShipment]:
    shipments = db.getAll()
    print("shipments :::::::: ", shipments)
    if shipments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    return shipments


@app.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(data: BaseShipment) -> int:
    return db.create(data)


@app.patch("/shipment")
def update_shipment(id: int, data: UpdateShipment) -> ReadShipment | None:
    res = db.update(id, data)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "Shipment with given id not found", "error": True},
        )
    return res


@app.delete("/shipment")
def delete_shipment(id: int) -> int | None:
    return db.delete(id)


# api using session
# creating session in parameters list itself using the Depends method provided by fastApi
@app.post("/shipment-by-session-1", status_code=status.HTTP_201_CREATED)
def create_shipment1(
    data: BaseShipment, session: Session = Depends(get_session)
) -> int:
    new_shipment = Shipment(
        **data.model_dump(), estimated_delivery=datetime.now() + timedelta(days=3)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return new_shipment.id


# using session provided by the session Annotaion created in session file
@app.post("/shipment-by-session-2", status_code=status.HTTP_201_CREATED)
def create_shipment2(data: BaseShipment, session: sessionDep) -> int:
    new_shipment = Shipment(
        **data.model_dump(), estimated_delivery=datetime.now() + timedelta(days=3)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return new_shipment.id


@app.get("/all-shipments-by-session")
def get_all_shipments_by_session(session: sessionDep) -> list[ReadShipment]:
    shipments = session.exec(select(Shipment)).scalars().all()
    print("shipments :::::::: ", shipments)
    if shipments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    return shipments


@app.patch("/shipment-by-session")
def update_shipment1(
    id: int, data: UpdateShipment, session: sessionDep
) -> ReadShipment:

    print("control in updating the data ::: ", data)
    data_to_update = data.model_dump(exclude_none=True)
    if not data_to_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"msg": "No parameters found in th request"},
        )
    # taking out the session
    shipment = session.get(Shipment, id)

    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "Entry not found in record"},
        )

    # updating the session
    shipment.sqlmodel_update(data_to_update)

    # adding back the updated in session
    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@app.delete("/shipment-by-session")
def delete_shipment_by_session(id: int, session: sessionDep) -> dict[str, Any]:
    shipment = session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Record not found"}
        )
    session.delete(shipment)
    session.commit()
    print("delete response :: ", shipment)
    return {"detail": f"Shipment with #${id} deleted"}
