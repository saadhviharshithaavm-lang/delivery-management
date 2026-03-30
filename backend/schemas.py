from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date

# Customer Schemas
class CustomerBase(BaseModel):
    Name: str = Field(..., min_length=1, max_length=100)
    Phone_Num: str = Field(..., pattern=r'^\d{10}$')
    Address: str = Field(..., min_length=1, max_length=255)
    Area: str = Field(..., min_length=1, max_length=50)
    Account_Status: Literal['Active', 'Inactive'] = 'Active'

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    Name: Optional[str] = Field(None, min_length=1, max_length=100)
    Phone_Num: Optional[str] = Field(None, pattern=r'^\d{10}$')
    Address: Optional[str] = Field(None, min_length=1, max_length=255)
    Area: Optional[str] = Field(None, min_length=1, max_length=50)
    Account_Status: Optional[Literal['Active', 'Inactive']] = None

class CustomerResponse(CustomerBase):
    Customer_ID: str

    class Config:
        from_attributes = True

# Supplier Schemas
class SupplierBase(BaseModel):
    Supplier_Name: str
    Phone_Num: str

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    Supplier_ID: str

    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    Product_Name: str
    Price_per_unit: float
    Unit: str

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    Product_ID: str

    class Config:
        from_attributes = True

# Generic Response
class MessageResponse(BaseModel):
    message: str
    success: bool = True
