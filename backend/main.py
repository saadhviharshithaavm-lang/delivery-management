from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from database import get_db
from models import Customer
from schemas import CustomerCreate, CustomerUpdate, CustomerResponse, MessageResponse

load_dotenv()

app = FastAPI(title="FreshDeliver API", version="1.0.0")

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to generate Customer ID
def generate_customer_id(db: Session) -> str:
    last_customer = db.query(Customer).order_by(Customer.Customer_ID.desc()).first()
    if last_customer:
        last_num = int(last_customer.Customer_ID.replace('C', ''))
        new_num = last_num + 1
    else:
        new_num = 1
    return f"C{new_num:03d}"

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "FreshDeliver API is running", "version": "1.0.0"}

# ==================== CUSTOMER ENDPOINTS ====================

@app.get("/api/customers", response_model=List[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):
    """Get all customers"""
    customers = db.query(Customer).all()
    return customers

@app.get("/api/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Get a specific customer by ID"""
    customer = db.query(Customer).filter(Customer.Customer_ID == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/api/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    # Check if phone number already exists
    existing = db.query(Customer).filter(Customer.Phone_Num == customer.Phone_Num).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    # Generate new customer ID
    customer_id = generate_customer_id(db)

    # Create new customer
    db_customer = Customer(
        Customer_ID=customer_id,
        **customer.model_dump()
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.put("/api/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: str, customer: CustomerUpdate, db: Session = Depends(get_db)):
    """Update an existing customer"""
    db_customer = db.query(Customer).filter(Customer.Customer_ID == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Check if phone number is being changed and already exists
    if customer.Phone_Num and customer.Phone_Num != db_customer.Phone_Num:
        existing = db.query(Customer).filter(Customer.Phone_Num == customer.Phone_Num).first()
        if existing:
            raise HTTPException(status_code=400, detail="Phone number already registered")

    # Update fields
    update_data = customer.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.delete("/api/customers/{customer_id}", response_model=MessageResponse)
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    """Delete a customer"""
    db_customer = db.query(Customer).filter(Customer.Customer_ID == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(db_customer)
    db.commit()
    return MessageResponse(message="Customer deleted successfully")

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
