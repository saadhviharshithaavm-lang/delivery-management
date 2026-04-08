from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import date

# ==================== CUSTOMER ====================
class CustomerBase(BaseModel):
    Name: str = Field(..., min_length=1, max_length=50)
    Phone_Num: str = Field(..., pattern=r'^\d{10}$')
    Address: str = Field(..., min_length=1, max_length=100)
    Area: str = Field(..., min_length=1, max_length=50)
    User_Name: Optional[str] = Field(None, min_length=3, max_length=50)
    Password: Optional[str] = Field(None, min_length=4, max_length=100)
    Account_Status: Literal['Active', 'Inactive'] = 'Active'

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    Name: Optional[str] = Field(None, min_length=1, max_length=50)
    Phone_Num: Optional[str] = Field(None, pattern=r'^\d{10}$')
    Address: Optional[str] = Field(None, min_length=1, max_length=100)
    Area: Optional[str] = Field(None, min_length=1, max_length=50)
    User_Name: Optional[str] = Field(None, min_length=3, max_length=50)
    Password: Optional[str] = Field(None, min_length=4, max_length=100)
    Account_Status: Optional[Literal['Active', 'Inactive']] = None

class CustomerResponse(BaseModel):
    Customer_ID: int
    Name: str
    Phone_Num: str
    Address: str
    Area: str
    Account_Status: Literal['Active', 'Inactive']
    User_Name: Optional[str] = None
    class Config:
        from_attributes = True

# ==================== SUPPLIER ====================
class SupplierBase(BaseModel):
    Supplier_Name: str = Field(..., min_length=1, max_length=50)
    Phone_Num: str = Field(..., min_length=1, max_length=15)
    User_Name: Optional[str] = Field(None, min_length=3, max_length=50)
    Password: Optional[str] = Field(None, min_length=4, max_length=100)

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    Supplier_Name: Optional[str] = Field(None, min_length=1, max_length=50)
    Phone_Num: Optional[str] = Field(None, min_length=1, max_length=15)
    User_Name: Optional[str] = Field(None, min_length=3, max_length=50)
    Password: Optional[str] = Field(None, min_length=4, max_length=100)

class SupplierResponse(BaseModel):
    Supplier_ID: int
    Supplier_Name: str
    Phone_Num: str
    User_Name: Optional[str] = None
    class Config:
        from_attributes = True

# ==================== PRODUCT ====================
class ProductBase(BaseModel):
    Product_Name: str = Field(..., min_length=1, max_length=50)
    Price_per_unit: float = Field(..., gt=0)
    Unit: str = Field(..., min_length=1, max_length=20)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    Product_Name: Optional[str] = Field(None, min_length=1, max_length=50)
    Price_per_unit: Optional[float] = Field(None, gt=0)
    Unit: Optional[str] = Field(None, min_length=1, max_length=20)

class ProductResponse(ProductBase):
    Product_ID: int
    class Config:
        from_attributes = True

# ==================== INVENTORY ====================
class InventoryBase(BaseModel):
    Product_ID: int
    Supplier_ID: int
    Available_quantity: int = 0
    LastUpdated: Optional[date] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    Product_ID: Optional[int] = None
    Supplier_ID: Optional[int] = None
    Available_quantity: Optional[int] = None
    LastUpdated: Optional[date] = None

class InventoryResponse(InventoryBase):
    Inventory_ID: int
    class Config:
        from_attributes = True

# ==================== SUBSCRIPTION ====================
class SubscriptionBase(BaseModel):
    Customer_ID: int
    Supplier_ID: int
    Start_date: date
    End_date: date
    Status: Literal['Active', 'Paused', 'Cancelled'] = 'Active'

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    Customer_ID: Optional[int] = None
    Supplier_ID: Optional[int] = None
    Start_date: Optional[date] = None
    End_date: Optional[date] = None
    Status: Optional[Literal['Active', 'Paused', 'Cancelled']] = None

class SubscriptionResponse(SubscriptionBase):
    Subscription_ID: int
    class Config:
        from_attributes = True

# ==================== SUBSCRIPTION DETAIL ====================
class SubscriptionDetailBase(BaseModel):
    Subscription_ID: int
    Product_ID: int
    Quantity_Per_Day: int
    Delivery_Frequency: str = Field(..., max_length=20)

class SubscriptionDetailCreate(SubscriptionDetailBase):
    pass

class SubscriptionDetailUpdate(BaseModel):
    Subscription_ID: Optional[int] = None
    Product_ID: Optional[int] = None
    Quantity_Per_Day: Optional[int] = None
    Delivery_Frequency: Optional[str] = Field(None, max_length=20)

class SubscriptionDetailResponse(SubscriptionDetailBase):
    class Config:
        from_attributes = True

# ==================== DELIVERY PERSON ====================
class DeliveryPersonBase(BaseModel):
    Name: str = Field(..., min_length=1, max_length=50)
    Phone_Num: str = Field(..., min_length=1, max_length=15)
    User_Name: Optional[str] = Field(None, min_length=3, max_length=50)
    Password: Optional[str] = Field(None, min_length=4, max_length=100)
    VehicleType: Optional[str] = Field(None, max_length=20)
    Area_assigned: Optional[str] = Field(None, max_length=50)

class DeliveryPersonCreate(DeliveryPersonBase):
    pass

class DeliveryPersonUpdate(BaseModel):
    Name: Optional[str] = Field(None, min_length=1, max_length=50)
    Phone_Num: Optional[str] = Field(None, min_length=1, max_length=15)
    User_Name: Optional[str] = Field(None, min_length=3, max_length=50)
    Password: Optional[str] = Field(None, min_length=4, max_length=100)
    VehicleType: Optional[str] = Field(None, max_length=20)
    Area_assigned: Optional[str] = Field(None, max_length=50)

class DeliveryPersonResponse(BaseModel):
    DeliveryPerson_ID: int
    Name: str
    Phone_Num: str
    User_Name: Optional[str] = None
    VehicleType: Optional[str] = None
    Area_assigned: Optional[str] = None
    class Config:
        from_attributes = True

# ==================== LOGIN ====================
class LoginRequest(BaseModel):
    User_Name: str = Field(..., min_length=1, max_length=50)
    Password: str = Field(..., min_length=4, max_length=100)
    Role: Optional[Literal['admin', 'customer', 'supplier', 'delivery']] = None

class LoginResponse(BaseModel):
    id: int
    role: Literal['admin', 'customer', 'supplier', 'delivery']
    name: str

# ==================== ORDER ====================
class OrderBase(BaseModel):
    Customer_ID: int
    Order_date: date
    Order_status: Literal['Pending', 'Processing', 'Delivered', 'Failed', 'Cancelled'] = 'Pending'
    Total_amount: float

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    Customer_ID: Optional[int] = None
    Order_date: Optional[date] = None
    Order_status: Optional[Literal['Pending', 'Processing', 'Delivered', 'Failed', 'Cancelled']] = None
    Total_amount: Optional[float] = None

class OrderResponse(OrderBase):
    Order_ID: int
    class Config:
        from_attributes = True

# ==================== ORDER ITEM ====================
class OrderItemBase(BaseModel):
    Order_ID: int
    Product_ID: int
    Quantity: int
    Price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    Order_ID: Optional[int] = None
    Product_ID: Optional[int] = None
    Quantity: Optional[int] = None
    Price: Optional[float] = None

class OrderItemResponse(OrderItemBase):
    class Config:
        from_attributes = True

# ==================== PAYMENT ====================
class PaymentBase(BaseModel):
    Order_ID: int
    Amount: float
    Payment_method: str = Field(..., max_length=20)
    Payment_status: Literal['Paid', 'Pending', 'Completed', 'Failed'] = 'Pending'
    Payment_Date: Optional[date] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    Order_ID: Optional[int] = None
    Amount: Optional[float] = None
    Payment_method: Optional[str] = Field(None, max_length=20)
    Payment_status: Optional[Literal['Paid', 'Pending', 'Completed', 'Failed']] = None
    Payment_Date: Optional[date] = None

class PaymentResponse(PaymentBase):
    Payment_ID: int
    class Config:
        from_attributes = True

# ==================== DELIVERY ====================
class DeliveryBase(BaseModel):
    Order_ID: int
    DeliveryPerson_ID: int
    Delivery_date: date
    Delivery_Status: Literal['Pending', 'Scheduled', 'Out for Delivery', 'Delivered', 'Failed'] = 'Pending'

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryUpdate(BaseModel):
    Order_ID: Optional[int] = None
    DeliveryPerson_ID: Optional[int] = None
    Delivery_date: Optional[date] = None
    Delivery_Status: Optional[Literal['Pending', 'Scheduled', 'Out for Delivery', 'Delivered', 'Failed']] = None

class DeliveryResponse(DeliveryBase):
    Delivery_ID: int
    class Config:
        from_attributes = True

# ==================== DELIVERY SCHEDULE ====================
class DeliveryScheduleBase(BaseModel):
    Delivery_ID: int
    Scheduled_date: date
    Time_slot: str = Field(..., max_length=20)
    Schedule_status: str = Field(..., max_length=20)

class DeliveryScheduleCreate(DeliveryScheduleBase):
    pass

class DeliveryScheduleUpdate(BaseModel):
    Delivery_ID: Optional[int] = None
    Scheduled_date: Optional[date] = None
    Time_slot: Optional[str] = Field(None, max_length=20)
    Schedule_status: Optional[str] = Field(None, max_length=20)

class DeliveryScheduleResponse(DeliveryScheduleBase):
    Schedule_ID: int
    class Config:
        from_attributes = True

# ==================== SUPPLIER PRODUCT ====================
class SupplierProductBase(BaseModel):
    Supplier_ID: int
    Product_ID: int

class SupplierProductCreate(SupplierProductBase):
    pass

class SupplierProductResponse(SupplierProductBase):
    ID: int
    class Config:
        from_attributes = True

# ==================== GENERIC ====================
class MessageResponse(BaseModel):
    message: str
    success: bool = True
