# FreshDeliver - Complete Setup Guide

## 🎯 Overview

You now have a complete FreshDeliver application with:
- **Frontend**: HTML/CSS/JavaScript (Pure vanilla, no build tools)
- **Backend**: FastAPI + MySQL (Python)
- **Features**: Full CRUD operations for Customer Management

---

## 📁 Project Structure

```
project_frontend/
├── backend/                    # FastAPI Backend
│   ├── main.py                # API routes & application
│   ├── models.py              # Database models (SQLAlchemy)
│   ├── schemas.py             # Request/Response schemas (Pydantic)
│   ├── database.py            # Database connection
│   ├── customer.sql           # Database schema & seed data
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   ├── run.bat               # Windows startup script
│   └── README.md             # Backend documentation
│
├── js/
│   ├── api.js                # Original localStorage API (legacy)
│   ├── api-client.js         # New FastAPI client
│   ├── auth.js               # Authentication
│   ├── admin.js              # Admin navigation
│   └── customer.js           # Customer navigation
│
├── admin-customers.html       # Original (localStorage version)
├── admin-customers-backend.html  # New (Backend API version)
├── index.html                # Login page
└── ...                       # Other HTML pages

```

---

## 🚀 Quick Start

### Step 1: Setup MySQL Database

1. **Start MySQL Server**
   ```bash
   # Windows: Start MySQL service
   net start mysql
   ```

2. **Create Database**
   ```bash
   cd backend
   mysql -u root -p < customer.sql
   ```

   Or manually in MySQL:
   ```sql
   CREATE DATABASE freshdeliver;
   USE freshdeliver;
   SOURCE customer.sql;
   ```

### Step 2: Setup Backend

1. **Navigate to backend folder**
   ```bash
   cd backend
   ```

2. **Create `.env` file**
   ```bash
   copy .env.example .env
   ```

3. **Edit `.env` with your settings**
   ```env
   DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/freshdeliver
   SECRET_KEY=your-secret-key-change-this
   CORS_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
   ```

4. **Run the backend** (Windows)
   ```bash
   # Double-click run.bat
   # OR
   run.bat
   ```

   Or manually:
   ```bash
   # Create virtual environment
   python -m venv venv
   venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Run server
   python main.py
   ```

   ✅ Backend will start at: **http://localhost:8000**
   📚 API Docs: **http://localhost:8000/docs**

### Step 3: Start Frontend

1. **Navigate to project root**
   ```bash
   cd ..
   ```

2. **Start HTTP server**
   ```bash
   python -m http.server 8080
   ```

   ✅ Frontend will be at: **http://localhost:8080**

### Step 4: Login & Test

1. Open **http://localhost:8080/index.html**
2. Login with admin credentials:
   - Username: `admin`
   - Password: `admin123`
3. Navigate to **Customer Management (Backend)**
4. Open **admin-customers-backend.html**

---

## 🔧 Configuration

### Database Connection

Edit `backend/.env`:
```env
# For MySQL
DATABASE_URL=mysql+pymysql://username:password@host:port/database

# Examples:
# Local MySQL:
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/freshdeliver

# Remote MySQL:
DATABASE_URL=mysql+pymysql://user:pass@192.168.1.100:3306/freshdeliver
```

### CORS Settings

If your frontend runs on a different port, update `backend/.env`:
```env
CORS_ORIGINS=http://localhost:8080,http://localhost:5500,http://127.0.0.1:8080
```

---

## 📊 API Endpoints

### Customer Management

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/customers` | Get all customers | - |
| GET | `/api/customers/{id}` | Get customer by ID | - |
| POST | `/api/customers` | Create customer | `{Name, Phone_Num, Address, Area, Account_Status}` |
| PUT | `/api/customers/{id}` | Update customer | `{Name?, Phone_Num?, Address?, Area?, Account_Status?}` |
| DELETE | `/api/customers/{id}` | Delete customer | - |

### Example API Usage

**Using curl:**
```bash
# Get all customers
curl http://localhost:8000/api/customers

# Create customer
curl -X POST http://localhost:8000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"Name":"John Doe","Phone_Num":"9876543210","Address":"123 St","Area":"Koramangala","Account_Status":"Active"}'

# Update customer
curl -X PUT http://localhost:8000/api/customers/C001 \
  -H "Content-Type: application/json" \
  -d '{"Account_Status":"Inactive"}'

# Delete customer
curl -X DELETE http://localhost:8000/api/customers/C001
```

**Using JavaScript:**
```javascript
// Get all customers
const customers = await CustomerAPI.getAll();

// Create customer
await CustomerAPI.create({
  Name: "John Doe",
  Phone_Num: "9876543210",
  Address: "123 Main St",
  Area: "Koramangala",
  Account_Status: "Active"
});

// Update customer
await CustomerAPI.update('C001', { Account_Status: 'Inactive' });

// Delete customer
await CustomerAPI.delete('C001');
```

---

## 🎨 Features Implemented

### Backend (FastAPI)
- ✅ RESTful API design
- ✅ SQLAlchemy ORM models
- ✅ Pydantic validation schemas
- ✅ CORS middleware
- ✅ Auto-generated Customer IDs (C001, C002, etc.)
- ✅ Phone number validation (10 digits)
- ✅ Unique phone number constraint
- ✅ Error handling
- ✅ API documentation (Swagger/ReDoc)

### Frontend (admin-customers-backend.html)
- ✅ View all customers in table
- ✅ Search & filter functionality
- ✅ Add new customer
- ✅ Edit existing customer
- ✅ Delete customer
- ✅ Real-time stats (Total, Active, Inactive)
- ✅ Responsive design
- ✅ Toast notifications
- ✅ Form validation
- ✅ Error handling

---

## 🔍 Testing the System

### 1. Test Backend Directly

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Get Customers:**
```bash
curl http://localhost:8000/api/customers
```

**Create Test Customer:**
```bash
curl -X POST http://localhost:8000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "Test User",
    "Phone_Num": "9999999999",
    "Address": "Test Address",
    "Area": "Whitefield",
    "Account_Status": "Active"
  }'
```

### 2. Test Frontend

1. Open http://localhost:8080/admin-customers-backend.html
2. Try these actions:
   - ➕ Add new customer
   - ✏️ Edit existing customer
   - 🔍 Search customers
   - 🗑️ Delete customer
   - 🔄 Refresh list

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error: "Can't connect to MySQL server"**
```bash
# Check if MySQL is running
mysql -u root -p

# Start MySQL service (Windows)
net start mysql
```

**Error: "Access denied for user"**
- Check DATABASE_URL in `.env` file
- Verify username/password are correct

**Error: "Unknown database 'freshdeliver'"**
```bash
# Create database
mysql -u root -p
CREATE DATABASE freshdeliver;
USE freshdeliver;
SOURCE customer.sql;
```

### Frontend Issues

**Error: "Failed to load customers"**
- Check if backend is running: http://localhost:8000/health
- Check browser console for CORS errors
- Verify CORS_ORIGINS in backend/.env

**CORS Error:**
```env
# Add your frontend URL to backend/.env
CORS_ORIGINS=http://localhost:8080,http://localhost:5500
```

### Port Already in Use

**Backend (8000):**
```bash
# Change port in run command
uvicorn main:app --reload --port 8001
```

**Frontend (8080):**
```bash
# Use different port
python -m http.server 8081
```

---

## 📚 Next Steps

### Expand the System

1. **Add More Entities:**
   - Suppliers management
   - Products management
   - Orders management
   - Delivery tracking

2. **Authentication:**
   - JWT tokens
   - User roles & permissions
   - Session management

3. **Advanced Features:**
   - Pagination for large datasets
   - Export to CSV/Excel
   - Upload customer photos
   - Email notifications
   - SMS integration

4. **Deployment:**
   - Deploy backend to cloud (AWS, Azure, Heroku)
   - Deploy frontend to GitHub Pages or Netlify
   - Use production database (AWS RDS, etc.)

---

## 📞 Demo Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**Existing Customers:**
- Priya Sharma - 9876543210
- Ramesh Patel - 9812345678
- Meena Iyer - 9123456780

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [MySQL Reference](https://dev.mysql.com/doc/)
- [Pydantic Validation](https://docs.pydantic.dev/)

---

## ✅ Checklist

- [ ] MySQL server installed and running
- [ ] Database created with seed data
- [ ] Backend `.env` file configured
- [ ] Backend dependencies installed
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 8080
- [ ] Successfully logged in as admin
- [ ] Customer CRUD operations working
- [ ] API documentation accessible at /docs

---

**🎉 Congratulations! Your FreshDeliver system is ready!**

For questions or issues, check:
- Backend logs in terminal
- Browser console (F12) for frontend errors
- API docs at http://localhost:8000/docs
