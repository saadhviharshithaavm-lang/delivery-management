from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base


# Customer Model
class Customer(Base):
    __tablename__ = "CUSTOMER"

    Customer_ID = Column("CUSTOMER_ID", Integer, primary_key=True, index=True)
    Name = Column("NAME", String(50), nullable=False)
    Phone_Num = Column("PHONE_NUM", String(15), nullable=False, unique=True)
    Address = Column("ADDRESS", String(100), nullable=False)
    Area = Column("AREA", String(50), nullable=False)
    User_Name = Column("USER_NAME", String(50), nullable=False, unique=True)
    Password = Column("PASSWORD", String(100), nullable=False)
    Account_Status = Column("ACCOUNT_STATUS", String(20), default='Active')

    __table_args__ = (
        CheckConstraint("ACCOUNT_STATUS IN ('Active', 'Inactive')", name='chk_cust_status'),
    )


# Supplier Model
class Supplier(Base):
    __tablename__ = "SUPPLIER"

    Supplier_ID = Column("SUPPLIER_ID", Integer, primary_key=True, index=True)
    Supplier_Name = Column("SUPPLIER_NAME", String(50), nullable=False)
    Phone_Num = Column("PHONE_NUM", String(15), nullable=False)
    User_Name = Column("USER_NAME", String(50), nullable=False, unique=True)
    Password = Column("PASSWORD", String(100), nullable=False)


# Admin Model
class Admin(Base):
    __tablename__ = "ADMIN"

    Admin_ID = Column("ADMIN_ID", Integer, primary_key=True, index=True)
    User_Name = Column("USER_NAME", String(50), nullable=False, unique=True)
    Password = Column("PASSWORD", String(100), nullable=False)
    Name = Column("NAME", String(50), nullable=True)


# Product Model
class Product(Base):
    __tablename__ = "PRODUCT"

    Product_ID = Column("PRODUCT_ID", Integer, primary_key=True, index=True)
    Product_Name = Column("PRODUCT_NAME", String(50), nullable=False)
    Price_per_unit = Column("PRICE_PER_UNIT", Float, nullable=False)
    Unit = Column("UNIT", String(20), nullable=False)


# Inventory Model
class Inventory(Base):
    __tablename__ = "INVENTORY"

    Inventory_ID = Column("INVENTORY_ID", Integer, primary_key=True, index=True)
    Product_ID = Column("PRODUCT_ID", Integer, ForeignKey("PRODUCT.PRODUCT_ID"))
    Supplier_ID = Column("SUPPLIER_ID", Integer, ForeignKey("SUPPLIER.SUPPLIER_ID"))
    Available_quantity = Column("AVAILABLE_QUANTITY", Integer, default=0)
    LastUpdated = Column("LASTUPDATED", Date)

    # __table_args__ = (
    #     UniqueConstraint('Product_ID', 'Supplier_ID', name='unique_product_supplier_inventory'),
    # )


# Subscription Model
class Subscription(Base):
    __tablename__ = "SUBSCRIPTION"

    Subscription_ID = Column("SUBSCRIPTION_ID", Integer, primary_key=True, index=True)
    Customer_ID = Column("CUSTOMER_ID", Integer, ForeignKey("CUSTOMER.CUSTOMER_ID"))
    Supplier_ID = Column("SUPPLIER_ID", Integer, ForeignKey("SUPPLIER.SUPPLIER_ID"))
    Start_date = Column("START_DATE", Date)
    End_date = Column("END_DATE", Date)
    Status = Column("STATUS", String(10), default='Active')

    __table_args__ = (
        CheckConstraint("STATUS IN ('Active', 'Paused', 'Cancelled')", name='chk_sub_status'),
    )


# Subscription Detail Model
class SubscriptionDetail(Base):
    __tablename__ = "SUBSCRIPTION_DETAILS"

    Subscription_ID = Column("SUBSCRIPTION_ID", Integer, ForeignKey("SUBSCRIPTION.SUBSCRIPTION_ID"), primary_key=True)
    Product_ID = Column("PRODUCT_ID", Integer, ForeignKey("PRODUCT.PRODUCT_ID"), primary_key=True)
    Quantity_Per_Day = Column("QUANTITY_PER_DAY", Integer)
    Delivery_Frequency = Column("DELIVERY_FREQUENCY", String(20))


# Delivery Person Model
class DeliveryPerson(Base):
    __tablename__ = "DELIVERY_PERSON"

    DeliveryPerson_ID = Column("DELIVERYPERSON_ID", Integer, primary_key=True, index=True)
    Name = Column("NAME", String(50), nullable=False)
    Phone_Num = Column("PHONE_NUM", String(15), nullable=False)
    User_Name = Column("USER_NAME", String(50), nullable=False, unique=True)
    Password = Column("PASSWORD", String(100), nullable=False)
    VehicleType = Column("VEHICLETYPE", String(20))
    Area_assigned = Column("AREA_ASSIGNED", String(50))


# Order Model
class Order(Base):
    __tablename__ = "CUSTOMER_ORDER"

    Order_ID = Column("ORDER_ID", Integer, primary_key=True, index=True)
    Customer_ID = Column("CUSTOMER_ID", Integer, ForeignKey("CUSTOMER.CUSTOMER_ID"))
    Order_date = Column("ORDER_DATE", Date)
    Order_status = Column("ORDER_STATUS", String(20), default='Pending')
    Total_amount = Column("TOTAL_AMOUNT", Float)

    __table_args__ = (
        CheckConstraint("ORDER_STATUS IN ('Pending', 'Processing', 'Delivered', 'Failed','Cancelled')", name='chk_order_status'),
    )


# Order Item Model
class OrderItem(Base):
    __tablename__ = "ORDER_ITEMS"

    Order_ID = Column("ORDER_ID", Integer, ForeignKey("CUSTOMER_ORDER.ORDER_ID"), primary_key=True)
    Product_ID = Column("PRODUCT_ID", Integer, ForeignKey("PRODUCT.PRODUCT_ID"), primary_key=True)
    Quantity = Column("QUANTITY", Integer)
    Price = Column("PRICE", Float)


# Payment Model
class Payment(Base):
    __tablename__ = "PAYMENT"

    Payment_ID = Column("PAYMENT_ID", Integer, primary_key=True, index=True)
    Order_ID = Column("ORDER_ID", Integer, ForeignKey("CUSTOMER_ORDER.ORDER_ID"), unique=True)
    Amount = Column("AMOUNT", Float)
    Payment_method = Column("PAYMENT_METHOD", String(20))
    Payment_status = Column("PAYMENT_STATUS", String(10), default='Pending')
    Payment_Date = Column("PAYMENT_DATE", Date, nullable=True)

    __table_args__ = (
        CheckConstraint("PAYMENT_STATUS IN ('Paid', 'Pending', 'Failed')", name='chk_pay_status'),
    )


# Delivery Model
class Delivery(Base):
    __tablename__ = "DELIVERY"

    Delivery_ID = Column("DELIVERY_ID", Integer, primary_key=True, index=True)
    Order_ID = Column("ORDER_ID", Integer, ForeignKey("CUSTOMER_ORDER.ORDER_ID"), unique=True)
    DeliveryPerson_ID = Column("DELIVERYPERSON_ID", Integer, ForeignKey("DELIVERY_PERSON.DELIVERYPERSON_ID"))
    Delivery_date = Column("DELIVERY_DATE", Date)
    Delivery_Status = Column("DELIVERY_STATUS", String(10), default='Pending')

    __table_args__ = (
        CheckConstraint("DELIVERY_STATUS IN ('Pending', 'Delivered', 'Failed')", name='chk_del_status'),
    )


# Supplier Product Model (Junction Table)
class SupplierProduct(Base):
    __tablename__ = "SUPPLIER_PRODUCT"

    ID = Column("ID", Integer, primary_key=True, index=True)
    Supplier_ID = Column("SUPPLIER_ID", Integer, ForeignKey("SUPPLIER.SUPPLIER_ID"))
    Product_ID = Column("PRODUCT_ID", Integer, ForeignKey("PRODUCT.PRODUCT_ID"))


# Delivery Schedule Model
class DeliverySchedule(Base):
    __tablename__ = "DELIVERY_SCHEDULE"

    Schedule_ID = Column("SCHEDULE_ID", Integer, primary_key=True, index=True)
    Delivery_ID = Column("DELIVERY_ID", Integer, ForeignKey("DELIVERY.DELIVERY_ID"), unique=True)
    Scheduled_date = Column("SCHEDULED_DATE", Date)
    Time_slot = Column("TIME_SLOT", String(20))
    Schedule_status = Column("SCHEDULE_STATUS", String(20))
