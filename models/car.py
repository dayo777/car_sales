"""Car DB Representation"""
from typing import Optional

from beanie import Document, Indexed
from datetime import datetime
from enum import Enum


class CarStatus(Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    UNAVAILABLE = "unavailable"

# You can add more colors
class CarColor(Enum):
    BLACK = "black"
    WHITE = "white"
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

# use the VIN as a dummy ID, pending implementation of the auth
class Car(Document):
    """Car DB representation"""
    vin: Indexed(int, unique=True)
    make: str
    model: str
    year: int
    price: float
    mileage: float
    color: CarColor
    status: CarStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Settings:
        name = "car"

    def __str__(self) -> str:
        return f"{self.year} {self.make} {self.model}"

    @classmethod
    async def by_vin(cls, vin: int) -> Optional["Car"]:
        """Get a car by VIN"""
        return await cls.find_one(cls.vin == vin)

    @classmethod
    async def check_if_sold(cls, sold_status: CarStatus) -> Optional["Car"]:
        """Check if car is sold already to prevent updating any value on the Car"""
        return await cls.find_one(cls.status.value == sold_status.value)

class CarUpdate(Document):
    vin: int
    price: float | None = None
    status: CarStatus | None = None

    class Settings:
        name = "car"

class CarOut(Document):
    vin: Indexed(int, unique=True)
    make: str
    model: str
    year: int
    price: float
    mileage: float
    color: CarColor
    status: CarStatus

    class Settings:
        name = "car"

class CarID(Document):
    vin: Indexed(int, unique=True)

    class Settings:
        name = "car"