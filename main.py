"""
    Database Models are contained in the Models folder.
    Logic & domain are contained in Routes.
"""
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient

# import Models here
from models.customer import Customer, CustomerID, CustomerUpdate
from models.car import Car, CarUpdate, CarID
from models.order import Order

# import routes here
from routes import car as car_route
from routes import customer as customer_route

config = dotenv_values(".env")

conn_str = config['MONGO_URI'] # set this to the MONGO-URI conn string
database_name = config['DB_NAME'] # set this as the DB name


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.db = AsyncIOMotorClient(conn_str).get_database(database_name)
    # ensure to add all the Models created to the `documents_models` list below
    await init_beanie(app.db, document_models=[
        Customer, CustomerID, CustomerUpdate,
        Car, CarID, CarUpdate,
        Order,
    ]) # add the Models to the DB

    print("DB connection successful...")
    yield
    print("!! Shutdown complete !!")

# start the server with =>  "uvicorn main:app"
app = FastAPI(lifespan=lifespan)
app.include_router(customer_route.router, prefix="/api/v1/customer")
app.include_router(car_route.router, prefix="/api/v1/car")
# app.include_router(OrderRoute.router, prefix="/order")
