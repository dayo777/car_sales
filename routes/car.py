"""Car route endpoints"""

from typing import List
import json

from fastapi import APIRouter, HTTPException, status, Response
from models.car import Car, CarUpdate, CarOut, CarID, CarStatus
from datetime import datetime, timezone



router = APIRouter(tags=["Car"])
current_time = datetime.now(timezone.utc)

@router.post("/", response_model=CarOut)
@router.post("", response_model=CarOut)
async def create_car(new_car: Car):
    """Create a new car"""
    vin_check = await Car.by_vin(new_car.vin)
    if vin_check is not None:
        return HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Car with VIN already exist.")

    car = Car(
        vin=new_car.vin,
        make=new_car.make,
        model=new_car.model,
        year=new_car.year,
        price=new_car.price,
        mileage=new_car.mileage,
        color=new_car.color,
        status=new_car.status,
        created_at=current_time,
        updated_at=None
    )
    await car.create()
    return car

@router.get("", response_model=CarOut)
@router.get("/", response_model=CarOut)
async def get_car(car_id: CarID):
    """Retrieve a single Car"""
    car = await Car.find_one(Car.vin == car_id.vin)
    if car is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Car not found!")
    return car

@router.get("/list", response_model=List[CarOut])
@router.get("/list/", response_model=List[CarOut])
async def list_car():
    return await Car.find_all().to_list()

@router.delete("/delete")
@router.delete("/delete/")
async def delete_customer(car_id: CarID) -> Response:
    """Delete a car"""
    await Car.find_one(Car.vin == car_id.vin).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/update", response_model=CarOut)
@router.patch("/update/", response_model=CarOut)
async def update_car(car_update: CarUpdate) -> Response:
    car = await Car.find_one(Car.vin == car_update.vin)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Error updating cars")

    # if car is Sold, do not update the Status
    check_if_sold = await Car.check_if_sold(car.status)
    if check_if_sold is None:
        # update each field if supplied
        if car_update.price is not None:
            car.price = car_update.price
            car.updated_at = current_time

        if car_update.status is not None:
            car.status = car_update.status
            car.updated_at = current_time

        await car.save()
        return Response("Car update successful!")

    return Response("Unable to update sold Car!")