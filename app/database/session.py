from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from .models import Shipment

engine = create_engine(
    url="sqlite:///sqlite.db",
    echo=True,  # this basically prints the sql statements executed
    connect_args={"check_same_thread": False},
)


def create_db_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(bind=engine) as session:
        yield session


# this annotated type can be used as a type while creating
# parameter in the function call, instead of creating session explicitly and parameter itself
sessionDep = Annotated[Session, Depends(get_session)]
