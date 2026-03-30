# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FreshDeliver is a frontend-only milk & vegetables delivery management system built as a DBMS project. It simulates a complete delivery platform with role-based portals for Admin, Customer, Supplier, and Delivery personnel.

**Tech Stack**: Pure HTML/CSS/JavaScript (no build tools), Chart.js for visualizations, localStorage for data persistence.

## Architecture

### Data Layer (`js/api.js`)
- Mock database using localStorage under key `freshdeliver_db`
- Pre-seeded with demo data (customers, suppliers, products, orders, deliveries, etc.)
- All CRUD operations are async with artificial 80ms delay
- Global `API` object exposes entity methods: `API.customers.getAll()`, `API.orders.create(data)`, etc.
- ID generation uses prefix pattern: `C001`, `S001`, `P001`, `O001`, etc.
- Call `resetDB()` in console to restore seed data

### Auth Layer (`js/auth.js`)
- Session management using sessionStorage under key `freshdeliver_session`
- Demo accounts with hardcoded credentials (see index.html for full list)
- `Auth.login(username, password)` returns `{success, session}` or `{success, error}`
- `Auth.requireAuth(role)` enforces role-based access on protected pages
- Global helpers: `showToast()`, `openModal()`, `closeModal()`, `formatCurrency()`, `formatDate()`, `statusBadge()`

### Role-Specific Navigation (`js/admin.js`, `js/customer.js`)
- Each role has a navigation builder function
- Call `buildAdminSidebar('admin-dashboard.html')` to render sidebar with active page highlighting
- Similar pattern for customer sidebar

### Key Entities
- **Customers**: User accounts with subscription management
- **Suppliers**: Product providers (Nandini Dairy, Green Valley Farms, etc.)
- **Products**: Milk, vegetables with price per unit
- **Inventory**: Stock levels with low-stock tracking
- **Subscriptions**: Customer-Supplier associations with product details
- **Orders**: Customer purchase records with line items
- **Deliveries**: Order fulfillment tracking with assigned delivery persons
- **Payments**: Transaction records (UPI, Cash, Card)
- **Delivery Schedules**: Time slots and delivery assignments

## Development Workflow

### Running the Application
```bash
# No build step required - just open in browser
# Option 1: Direct file open
open index.html

# Option 2: Local server (if needed for testing)
python -m http.server 8000
# Then visit http://localhost:8000
```

### Demo Credentials
- **Admin**: `admin` / `admin123`
- **Customer**: `priya` / `pass123`
- **Supplier**: `nandini` / `supp123`
- **Delivery**: `raju` / `del123`

### Testing Data Operations
Open browser console and use:
```javascript
// View current data
API.customers.getAll()
API.orders.getById('O001')

// Create new record
await API.products.create({Product_Name: 'Butter', Price_per_unit: 50, Unit: '100g'})

// Reset to seed data
resetDB()
```

## File Organization

```
project_frontend/
├── index.html                          # Landing page with login
├── index.css                           # Global styles
├── js/
│   ├── api.js                         # Mock database & CRUD operations
│   ├── auth.js                        # Authentication & UI helpers
│   ├── admin.js                       # Admin navigation builder
│   └── customer.js                    # Customer navigation builder
├── admin-*.html                       # Admin portal pages (11 pages)
├── customer-*.html                    # Customer portal pages (6 pages)
├── supplier-*.html                    # Supplier portal pages (3 pages)
└── delivery-*.html                    # Delivery portal pages (3 pages)
```

## Common Patterns

### Page Initialization
Every protected page follows this pattern:
```javascript
const session = Auth.requireAuth('admin'); // or 'customer', 'supplier', 'delivery'
if (!session) return; // Redirected if not authenticated

Auth.initSidebarUser();
Auth.initMobileSidebar();
buildAdminSidebar('admin-dashboard.html'); // Current page
initModalClosers();
```

### CRUD Operations
```javascript
// Read
const customers = await API.customers.getAll();
const customer = await API.customers.getById('C001');

// Create
const newCustomer = await API.customers.create({
  Name: 'John Doe',
  Phone_Num: '9876543210',
  Address: '123 Street',
  Area: 'Koramangala',
  Account_Status: 'Active'
});

// Update
await API.customers.update('C001', {Account_Status: 'Inactive'});

// Delete
await API.customers.delete('C001');
```

### UI Feedback
```javascript
showToast('Customer added successfully!', 'success'); // or 'error', 'warning', 'info'
```

### Modal Dialogs
```html
<div class="modal-overlay" id="add-modal">
  <div class="modal-dialog">
    <div class="modal-header">
      <h3>Add New Customer</h3>
      <button class="modal-close">&times;</button>
    </div>
    <!-- modal content -->
  </div>
</div>

<script>
openModal('add-modal');
closeModal('add-modal');
</script>
```

## Data Relationships

- **Subscriptions**: Links Customer → Supplier, with details in `subscription_details` (Product + Quantity + Frequency)
- **Orders**: Customer purchases with line items in `order_items`
- **Deliveries**: Links Order → Delivery Person with schedule in `delivery_schedules`
- **Payments**: One-to-one with Orders
- **Supplier Products**: Junction table linking Suppliers to Products they provide
- **Inventory**: One-to-one with Products for stock tracking

## Important Notes

- No backend server - all data is in browser localStorage
- Data persists across page reloads but not across browsers/devices
- Session expires when browser tab closes (sessionStorage)
- All operations are client-side only
- Chart.js loaded from CDN for dashboard visualizations
- Mobile-responsive with hamburger menu for sidebar
