from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlmodel import Session

from app.db import Database
from app.database.models import Shipment
from app.database.session import get_session, sessionDep
from app.api.schemas.shipment import BaseShipment, ReadShipment, UpdateShipment

router = APIRouter()

db = Database()

@router.get("/shipment")
def get_shipment(id: int) -> ReadShipment:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist"
        )
    return shipment


@router.get("/shipment/{id}")
def get_shipment_by_id(id: int) -> ReadShipment:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id does not exist"
        )
    return shipment


@router.get("/all-shipments")
def get_all_shipments() -> list[ReadShipment]:
    shipments = db.getAll()
    print("shipments :::::::: ", shipments)
    if shipments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    return shipments


@router.post("/shipment", status_code=status.HTTP_201_CREATED)
def create_shipment(data: BaseShipment) -> int:
    return db.create(data)


@router.patch("/shipment")
def update_shipment(id: int, data: UpdateShipment) -> ReadShipment | None:
    res = db.update(id, data)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "Shipment with given id not found", "error": True},
        )
    return res


@router.delete("/shipment")
def delete_shipment(id: int) -> int | None:
    return db.delete(id)


# api using session ##############################################################################
# creating session in parameters list itself using the Depends method provided by fastApi
# @router.post("/shipment-by-session-1", status_code=status.HTTP_201_CREATED)
# def create_shipment1(
#     data: BaseShipment, session: Session = Depends(get_session)
# ) -> int:
#     new_shipment = Shipment(
#         **data.model_dump(), estimated_delivery=datetime.now() + timedelta(days=3)
#     )
#     session.add(new_shipment)
#     session.commit()
#     session.refresh(new_shipment)
#     return new_shipment.id


# using session provided by the session Annotaion created in session file
@router.post("/shipment-by-session", status_code=status.HTTP_201_CREATED)
async def create_shipment2(data: BaseShipment, session: sessionDep) -> int:
    new_shipment = Shipment(
        **data.model_dump(), estimated_delivery=datetime.now() + timedelta(days=3)
    )
    session.add(new_shipment)
    await session.commit()
    await session.refresh(new_shipment)
    return new_shipment.id


@router.get("/all-shipments-by-session")
async def get_all_shipments_by_session(session: sessionDep) -> list[ReadShipment]:
    # shipments = session.exec(select(Shipment)).scalars().all()
    result = await session.execute(select(Shipment))
    shipments = result.scalars().all()
    print("shipments :::::::: ", shipments)
    if shipments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    return shipments


@router.patch("/shipment-by-session")
async def update_shipment1(
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
    shipment = await session.get(Shipment, id)

    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "Entry not found in record"},
        )

    # updating the session
    shipment.sqlmodel_update(data_to_update)

    # adding back the updated in session
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)

    return shipment


@router.delete("/shipment-by-session")
async def delete_shipment_by_session(id: int, session: sessionDep) -> dict[str, Any]:
    shipment = await session.get(Shipment, id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Record not found"}
        )
    await session.delete(shipment)
    await session.commit()
    print("delete response :: ", shipment)
    return {"detail": f"Shipment with #${id} deleted"}