from beanie import Document, Link
from datetime import datetime

# other models
from customer import Customer
from car import Car
from enum import Enum


class OrderStatus(Enum):
    DELIVERED = "delivered"
    PENDING = "pending"



class Order(Document):
    """Order DB representation"""
    customer_id: Link[Customer]
    car_id: Link[Car]
    order_date: datetime
    delivery_date: datetime | None = None
    status: OrderStatus
    total_price: float
    updated_at: datetime | None = None

    class Settings:
        name = "order"

    def __str__(self) -> str:
        return f""

class OrderUpdate(Document):
    status: OrderStatus | None = None

    class Settings:
        name = "order"