from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from database import get_db
from models import (
    Admin, Customer, Supplier, Product, Inventory, Subscription, SubscriptionDetail,
    DeliveryPerson, Order, OrderItem, Payment, Delivery, DeliverySchedule,
    SupplierProduct
)
from schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse,
    SupplierCreate, SupplierUpdate, SupplierResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    InventoryCreate, InventoryUpdate, InventoryResponse,
    SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse,
    SubscriptionDetailCreate, SubscriptionDetailUpdate, SubscriptionDetailResponse,
    DeliveryPersonCreate, DeliveryPersonUpdate, DeliveryPersonResponse,
    OrderCreate, OrderUpdate, OrderResponse,
    OrderItemCreate, OrderItemUpdate, OrderItemResponse,
    PaymentCreate, PaymentUpdate, PaymentResponse,
    DeliveryCreate, DeliveryUpdate, DeliveryResponse,
    DeliveryScheduleCreate, DeliveryScheduleUpdate, DeliveryScheduleResponse,
    SupplierProductCreate, SupplierProductResponse,
    LoginRequest, LoginResponse,
    MessageResponse
)

load_dotenv()

app = FastAPI(title="FreshDeliver API", version="1.0.0")

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:8080,http://192.168.1.27:8080").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== HELPER: Auto-generate next integer ID ====================
def generate_next_id(db: Session, model, id_column) -> int:
    last = db.query(id_column).order_by(id_column.desc()).first()
    return (last[0] + 1) if last else 1


def normalize_username(value: str) -> str:
    return ''.join(ch.lower() for ch in str(value or '').strip() if ch.isalnum())


def generate_unique_username(db: Session, model, name: str, fallback: str) -> str:
    base = normalize_username(name.split()[0] if name else '') or normalize_username(fallback) or 'user'
    username = base
    suffix = 1
    while db.query(model).filter(model.User_Name == username).first():
        username = f"{base}{suffix}"
        suffix += 1
    return username


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "FreshDeliver API is running", "version": "1.0.0"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ==================== AUTHENTICATION ====================
@app.post("/api/login", response_model=LoginResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    print("Login attempt:", login_request)
    if login_request.Role == 'admin':
        admin = db.query(Admin).filter(Admin.User_Name == login_request.User_Name, Admin.Password == login_request.Password).first()
        if admin:
            return LoginResponse(id=admin.Admin_ID, role='admin', name=admin.Name or admin.User_Name)
    elif login_request.Role == 'customer':
        customer = db.query(Customer).filter(Customer.User_Name == login_request.User_Name, Customer.Password == login_request.Password).first()
        if customer:
            return LoginResponse(id=customer.Customer_ID, role='customer', name=customer.Name)
    elif login_request.Role == 'supplier':
        supplier = db.query(Supplier).filter(Supplier.User_Name == login_request.User_Name, Supplier.Password == login_request.Password).first()
        if supplier:
            return LoginResponse(id=supplier.Supplier_ID, role='supplier', name=supplier.Supplier_Name)
    elif login_request.Role == 'delivery':
        delivery_person = db.query(DeliveryPerson).filter(DeliveryPerson.User_Name == login_request.User_Name, DeliveryPerson.Password == login_request.Password).first()
        if delivery_person:
            return LoginResponse(id=delivery_person.DeliveryPerson_ID, role='delivery', name=delivery_person.Name)
    else:
        admin = db.query(Admin).filter(Admin.User_Name == login_request.User_Name, Admin.Password == login_request.Password).first()
        if admin:
            return LoginResponse(id=admin.Admin_ID, role='admin', name=admin.Name or admin.User_Name)
        customer = db.query(Customer).filter(Customer.User_Name == login_request.User_Name, Customer.Password == login_request.Password).first()
        if customer:
            return LoginResponse(id=customer.Customer_ID, role='customer', name=customer.Name)
        supplier = db.query(Supplier).filter(Supplier.User_Name == login_request.User_Name, Supplier.Password == login_request.Password).first()
        if supplier:
            return LoginResponse(id=supplier.Supplier_ID, role='supplier', name=supplier.Supplier_Name)
        delivery_person = db.query(DeliveryPerson).filter(DeliveryPerson.User_Name == login_request.User_Name, DeliveryPerson.Password == login_request.Password).first()
        if delivery_person:
            return LoginResponse(id=delivery_person.DeliveryPerson_ID, role='delivery', name=delivery_person.Name)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# ==================== CUSTOMER ENDPOINTS ====================

@app.get("/api/customers", response_model=List[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@app.get("/api/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.Customer_ID == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/api/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    if db.query(Customer).filter(Customer.Phone_Num == customer.Phone_Num).first():
        raise HTTPException(status_code=400, detail="Phone number already registered")
    payload = customer.model_dump()
    payload['User_Name'] = payload.get('User_Name') or generate_unique_username(db, Customer, customer.Name, customer.Phone_Num)
    payload['Password'] = payload.get('Password') or customer.Phone_Num or 'changeme123'
    if db.query(Customer).filter(Customer.User_Name == payload['User_Name']).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    new_id = generate_next_id(db, Customer, Customer.Customer_ID)
    db_customer = Customer(Customer_ID=new_id, **payload)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.put("/api/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.Customer_ID == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer.Phone_Num and customer.Phone_Num != db_customer.Phone_Num:
        existing = db.query(Customer).filter(Customer.Phone_Num == customer.Phone_Num).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone number already registered")
    if customer.User_Name and customer.User_Name != db_customer.User_Name:
        existing = db.query(Customer).filter(Customer.User_Name == customer.User_Name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already registered")
    for field, value in customer.model_dump(exclude_unset=True).items():
        setattr(db_customer, field, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.delete("/api/customers/{customer_id}", response_model=MessageResponse)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.Customer_ID == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return MessageResponse(message="Customer deleted successfully")


# ==================== SUPPLIER ENDPOINTS ====================

@app.get("/api/suppliers", response_model=List[SupplierResponse])
def get_all_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@app.get("/api/suppliers/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.Supplier_ID == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@app.post("/api/suppliers", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    payload = supplier.model_dump()
    payload['User_Name'] = payload.get('User_Name') or generate_unique_username(db, Supplier, supplier.Supplier_Name, supplier.Phone_Num)
    payload['Password'] = payload.get('Password') or supplier.Phone_Num or 'changeme123'
    if db.query(Supplier).filter(Supplier.User_Name == payload['User_Name']).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    new_id = generate_next_id(db, Supplier, Supplier.Supplier_ID)
    db_supplier = Supplier(Supplier_ID=new_id, **payload)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@app.put("/api/suppliers/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    db_supplier = db.query(Supplier).filter(Supplier.Supplier_ID == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    if supplier.User_Name and supplier.User_Name != db_supplier.User_Name:
        existing = db.query(Supplier).filter(Supplier.User_Name == supplier.User_Name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already registered")
    for field, value in supplier.model_dump(exclude_unset=True).items():
        setattr(db_supplier, field, value)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@app.delete("/api/suppliers/{supplier_id}", response_model=MessageResponse)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = db.query(Supplier).filter(Supplier.Supplier_ID == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(db_supplier)
    db.commit()
    return MessageResponse(message="Supplier deleted successfully")


# ==================== PRODUCT ENDPOINTS ====================

@app.get("/api/products", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/api/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.Product_ID == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_id = generate_next_id(db, Product, Product.Product_ID)
    db_product = Product(Product_ID=new_id, **product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/api/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.Product_ID == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}", response_model=MessageResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.Product_ID == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return MessageResponse(message="Product deleted successfully")


# ==================== INVENTORY ENDPOINTS ====================

@app.get("/api/inventory", response_model=List[InventoryResponse])
def get_all_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()

@app.get("/api/inventory/{inventory_id}", response_model=InventoryResponse)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inv = db.query(Inventory).filter(Inventory.Inventory_ID == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return inv

@app.post("/api/inventory", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    new_id = generate_next_id(db, Inventory, Inventory.Inventory_ID)
    db_inv = Inventory(Inventory_ID=new_id, **inventory.model_dump())
    db.add(db_inv)
    db.commit()
    db.refresh(db_inv)
    return db_inv

@app.put("/api/inventory/{inventory_id}", response_model=InventoryResponse)
def update_inventory(inventory_id: int, inventory: InventoryUpdate, db: Session = Depends(get_db)):
    db_inv = db.query(Inventory).filter(Inventory.Inventory_ID == inventory_id).first()
    if not db_inv:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    for field, value in inventory.model_dump(exclude_unset=True).items():
        setattr(db_inv, field, value)
    db.commit()
    db.refresh(db_inv)
    return db_inv

@app.delete("/api/inventory/{inventory_id}", response_model=MessageResponse)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    db_inv = db.query(Inventory).filter(Inventory.Inventory_ID == inventory_id).first()
    if not db_inv:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    db.delete(db_inv)
    db.commit()
    return MessageResponse(message="Inventory record deleted successfully")


# ==================== SUBSCRIPTION ENDPOINTS ====================

@app.get("/api/subscriptions", response_model=List[SubscriptionResponse])
def get_all_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).all()

@app.get("/api/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.Subscription_ID == subscription_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub

@app.post("/api/subscriptions", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    new_id = generate_next_id(db, Subscription, Subscription.Subscription_ID)
    db_sub = Subscription(Subscription_ID=new_id, **subscription.model_dump())
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@app.put("/api/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(subscription_id: int, subscription: SubscriptionUpdate, db: Session = Depends(get_db)):
    db_sub = db.query(Subscription).filter(Subscription.Subscription_ID == subscription_id).first()
    if not db_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    for field, value in subscription.model_dump(exclude_unset=True).items():
        setattr(db_sub, field, value)
    db.commit()
    db.refresh(db_sub)
    return db_sub

@app.delete("/api/subscriptions/{subscription_id}", response_model=MessageResponse)
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    db_sub = db.query(Subscription).filter(Subscription.Subscription_ID == subscription_id).first()
    if not db_sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    db.delete(db_sub)
    db.commit()
    return MessageResponse(message="Subscription deleted successfully")


# ==================== SUBSCRIPTION DETAIL ENDPOINTS ====================

@app.get("/api/subscription-details", response_model=List[SubscriptionDetailResponse])
def get_all_subscription_details(db: Session = Depends(get_db)):
    return db.query(SubscriptionDetail).all()

@app.get("/api/subscription-details/{subscription_id}/{product_id}", response_model=SubscriptionDetailResponse)
def get_subscription_detail(subscription_id: int, product_id: int, db: Session = Depends(get_db)):
    detail = db.query(SubscriptionDetail).filter(
        SubscriptionDetail.Subscription_ID == subscription_id,
        SubscriptionDetail.Product_ID == product_id
    ).first()
    if not detail:
        raise HTTPException(status_code=404, detail="Subscription detail not found")
    return detail

@app.post("/api/subscription-details", response_model=SubscriptionDetailResponse, status_code=status.HTTP_201_CREATED)
def create_subscription_detail(detail: SubscriptionDetailCreate, db: Session = Depends(get_db)):
    db_detail = SubscriptionDetail(**detail.model_dump())
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

@app.put("/api/subscription-details/{subscription_id}/{product_id}", response_model=SubscriptionDetailResponse)
def update_subscription_detail(subscription_id: int, product_id: int, detail: SubscriptionDetailUpdate, db: Session = Depends(get_db)):
    db_detail = db.query(SubscriptionDetail).filter(
        SubscriptionDetail.Subscription_ID == subscription_id,
        SubscriptionDetail.Product_ID == product_id
    ).first()
    if not db_detail:
        raise HTTPException(status_code=404, detail="Subscription detail not found")
    for field, value in detail.model_dump(exclude_unset=True).items():
        setattr(db_detail, field, value)
    db.commit()
    db.refresh(db_detail)
    return db_detail

@app.delete("/api/subscription-details/{subscription_id}/{product_id}", response_model=MessageResponse)
def delete_subscription_detail(subscription_id: int, product_id: int, db: Session = Depends(get_db)):
    db_detail = db.query(SubscriptionDetail).filter(
        SubscriptionDetail.Subscription_ID == subscription_id,
        SubscriptionDetail.Product_ID == product_id
    ).first()
    if not db_detail:
        raise HTTPException(status_code=404, detail="Subscription detail not found")
    db.delete(db_detail)
    db.commit()
    return MessageResponse(message="Subscription detail deleted successfully")


# ==================== DELIVERY PERSON ENDPOINTS ====================

@app.get("/api/delivery-persons", response_model=List[DeliveryPersonResponse])
def get_all_delivery_persons(db: Session = Depends(get_db)):
    return db.query(DeliveryPerson).all()

@app.get("/api/delivery-persons/{person_id}", response_model=DeliveryPersonResponse)
def get_delivery_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(DeliveryPerson).filter(DeliveryPerson.DeliveryPerson_ID == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    return person

@app.post("/api/delivery-persons", response_model=DeliveryPersonResponse, status_code=status.HTTP_201_CREATED)
def create_delivery_person(person: DeliveryPersonCreate, db: Session = Depends(get_db)):
    payload = person.model_dump()
    payload['User_Name'] = payload.get('User_Name') or generate_unique_username(db, DeliveryPerson, person.Name, person.Phone_Num)
    payload['Password'] = payload.get('Password') or person.Phone_Num or 'changeme123'
    if db.query(DeliveryPerson).filter(DeliveryPerson.User_Name == payload['User_Name']).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    new_id = generate_next_id(db, DeliveryPerson, DeliveryPerson.DeliveryPerson_ID)
    db_person = DeliveryPerson(DeliveryPerson_ID=new_id, **payload)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.put("/api/delivery-persons/{person_id}", response_model=DeliveryPersonResponse)
def update_delivery_person(person_id: int, person: DeliveryPersonUpdate, db: Session = Depends(get_db)):
    db_person = db.query(DeliveryPerson).filter(DeliveryPerson.DeliveryPerson_ID == person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    for field, value in person.model_dump(exclude_unset=True).items():
        setattr(db_person, field, value)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.delete("/api/delivery-persons/{person_id}", response_model=MessageResponse)
def delete_delivery_person(person_id: int, db: Session = Depends(get_db)):
    db_person = db.query(DeliveryPerson).filter(DeliveryPerson.DeliveryPerson_ID == person_id).first()
    if not db_person:
        raise HTTPException(status_code=404, detail="Delivery person not found")
    db.delete(db_person)
    db.commit()
    return MessageResponse(message="Delivery person deleted successfully")


# ==================== ORDER ENDPOINTS ====================

@app.get("/api/orders", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.Order_ID == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/api/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_id = generate_next_id(db, Order, Order.Order_ID)
    db_order = Order(Order_ID=new_id, **order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.put("/api/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.Order_ID == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for field, value in order.model_dump(exclude_unset=True).items():
        setattr(db_order, field, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/api/orders/{order_id}", response_model=MessageResponse)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.Order_ID == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return MessageResponse(message="Order deleted successfully")


# ==================== ORDER ITEM ENDPOINTS ====================

@app.get("/api/order-items", response_model=List[OrderItemResponse])
def get_all_order_items(db: Session = Depends(get_db)):
    return db.query(OrderItem).all()

@app.get("/api/order-items/{order_id}/{product_id}", response_model=OrderItemResponse)
def get_order_item(order_id: int, product_id: int, db: Session = Depends(get_db)):
    item = db.query(OrderItem).filter(
        OrderItem.Order_ID == order_id,
        OrderItem.Product_ID == product_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return item

@app.post("/api/order-items", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def create_order_item(item: OrderItemCreate, db: Session = Depends(get_db)):
    db_item = OrderItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/api/order-items/{order_id}/{product_id}", response_model=OrderItemResponse)
def update_order_item(order_id: int, product_id: int, item: OrderItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(OrderItem).filter(
        OrderItem.Order_ID == order_id,
        OrderItem.Product_ID == product_id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    for field, value in item.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/api/order-items/{order_id}/{product_id}", response_model=MessageResponse)
def delete_order_item(order_id: int, product_id: int, db: Session = Depends(get_db)):
    db_item = db.query(OrderItem).filter(
        OrderItem.Order_ID == order_id,
        OrderItem.Product_ID == product_id
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    db.delete(db_item)
    db.commit()
    return MessageResponse(message="Order item deleted successfully")


# ==================== PAYMENT ENDPOINTS ====================

@app.get("/api/payments", response_model=List[PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()

@app.get("/api/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.Payment_ID == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.post("/api/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    new_id = generate_next_id(db, Payment, Payment.Payment_ID)
    db_payment = Payment(Payment_ID=new_id, **payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.put("/api/payments/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.Payment_ID == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    for field, value in payment.model_dump(exclude_unset=True).items():
        setattr(db_payment, field, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.delete("/api/payments/{payment_id}", response_model=MessageResponse)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.Payment_ID == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(db_payment)
    db.commit()
    return MessageResponse(message="Payment deleted successfully")


# ==================== DELIVERY ENDPOINTS ====================

@app.get("/api/deliveries", response_model=List[DeliveryResponse])
def get_all_deliveries(db: Session = Depends(get_db)):
    return db.query(Delivery).all()

@app.get("/api/deliveries/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(Delivery).filter(Delivery.Delivery_ID == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

@app.post("/api/deliveries", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    new_id = generate_next_id(db, Delivery, Delivery.Delivery_ID)
    db_delivery = Delivery(Delivery_ID=new_id, **delivery.model_dump())
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@app.put("/api/deliveries/{delivery_id}", response_model=DeliveryResponse)
def update_delivery(delivery_id: int, delivery: DeliveryUpdate, db: Session = Depends(get_db)):
    db_delivery = db.query(Delivery).filter(Delivery.Delivery_ID == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    for field, value in delivery.model_dump(exclude_unset=True).items():
        setattr(db_delivery, field, value)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

@app.delete("/api/deliveries/{delivery_id}", response_model=MessageResponse)
def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    db_delivery = db.query(Delivery).filter(Delivery.Delivery_ID == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    db.delete(db_delivery)
    db.commit()
    return MessageResponse(message="Delivery deleted successfully")


# ==================== DELIVERY SCHEDULE ENDPOINTS ====================

@app.get("/api/delivery-schedules", response_model=List[DeliveryScheduleResponse])
def get_all_delivery_schedules(db: Session = Depends(get_db)):
    return db.query(DeliverySchedule).all()

@app.get("/api/delivery-schedules/{schedule_id}", response_model=DeliveryScheduleResponse)
def get_delivery_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(DeliverySchedule).filter(DeliverySchedule.Schedule_ID == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Delivery schedule not found")
    return schedule

@app.post("/api/delivery-schedules", response_model=DeliveryScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_delivery_schedule(schedule: DeliveryScheduleCreate, db: Session = Depends(get_db)):
    new_id = generate_next_id(db, DeliverySchedule, DeliverySchedule.Schedule_ID)
    db_schedule = DeliverySchedule(Schedule_ID=new_id, **schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@app.put("/api/delivery-schedules/{schedule_id}", response_model=DeliveryScheduleResponse)
def update_delivery_schedule(schedule_id: int, schedule: DeliveryScheduleUpdate, db: Session = Depends(get_db)):
    db_schedule = db.query(DeliverySchedule).filter(DeliverySchedule.Schedule_ID == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Delivery schedule not found")
    for field, value in schedule.model_dump(exclude_unset=True).items():
        setattr(db_schedule, field, value)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@app.delete("/api/delivery-schedules/{schedule_id}", response_model=MessageResponse)
def delete_delivery_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(DeliverySchedule).filter(DeliverySchedule.Schedule_ID == schedule_id).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Delivery schedule not found")
    db.delete(db_schedule)
    db.commit()
    return MessageResponse(message="Delivery schedule deleted successfully")


# ==================== SUPPLIER PRODUCT ENDPOINTS ====================

@app.get("/api/supplier-products", response_model=List[SupplierProductResponse])
def get_all_supplier_products(db: Session = Depends(get_db)):
    return db.query(SupplierProduct).all()

@app.get("/api/supplier-products/{supplier_id}", response_model=List[SupplierProductResponse])
def get_supplier_products_by_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return db.query(SupplierProduct).filter(SupplierProduct.Supplier_ID == supplier_id).all()

@app.post("/api/supplier-products", response_model=SupplierProductResponse, status_code=status.HTTP_201_CREATED)
def create_supplier_product(sp: SupplierProductCreate, db: Session = Depends(get_db)):
    payload = sp.model_dump()
    new_id = generate_next_id(db, SupplierProduct, SupplierProduct.ID)
    payload['ID'] = new_id
    db_sp = SupplierProduct(**payload)
    db.add(db_sp)
    db.commit()
    db.refresh(db_sp)
    return db_sp

@app.delete("/api/supplier-products/{supplier_id}/{product_id}", response_model=MessageResponse)
def delete_supplier_product(supplier_id: int, product_id: int, db: Session = Depends(get_db)):
    db_sp = db.query(SupplierProduct).filter(
        SupplierProduct.Supplier_ID == supplier_id,
        SupplierProduct.Product_ID == product_id
    ).first()
    if not db_sp:
        raise HTTPException(status_code=404, detail="Supplier-product link not found")
    db.delete(db_sp)
    db.commit()
    return MessageResponse(message="Supplier-product link deleted successfully")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
