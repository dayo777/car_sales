"""Customer DB Representation"""

from beanie import Document, Indexed
from datetime import datetime
from typing import Annotated, Optional
from pydantic import EmailStr


class CustomerOut(Document):
    """Customer fields returned to the client"""
    email: Annotated[str, Indexed(EmailStr, unique=True)]
    name: Indexed(str, unique=True)
    phone: str
    address: str

    class Settings:
        name = "customer"

# class CustomerCreate(Document):
#     email: Annotated[str, Indexed(EmailStr, unique=True)]
#     name: Indexed(str, unique=True)
#     phone: str
#     address: str

class Customer(Document):
    """Customer DB representation"""
    email: Annotated[str, Indexed(EmailStr, unique=True)]
    name: Indexed(str, unique=True)
    phone: str
    address: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Settings:
        max_nesting_depth = 3
        name = "customer"

    def __repr__(self) -> str:
        return f"<Customer {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Customer):
            return self.email == other.email
        return False

    @classmethod
    async def by_email(cls, email: str) -> Optional["Customer"]:
        """Get a user by email"""
        return await cls.find_one(cls.email == email)

    @classmethod
    async def by_name(cls, name: str) -> Optional["Customer"]:
        """Get a user by name"""
        return await cls.find_one(cls.name == name)

class CustomerUpdate(Document):
    """Updatable Customer fields"""
    email: EmailStr
    name: str | None = None
    phone: str | None = None
    address: str | None = None

    class Settings:
        name = "customer"

class CustomerID(Document):
    email: EmailStr

    class Settings:
        name = "customer"