"""Customer route endpoints"""

from fastapi import APIRouter, HTTPException, status, Response
from models.customer import Customer, CustomerOut, CustomerID, CustomerUpdate
from datetime import datetime, timezone
from typing import List


router = APIRouter(tags=["Customer"])
current_time = datetime.now(timezone.utc)

@router.post("", response_model=CustomerOut)
@router.post("/", response_model=CustomerOut)
async def create_customer(new_customer: Customer):
    """Create a new customer"""
    email_check = await Customer.by_email(new_customer.email)
    if email_check is not None:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "User with that email already exists")

    name_check = await Customer.by_name(new_customer.name)
    if name_check is not None:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "User with that name already exists")

    customer = Customer(
        email=new_customer.email,
        name=new_customer.name,
        phone=new_customer.phone,
        address=new_customer.address,
        created_at=current_time,
        updated_at=None
    )
    await customer.create()
    return customer

@router.get("/", response_model=CustomerOut)
async def get_customer(customer_id: CustomerID):
    """Retrieve a single customer"""
    customer = await Customer.find_one(Customer.email == customer_id.email)
    if customer is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Customer not found!")
    return customer

@router.get("/list/", response_model=List[CustomerOut])
async def list_customer():
    return await Customer.find_all().to_list()

@router.delete("/delete/")
async def delete_customer(customer_id: CustomerID) -> Response:
    """Delete a customer"""
    await Customer.find_one(Customer.email == customer_id.email).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# work on this
@router.patch("/update/", response_model=CustomerOut)
async def update_customer(customer_update: CustomerUpdate) -> Response:
    customer = await Customer.find_one(Customer.email == customer_update.email)

    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Customer does not exist!")

    # update each field if it is not None
    if customer_update.name is not None:
        customer.name = customer_update.name
        customer.updated_at = current_time

    if customer_update.phone is not None:
        customer.phone = customer_update.phone
        customer.updated_at = current_time

    if customer_update.address is not None:
        customer.address = customer_update.address
        customer.updated_at = current_time

    await customer.save()
    return Response("Customer update successful!")