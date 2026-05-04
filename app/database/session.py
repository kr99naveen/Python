from sqlalchemy import create_engine
from sqlmodel import SQLModel
from .models import Shipment

engine=create_engine(
    url="sqlite:///sqlite.db",
    echo=True,
    connect_args={
        "check_same_thread" : False
    }
)

SQLModel.metadata.create_all(bind=engine)