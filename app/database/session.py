from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from .models import Shipment
from config import settings


################################### Sqlite DB configuration ###########################################
# engine = create_engine(
#     url="sqlite:///sqlite.db",
#     echo=True,  # this basically prints the sql statements executed
#     connect_args={"check_same_thread": False},
# )


# def create_db_tables():
#     SQLModel.metadata.create_all(bind=engine)


# def get_session():
#     with Session(bind=engine) as session:
#         yield session


# # this annotated type can be used as a type while creating
# # parameter in the function call, instead of creating session explicitly and parameter itself
# sessionDep = Annotated[Session, Depends(get_session)]

######################################################################################################


#################################### POSTGRESQL configuration ########################################

engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True,  # this basically prints the sql statements executed
)


async def create_db_tables():
    try:
        async with engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print("exception while creating the tables ::: ",e)
    


async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session


# this annotated type can be used as a type while creating
# parameter in the function call, instead of creating session explicitly and parameter itself
sessionDep = Annotated[AsyncSession, Depends(get_session)]


