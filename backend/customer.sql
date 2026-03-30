-- FreshDeliver Database Schema
-- Customer and related tables

-- Create Database
CREATE DATABASE IF NOT EXISTS freshdeliver;
USE freshdeliver;

-- ==================== CUSTOMERS TABLE ====================
CREATE TABLE IF NOT EXISTS customers (
    Customer_ID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Phone_Num VARCHAR(15) NOT NULL UNIQUE,
    Address VARCHAR(255) NOT NULL,
    Area VARCHAR(50) NOT NULL,
    Account_Status ENUM('Active', 'Inactive') DEFAULT 'Active',
    INDEX idx_area (Area),
    INDEX idx_status (Account_Status),
    INDEX idx_phone (Phone_Num)
);

-- ==================== SUPPLIERS TABLE ====================
CREATE TABLE IF NOT EXISTS suppliers (
    Supplier_ID VARCHAR(10) PRIMARY KEY,
    Supplier_Name VARCHAR(100) NOT NULL,
    Phone_Num VARCHAR(15) NOT NULL
);

-- ==================== PRODUCTS TABLE ====================
CREATE TABLE IF NOT EXISTS products (
    Product_ID VARCHAR(10) PRIMARY KEY,
    Product_Name VARCHAR(100) NOT NULL,
    Price_per_unit DECIMAL(10, 2) NOT NULL,
    Unit VARCHAR(20) NOT NULL,
    INDEX idx_name (Product_Name)
);

-- ==================== INVENTORY TABLE ====================
CREATE TABLE IF NOT EXISTS inventory (
    Inventory_ID VARCHAR(10) PRIMARY KEY,
    Product_ID VARCHAR(10) UNIQUE NOT NULL,
    Available_quantity INT DEFAULT 0,
    LastUpdated DATE,
    FOREIGN KEY (Product_ID) REFERENCES products(Product_ID) ON DELETE CASCADE
);

-- ==================== SUBSCRIPTIONS TABLE ====================
CREATE TABLE IF NOT EXISTS subscriptions (
    Subscription_ID VARCHAR(10) PRIMARY KEY,
    Customer_ID VARCHAR(10) NOT NULL,
    Supplier_ID VARCHAR(10) NOT NULL,
    Start_date DATE NOT NULL,
    End_date DATE NOT NULL,
    Status ENUM('Active', 'Paused', 'Cancelled') DEFAULT 'Active',
    FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID) ON DELETE CASCADE,
    FOREIGN KEY (Supplier_ID) REFERENCES suppliers(Supplier_ID) ON DELETE CASCADE,
    INDEX idx_customer (Customer_ID),
    INDEX idx_status (Status)
);

-- ==================== SUBSCRIPTION DETAILS TABLE ====================
CREATE TABLE IF NOT EXISTS subscription_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Subscription_ID VARCHAR(10) NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Quantity_Per_Day INT NOT NULL,
    Delivery_Frequency VARCHAR(20) NOT NULL,
    FOREIGN KEY (Subscription_ID) REFERENCES subscriptions(Subscription_ID) ON DELETE CASCADE,
    FOREIGN KEY (Product_ID) REFERENCES products(Product_ID) ON DELETE CASCADE
);

-- ==================== DELIVERY PERSONS TABLE ====================
CREATE TABLE IF NOT EXISTS delivery_persons (
    DeliveryPerson_ID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Phone_Num VARCHAR(15) NOT NULL,
    VehicleType VARCHAR(50),
    Area_assigned VARCHAR(50),
    INDEX idx_area (Area_assigned)
);

-- ==================== ORDERS TABLE ====================
CREATE TABLE IF NOT EXISTS orders (
    Order_ID VARCHAR(10) PRIMARY KEY,
    Customer_ID VARCHAR(10) NOT NULL,
    Order_date DATE NOT NULL,
    Order_status ENUM('Pending', 'Processing', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    Total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID) ON DELETE CASCADE,
    INDEX idx_customer (Customer_ID),
    INDEX idx_status (Order_status),
    INDEX idx_date (Order_date)
);

-- ==================== ORDER ITEMS TABLE ====================
CREATE TABLE IF NOT EXISTS order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Order_ID VARCHAR(10) NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Order_ID) REFERENCES orders(Order_ID) ON DELETE CASCADE,
    FOREIGN KEY (Product_ID) REFERENCES products(Product_ID) ON DELETE CASCADE
);

-- ==================== PAYMENTS TABLE ====================
CREATE TABLE IF NOT EXISTS payments (
    Payment_ID VARCHAR(10) PRIMARY KEY,
    Order_ID VARCHAR(10) UNIQUE NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    Payment_method VARCHAR(20) NOT NULL,
    Payment_status ENUM('Paid', 'Pending', 'Failed') DEFAULT 'Pending',
    Payment_Date DATE,
    FOREIGN KEY (Order_ID) REFERENCES orders(Order_ID) ON DELETE CASCADE
);

-- ==================== DELIVERIES TABLE ====================
CREATE TABLE IF NOT EXISTS deliveries (
    Delivery_ID VARCHAR(10) PRIMARY KEY,
    Order_ID VARCHAR(10) UNIQUE NOT NULL,
    DeliveryPerson_ID VARCHAR(10) NOT NULL,
    Delivery_date DATE NOT NULL,
    Delivery_Status ENUM('Pending', 'Delivered', 'Failed') DEFAULT 'Pending',
    FOREIGN KEY (Order_ID) REFERENCES orders(Order_ID) ON DELETE CASCADE,
    FOREIGN KEY (DeliveryPerson_ID) REFERENCES delivery_persons(DeliveryPerson_ID) ON DELETE CASCADE,
    INDEX idx_status (Delivery_Status),
    INDEX idx_person (DeliveryPerson_ID)
);

-- ==================== DELIVERY SCHEDULES TABLE ====================
CREATE TABLE IF NOT EXISTS delivery_schedules (
    Schedule_ID VARCHAR(10) PRIMARY KEY,
    Delivery_ID VARCHAR(10) UNIQUE NOT NULL,
    Scheduled_date DATE NOT NULL,
    Time_slot VARCHAR(20) NOT NULL,
    Schedule_status VARCHAR(20) NOT NULL,
    FOREIGN KEY (Delivery_ID) REFERENCES deliveries(Delivery_ID) ON DELETE CASCADE
);

-- ==================== SUPPLIER PRODUCTS JUNCTION TABLE ====================
CREATE TABLE IF NOT EXISTS supplier_products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Supplier_ID VARCHAR(10) NOT NULL,
    Product_ID VARCHAR(10) NOT NULL,
    FOREIGN KEY (Supplier_ID) REFERENCES suppliers(Supplier_ID) ON DELETE CASCADE,
    FOREIGN KEY (Product_ID) REFERENCES products(Product_ID) ON DELETE CASCADE,
    UNIQUE KEY unique_supplier_product (Supplier_ID, Product_ID)
);

-- ==================== SEED DATA FOR CUSTOMERS ====================
INSERT INTO customers (Customer_ID, Name, Phone_Num, Address, Area, Account_Status) VALUES
('C001', 'Priya Sharma', '9876543210', '12, Green Park, Near Market', 'Koramangala', 'Active'),
('C002', 'Ramesh Patel', '9812345678', '45, Lakeview Apartments', 'Indiranagar', 'Active'),
('C003', 'Meena Iyer', '9123456780', '7, Sunflower Colony', 'Whitefield', 'Active'),
('C004', 'Anil Verma', '9234567891', '3, MG Road, Block B', 'Koramangala', 'Inactive'),
('C005', 'Sunita Reddy', '9345678902', '88, HSR Layout, 4th Sector', 'HSR Layout', 'Active'),
('C006', 'Vikram Singh', '9456789013', '22, Electronics City Phase 1', 'Electronic City', 'Active');

-- ==================== SEED DATA FOR SUPPLIERS ====================
INSERT INTO suppliers (Supplier_ID, Supplier_Name, Phone_Num) VALUES
('S001', 'Nandini Dairy Farm', '8012345678'),
('S002', 'Green Valley Farms', '8123456789'),
('S003', 'Karnataka Agro Co.', '8234567890');

-- ==================== SEED DATA FOR PRODUCTS ====================
INSERT INTO products (Product_ID, Product_Name, Price_per_unit, Unit) VALUES
('P001', 'Full Cream Milk', 28.00, 'Litre'),
('P002', 'Toned Milk', 22.00, 'Litre'),
('P003', 'Curd', 35.00, 'Cup (200g)'),
('P004', 'Fresh Spinach', 18.00, '250g Bundle'),
('P005', 'Tomato', 12.00, 'Kg'),
('P006', 'Carrot', 15.00, 'Kg'),
('P007', 'Green Beans', 20.00, '500g Pack'),
('P008', 'Paneer', 80.00, '200g Block');
