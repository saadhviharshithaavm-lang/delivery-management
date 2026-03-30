from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, Sequence, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base


# Customer Model
class Customer(Base):
    __tablename__ = "CUSTOMER"

    Customer_ID = Column(String(10), primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Phone_Num = Column(String(15), nullable=False, unique=True)
    Address = Column(String(255), nullable=False)
    Area = Column(String(50), nullable=False)
    Account_Status = Column(String(10), default='Active')

    __table_args__ = (
        CheckConstraint("Account_Status IN ('Active', 'Inactive')", name='chk_cust_status'),
    )

    # Relationships
    # subscriptions = relationship("Subscription", back_populates="customer")
    orders = relationship("Order", back_populates="customer")


# Supplier Model
class Supplier(Base):
    __tablename__ = "SUPPLIER"

    Supplier_ID = Column(String(10), primary_key=True, index=True)
    Supplier_Name = Column(String(100), nullable=False)
    Phone_Num = Column(String(15), nullable=False)

    # Relationships
    subscriptions = relationship("Subscription", back_populates="supplier")
    supplier_products = relationship("SupplierProduct", back_populates="supplier")


# Product Model
class Product(Base):
    __tablename__ = "PRODUCT"

    Product_ID = Column(String(10), primary_key=True, index=True)
    Product_Name = Column(String(100), nullable=False)
    Price_per_unit = Column(Float, nullable=False)
    Unit = Column(String(20), nullable=False)

    # Relationships
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    supplier_products = relationship("SupplierProduct", back_populates="product")
    subscription_details = relationship("SubscriptionDetail", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")


# Inventory Model
class Inventory(Base):
    __tablename__ = "INVENTORY"

    Inventory_ID = Column(String(10), primary_key=True, index=True)
    Product_ID = Column(String(10), ForeignKey("products.Product_ID"), unique=True)
    Available_quantity = Column(Integer, default=0)
    LastUpdated = Column(Date)

    # Relationships
    product = relationship("Product", back_populates="inventory")


# Subscription Model
class Subscription(Base):
    __tablename__ = "SUBSCRIPTION"

    Subscription_ID = Column(String(10), primary_key=True, index=True)
    Customer_ID = Column(String(10), ForeignKey("customers.Customer_ID"))
    Supplier_ID = Column(String(10), ForeignKey("suppliers.Supplier_ID"))
    Start_date = Column(Date)
    End_date = Column(Date)
    Status = Column(String(10), default='Active')

    __table_args__ = (
        CheckConstraint("Status IN ('Active', 'Paused', 'Cancelled')", name='chk_sub_status'),
    )

    # Relationships
    customer = relationship("Customer", back_populates="subscriptions")
    supplier = relationship("Supplier", back_populates="subscriptions")
    subscription_details = relationship("SubscriptionDetail", back_populates="subscription")


# Subscription Detail Model
class SubscriptionDetail(Base):
    __tablename__ = "SUBSCRIPTION_DETAILS"

    id = Column(Integer, Sequence('sub_detail_seq'), primary_key=True)
    Subscription_ID = Column(String(10), ForeignKey("subscriptions.Subscription_ID"))
    Product_ID = Column(String(10), ForeignKey("products.Product_ID"))
    Quantity_Per_Day = Column(Integer)
    Delivery_Frequency = Column(String(20))

    # Relationships
    subscription = relationship("Subscription", back_populates="subscription_details")
    product = relationship("Product", back_populates="subscription_details")


# Delivery Person Model
class DeliveryPerson(Base):
    __tablename__ = "DELIVERY_PERSON"

    DeliveryPerson_ID = Column(String(10), primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Phone_Num = Column(String(15), nullable=False)
    VehicleType = Column(String(50))
    Area_assigned = Column(String(50))

    # Relationships
    deliveries = relationship("Delivery", back_populates="delivery_person")


# Order Model
class Order(Base):
    __tablename__ = "CUSTOMER_ORDER"

    Order_ID = Column(String(10), primary_key=True, index=True)
    Customer_ID = Column(String(10), ForeignKey("customers.Customer_ID"))
    Order_date = Column(Date)
    Order_status = Column(String(15), default='Pending')
    Total_amount = Column(Float)

    __table_args__ = (
        CheckConstraint("Order_status IN ('Pending', 'Processing', 'Delivered', 'Cancelled')", name='chk_order_status'),
    )

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)
    delivery = relationship("Delivery", back_populates="order", uselist=False)


# Order Item Model
class OrderItem(Base):
    __tablename__ = "ORDER_ITEMS"

    id = Column(Integer, Sequence('order_item_seq'), primary_key=True)
    Order_ID = Column(String(10), ForeignKey("orders.Order_ID"))
    Product_ID = Column(String(10), ForeignKey("products.Product_ID"))
    Quantity = Column(Integer)
    Price = Column(Float)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")


# Payment Model
class Payment(Base):
    __tablename__ = "PAYMENT"

    Payment_ID = Column(String(10), primary_key=True, index=True)
    Order_ID = Column(String(10), ForeignKey("orders.Order_ID"), unique=True)
    Amount = Column(Float)
    Payment_method = Column(String(20))
    Payment_status = Column(String(10), default='Pending')
    Payment_Date = Column(Date, nullable=True)

    __table_args__ = (
        CheckConstraint("Payment_status IN ('Paid', 'Pending', 'Failed')", name='chk_pay_status'),
    )

    # Relationships
    order = relationship("Order", back_populates="payment")


# Delivery Model
class Delivery(Base):
    __tablename__ = "DELIVERY"

    Delivery_ID = Column(String(10), primary_key=True, index=True)
    Order_ID = Column(String(10), ForeignKey("orders.Order_ID"), unique=True)
    DeliveryPerson_ID = Column(String(10), ForeignKey("delivery_persons.DeliveryPerson_ID"))
    Delivery_date = Column(Date)
    Delivery_Status = Column(String(10), default='Pending')

    __table_args__ = (
        CheckConstraint("Delivery_Status IN ('Pending', 'Delivered', 'Failed')", name='chk_del_status'),
    )

    # Relationships
    order = relationship("Order", back_populates="delivery")
    delivery_person = relationship("DeliveryPerson", back_populates="deliveries")
    delivery_schedule = relationship("DeliverySchedule", back_populates="delivery", uselist=False)


# Delivery Schedule Model
class DeliverySchedule(Base):
    __tablename__ = "DELIVERY_SCHEDULE"

    Schedule_ID = Column(String(10), primary_key=True, index=True)
    Delivery_ID = Column(String(10), ForeignKey("deliveries.Delivery_ID"), unique=True)
    Scheduled_date = Column(Date)
    Time_slot = Column(String(20))
    Schedule_status = Column(String(20))

    # Relationships
    delivery = relationship("Delivery", back_populates="delivery_schedule")


# Supplier Product Junction Model
class SupplierProduct(Base):
    __tablename__ = "SUPPLIER_PRODUCT"

    id = Column(Integer, Sequence('supp_prod_seq'), primary_key=True)
    Supplier_ID = Column(String(10), ForeignKey("suppliers.Supplier_ID"))
    Product_ID = Column(String(10), ForeignKey("products.Product_ID"))

    # Relationships
    supplier = relationship("Supplier", back_populates="supplier_products")
    product = relationship("Product", back_populates="supplier_products")