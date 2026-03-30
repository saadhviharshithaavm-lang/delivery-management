# FreshDeliver Backend API

FastAPI backend for FreshDeliver milk & vegetables delivery management system.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- pip (Python package manager)

### Installation

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Create MySQL database**
```bash
mysql -u root -p < customer.sql
```

Or manually:
```sql
CREATE DATABASE freshdeliver;
USE freshdeliver;
SOURCE customer.sql;
```

6. **Configure environment variables**
```bash
# Copy example env file
copy .env.example .env

# Edit .env file with your database credentials
```

Example `.env`:
```env
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/freshdeliver
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
```

7. **Run the server**
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Customer Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers` | Get all customers |
| GET | `/api/customers/{id}` | Get customer by ID |
| POST | `/api/customers` | Create new customer |
| PUT | `/api/customers/{id}` | Update customer |
| DELETE | `/api/customers/{id}` | Delete customer |

### Example Requests

**Get all customers:**
```bash
curl http://localhost:8000/api/customers
```

**Create customer:**
```bash
curl -X POST http://localhost:8000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "John Doe",
    "Phone_Num": "9876543210",
    "Address": "123 Main St",
    "Area": "Koramangala",
    "Account_Status": "Active"
  }'
```

**Update customer:**
```bash
curl -X PUT http://localhost:8000/api/customers/C001 \
  -H "Content-Type: application/json" \
  -d '{
    "Account_Status": "Inactive"
  }'
```

**Delete customer:**
```bash
curl -X DELETE http://localhost:8000/api/customers/C001
```

## 🗂️ Project Structure

```
backend/
├── main.py              # FastAPI application & routes
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for validation
├── database.py          # Database connection & session
├── customer.sql         # Database schema & seed data
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md           # This file
```

## 🛠️ Database Schema

### customers
- `Customer_ID` (PK) - VARCHAR(10)
- `Name` - VARCHAR(100)
- `Phone_Num` - VARCHAR(15) UNIQUE
- `Address` - VARCHAR(255)
- `Area` - VARCHAR(50)
- `Account_Status` - ENUM('Active', 'Inactive')

## 🔄 Frontend Integration

Update the frontend to use the new API:

1. Include the API client:
```html
<script src="js/api-client.js"></script>
```

2. Use the new admin-customers-backend.html page or update existing pages:
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

## 🔍 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Run with auto-reload (development)
```bash
uvicorn main:app --reload
```

### Production deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🐛 Troubleshooting

### Connection Issues
- Check if MySQL is running: `mysql -u root -p`
- Verify database exists: `SHOW DATABASES;`
- Check DATABASE_URL in .env file

### CORS Errors
- Update CORS_ORIGINS in .env file
- Include your frontend URL (e.g., http://localhost:5500)

### Port Already in Use
- Change port: `uvicorn main:app --port 8001`
- Or kill existing process

## 📝 Notes

- Phone numbers must be exactly 10 digits
- Customer IDs are auto-generated (C001, C002, etc.)
- Database tables are created automatically on first run
- Seed data is included in customer.sql

## 🚀 Next Steps

To add more features:
1. Add authentication & JWT tokens
2. Implement other entities (suppliers, products, orders)
3. Add pagination for large datasets
4. Implement filtering & sorting
5. Add background tasks for notifications
6. Set up logging & monitoring

## 📄 License

DBMS Project 2026
