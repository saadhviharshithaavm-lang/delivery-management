/* ============================================================
   FRESH DELIVER — Mock API Layer (localStorage-backed)
   All entity CRUD with realistic demo data pre-seeded.
   ============================================================ */

const DB_KEY = 'freshdeliver_db';

// ── Seed Data ──────────────────────────────────────────────
const SEED = {
  customers: [
    { Customer_ID: 'C001', Name: 'Priya Sharma', Phone_Num: '9876543210', Address: '12, Green Park, Near Market', Area: 'Koramangala', Account_Status: 'Active' },
    { Customer_ID: 'C002', Name: 'Ramesh Patel', Phone_Num: '9812345678', Address: '45, Lakeview Apartments', Area: 'Indiranagar', Account_Status: 'Active' },
    { Customer_ID: 'C003', Name: 'Meena Iyer', Phone_Num: '9123456780', Address: '7, Sunflower Colony', Area: 'Whitefield', Account_Status: 'Active' },
    { Customer_ID: 'C004', Name: 'Anil Verma', Phone_Num: '9234567891', Address: '3, MG Road, Block B', Area: 'Koramangala', Account_Status: 'Inactive' },
    { Customer_ID: 'C005', Name: 'Sunita Reddy', Phone_Num: '9345678902', Address: '88, HSR Layout, 4th Sector', Area: 'HSR Layout', Account_Status: 'Active' },
    { Customer_ID: 'C006', Name: 'Vikram Singh', Phone_Num: '9456789013', Address: '22, Electronics City Phase 1', Area: 'Electronic City', Account_Status: 'Active' },
  ],
  suppliers: [
    { Supplier_ID: 'S001', Supplier_Name: 'Nandini Dairy Farm', Phone_Num: '8012345678' },
    { Supplier_ID: 'S002', Supplier_Name: 'Green Valley Farms', Phone_Num: '8123456789' },
    { Supplier_ID: 'S003', Supplier_Name: 'Karnataka Agro Co.', Phone_Num: '8234567890' },
  ],
  products: [
    { Product_ID: 'P001', Product_Name: 'Full Cream Milk', Price_per_unit: 28, Unit: 'Litre' },
    { Product_ID: 'P002', Product_Name: 'Toned Milk', Price_per_unit: 22, Unit: 'Litre' },
    { Product_ID: 'P003', Product_Name: 'Curd', Price_per_unit: 35, Unit: 'Cup (200g)' },
    { Product_ID: 'P004', Product_Name: 'Fresh Spinach', Price_per_unit: 18, Unit: '250g Bundle' },
    { Product_ID: 'P005', Product_Name: 'Tomato', Price_per_unit: 12, Unit: 'Kg' },
    { Product_ID: 'P006', Product_Name: 'Carrot', Price_per_unit: 15, Unit: 'Kg' },
    { Product_ID: 'P007', Product_Name: 'Green Beans', Price_per_unit: 20, Unit: '500g Pack' },
    { Product_ID: 'P008', Product_Name: 'Paneer', Price_per_unit: 80, Unit: '200g Block' },
  ],
  inventory: [
    { Inventory_ID: 'I001', Product_ID: 'P001', Available_quantity: 340, LastUpdated: '2026-03-23' },
    { Inventory_ID: 'I002', Product_ID: 'P002', Available_quantity: 210, LastUpdated: '2026-03-23' },
    { Inventory_ID: 'I003', Product_ID: 'P003', Available_quantity: 125, LastUpdated: '2026-03-22' },
    { Inventory_ID: 'I004', Product_ID: 'P004', Available_quantity: 40, LastUpdated: '2026-03-23' },
    { Inventory_ID: 'I005', Product_ID: 'P005', Available_quantity: 180, LastUpdated: '2026-03-22' },
    { Inventory_ID: 'I006', Product_ID: 'P006', Available_quantity: 95, LastUpdated: '2026-03-23' },
    { Inventory_ID: 'I007', Product_ID: 'P007', Available_quantity: 60, LastUpdated: '2026-03-21' },
    { Inventory_ID: 'I008', Product_ID: 'P008', Available_quantity: 18, LastUpdated: '2026-03-23' },
  ],
  subscriptions: [
    { Subscription_ID: 'SUB001', Customer_ID: 'C001', Supplier_ID: 'S001', Start_date: '2026-01-01', End_date: '2026-06-30', Status: 'Active' },
    { Subscription_ID: 'SUB002', Customer_ID: 'C002', Supplier_ID: 'S002', Start_date: '2026-02-01', End_date: '2026-07-31', Status: 'Active' },
    { Subscription_ID: 'SUB003', Customer_ID: 'C003', Supplier_ID: 'S001', Start_date: '2026-01-15', End_date: '2026-04-15', Status: 'Paused' },
    { Subscription_ID: 'SUB004', Customer_ID: 'C005', Supplier_ID: 'S003', Start_date: '2026-03-01', End_date: '2026-08-31', Status: 'Active' },
    { Subscription_ID: 'SUB005', Customer_ID: 'C006', Supplier_ID: 'S002', Start_date: '2026-01-10', End_date: '2026-03-10', Status: 'Cancelled' },
  ],
  subscription_details: [
    { Subscription_ID: 'SUB001', Product_ID: 'P001', Quantity_Per_Day: 2, Delivery_Frequency: 'Daily' },
    { Subscription_ID: 'SUB001', Product_ID: 'P003', Quantity_Per_Day: 1, Delivery_Frequency: 'Daily' },
    { Subscription_ID: 'SUB002', Product_ID: 'P004', Quantity_Per_Day: 2, Delivery_Frequency: 'Daily' },
    { Subscription_ID: 'SUB002', Product_ID: 'P005', Quantity_Per_Day: 1, Delivery_Frequency: 'Alternate' },
    { Subscription_ID: 'SUB003', Product_ID: 'P002', Quantity_Per_Day: 1, Delivery_Frequency: 'Daily' },
    { Subscription_ID: 'SUB004', Product_ID: 'P006', Quantity_Per_Day: 1, Delivery_Frequency: 'Weekly' },
    { Subscription_ID: 'SUB004', Product_ID: 'P007', Quantity_Per_Day: 2, Delivery_Frequency: 'Daily' },
    { Subscription_ID: 'SUB005', Product_ID: 'P008', Quantity_Per_Day: 1, Delivery_Frequency: 'Alternate' },
  ],
  delivery_persons: [
    { DeliveryPerson_ID: 'DP001', Name: 'Raju Kumar', Phone_Num: '7890123456', VehicleType: 'Bicycle', Area_assigned: 'Koramangala' },
    { DeliveryPerson_ID: 'DP002', Name: 'Suresh Babu', Phone_Num: '7801234567', VehicleType: 'Motorbike', Area_assigned: 'Indiranagar' },
    { DeliveryPerson_ID: 'DP003', Name: 'Manoj Yadav', Phone_Num: '7712345678', VehicleType: 'Bicycle', Area_assigned: 'Whitefield' },
    { DeliveryPerson_ID: 'DP004', Name: 'Deepak Reddy', Phone_Num: '7623456789', VehicleType: 'Motorbike', Area_assigned: 'HSR Layout' },
    { DeliveryPerson_ID: 'DP005', Name: 'Arjun Nair', Phone_Num: '7534567890', VehicleType: 'E-Bike', Area_assigned: 'Electronic City' },
  ],
  orders: [
    { Order_ID: 'O001', Customer_ID: 'C001', Order_date: '2026-03-20', Order_status: 'Delivered', Total_amount: 168 },
    { Order_ID: 'O002', Customer_ID: 'C002', Order_date: '2026-03-21', Order_status: 'Processing', Total_amount: 66 },
    { Order_ID: 'O003', Customer_ID: 'C003', Order_date: '2026-03-21', Order_status: 'Pending', Total_amount: 44 },
    { Order_ID: 'O004', Customer_ID: 'C005', Order_date: '2026-03-22', Order_status: 'Delivered', Total_amount: 80 },
    { Order_ID: 'O005', Customer_ID: 'C001', Order_date: '2026-03-22', Order_status: 'Processing', Total_amount: 91 },
    { Order_ID: 'O006', Customer_ID: 'C006', Order_date: '2026-03-23', Order_status: 'Pending', Total_amount: 160 },
  ],
  order_items: [
    { Order_ID: 'O001', Product_ID: 'P001', Quantity: 4, Price: 28 },
    { Order_ID: 'O001', Product_ID: 'P003', Quantity: 2, Price: 35 },
    { Order_ID: 'O002', Product_ID: 'P004', Quantity: 2, Price: 18 },
    { Order_ID: 'O002', Product_ID: 'P005', Quantity: 2, Price: 12 },
    { Order_ID: 'O003', Product_ID: 'P002', Quantity: 2, Price: 22 },
    { Order_ID: 'O004', Product_ID: 'P006', Quantity: 2, Price: 15 },
    { Order_ID: 'O004', Product_ID: 'P007', Quantity: 1, Price: 20 },
    { Order_ID: 'O005', Product_ID: 'P001', Quantity: 2, Price: 28 },
    { Order_ID: 'O005', Product_ID: 'P003', Quantity: 1, Price: 35 },
    { Order_ID: 'O006', Product_ID: 'P008', Quantity: 2, Price: 80 },
  ],
  payments: [
    { Payment_ID: 'PAY001', Order_ID: 'O001', Amount: 168, Payment_method: 'UPI', Payment_status: 'Paid', Payment_Date: '2026-03-20' },
    { Payment_ID: 'PAY002', Order_ID: 'O002', Amount: 66,  Payment_method: 'Cash', Payment_status: 'Pending', Payment_Date: '' },
    { Payment_ID: 'PAY003', Order_ID: 'O003', Amount: 44,  Payment_method: 'Card', Payment_status: 'Pending', Payment_Date: '' },
    { Payment_ID: 'PAY004', Order_ID: 'O004', Amount: 80,  Payment_method: 'UPI', Payment_status: 'Paid', Payment_Date: '2026-03-22' },
    { Payment_ID: 'PAY005', Order_ID: 'O005', Amount: 91,  Payment_method: 'UPI', Payment_status: 'Pending', Payment_Date: '' },
    { Payment_ID: 'PAY006', Order_ID: 'O006', Amount: 160, Payment_method: 'Card', Payment_status: 'Pending', Payment_Date: '' },
  ],
  deliveries: [
    { Delivery_ID: 'D001', Order_ID: 'O001', DeliveryPerson_ID: 'DP001', Delivery_date: '2026-03-20', Delivery_Status: 'Delivered' },
    { Delivery_ID: 'D002', Order_ID: 'O002', DeliveryPerson_ID: 'DP002', Delivery_date: '2026-03-21', Delivery_Status: 'Pending' },
    { Delivery_ID: 'D003', Order_ID: 'O003', DeliveryPerson_ID: 'DP003', Delivery_date: '2026-03-21', Delivery_Status: 'Failed' },
    { Delivery_ID: 'D004', Order_ID: 'O004', DeliveryPerson_ID: 'DP004', Delivery_date: '2026-03-22', Delivery_Status: 'Delivered' },
    { Delivery_ID: 'D005', Order_ID: 'O005', DeliveryPerson_ID: 'DP001', Delivery_date: '2026-03-22', Delivery_Status: 'Pending' },
    { Delivery_ID: 'D006', Order_ID: 'O006', DeliveryPerson_ID: 'DP005', Delivery_date: '2026-03-23', Delivery_Status: 'Pending' },
  ],
  delivery_schedules: [
    { Schedule_ID: 'SCH001', Delivery_ID: 'D001', Scheduled_date: '2026-03-20', Time_slot: '06:00 - 08:00', Schedule_status: 'Completed' },
    { Schedule_ID: 'SCH002', Delivery_ID: 'D002', Scheduled_date: '2026-03-21', Time_slot: '07:00 - 09:00', Schedule_status: 'Pending' },
    { Schedule_ID: 'SCH003', Delivery_ID: 'D003', Scheduled_date: '2026-03-21', Time_slot: '06:30 - 08:30', Schedule_status: 'Failed' },
    { Schedule_ID: 'SCH004', Delivery_ID: 'D004', Scheduled_date: '2026-03-22', Time_slot: '06:00 - 08:00', Schedule_status: 'Completed' },
    { Schedule_ID: 'SCH005', Delivery_ID: 'D005', Scheduled_date: '2026-03-22', Time_slot: '08:00 - 10:00', Schedule_status: 'Pending' },
    { Schedule_ID: 'SCH006', Delivery_ID: 'D006', Scheduled_date: '2026-03-23', Time_slot: '07:00 - 09:00', Schedule_status: 'Pending' },
  ],
  supplier_products: [
    { Supplier_ID: 'S001', Product_ID: 'P001' },
    { Supplier_ID: 'S001', Product_ID: 'P002' },
    { Supplier_ID: 'S001', Product_ID: 'P003' },
    { Supplier_ID: 'S001', Product_ID: 'P008' },
    { Supplier_ID: 'S002', Product_ID: 'P004' },
    { Supplier_ID: 'S002', Product_ID: 'P005' },
    { Supplier_ID: 'S002', Product_ID: 'P007' },
    { Supplier_ID: 'S003', Product_ID: 'P006' },
    { Supplier_ID: 'S003', Product_ID: 'P007' },
  ]
};

// ── DB Init ────────────────────────────────────────────────
function initDB() {
  if (!localStorage.getItem(DB_KEY)) {
    localStorage.setItem(DB_KEY, JSON.stringify(SEED));
  }
}
function getDB() { return JSON.parse(localStorage.getItem(DB_KEY)); }
function saveDB(db) { localStorage.setItem(DB_KEY, JSON.stringify(db)); }
function resetDB() { localStorage.setItem(DB_KEY, JSON.stringify(SEED)); }

// ── ID Generator ───────────────────────────────────────────
function genId(prefix, existing, field) {
  const nums = existing.map(e => parseInt(e[field].replace(prefix,'')) || 0);
  const next = (nums.length ? Math.max(...nums) : 0) + 1;
  return `${prefix}${String(next).padStart(3,'0')}`;
}

// ── Generic CRUD ───────────────────────────────────────────
function delay(ms=80) { return new Promise(r => setTimeout(r, ms)); }

async function getAll(table) {
  await delay();
  return [...(getDB()[table] || [])];
}
async function getById(table, field, id) {
  await delay();
  return (getDB()[table] || []).find(r => r[field] === id) || null;
}
async function create(table, record) {
  await delay();
  const db = getDB();
  db[table] = [...(db[table] || []), record];
  saveDB(db);
  return record;
}
async function update(table, field, id, changes) {
  await delay();
  const db = getDB();
  db[table] = (db[table] || []).map(r => r[field] === id ? { ...r, ...changes } : r);
  saveDB(db);
  return db[table].find(r => r[field] === id);
}
async function remove(table, field, id) {
  await delay();
  const db = getDB();
  db[table] = (db[table] || []).filter(r => r[field] !== id);
  saveDB(db);
  return true;
}

// ── Entity APIs ────────────────────────────────────────────

// Customers
const API = {
  // Customers
  customers: {
    getAll: () => getAll('customers'),
    getById: id => getById('customers', 'Customer_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('C', db.customers, 'Customer_ID');
      return create('customers', { Customer_ID: id, ...data });
    },
    update: (id, data) => update('customers', 'Customer_ID', id, data),
    delete: id => remove('customers', 'Customer_ID', id),
  },

  // Suppliers
  suppliers: {
    getAll: () => getAll('suppliers'),
    getById: id => getById('suppliers', 'Supplier_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('S', db.suppliers, 'Supplier_ID');
      return create('suppliers', { Supplier_ID: id, ...data });
    },
    update: (id, data) => update('suppliers', 'Supplier_ID', id, data),
    delete: id => remove('suppliers', 'Supplier_ID', id),
  },

  // Products
  products: {
    getAll: () => getAll('products'),
    getById: id => getById('products', 'Product_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('P', db.products, 'Product_ID');
      return create('products', { Product_ID: id, ...data });
    },
    update: (id, data) => update('products', 'Product_ID', id, data),
    delete: id => remove('products', 'Product_ID', id),
  },

  // Inventory
  inventory: {
    getAll: () => getAll('inventory'),
    getById: id => getById('inventory', 'Inventory_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('I', db.inventory, 'Inventory_ID');
      return create('inventory', { Inventory_ID: id, LastUpdated: new Date().toISOString().slice(0,10), ...data });
    },
    update: (id, data) => update('inventory', 'Inventory_ID', id, { ...data, LastUpdated: new Date().toISOString().slice(0,10) }),
    delete: id => remove('inventory', 'Inventory_ID', id),
    getByProduct: async pid => {
      const all = await getAll('inventory');
      return all.find(i => i.Product_ID === pid) || null;
    }
  },

  // Subscriptions
  subscriptions: {
    getAll: () => getAll('subscriptions'),
    getById: id => getById('subscriptions', 'Subscription_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('SUB', db.subscriptions, 'Subscription_ID');
      return create('subscriptions', { Subscription_ID: id, ...data });
    },
    update: (id, data) => update('subscriptions', 'Subscription_ID', id, data),
    delete: id => remove('subscriptions', 'Subscription_ID', id),
    getByCustomer: async cid => { const all = await getAll('subscriptions'); return all.filter(s => s.Customer_ID === cid); },
  },

  // Subscription Details
  subscriptionDetails: {
    getAll: () => getAll('subscription_details'),
    getBySub: async sid => { const all = await getAll('subscription_details'); return all.filter(d => d.Subscription_ID === sid); },
    create: data => create('subscription_details', data),
    update: async (sid, pid, data) => {
      await delay();
      const db = getDB();
      db.subscription_details = db.subscription_details.map(d =>
        d.Subscription_ID === sid && d.Product_ID === pid ? { ...d, ...data } : d
      );
      saveDB(db);
    },
    delete: async (sid, pid) => {
      await delay();
      const db = getDB();
      db.subscription_details = db.subscription_details.filter(d => !(d.Subscription_ID === sid && d.Product_ID === pid));
      saveDB(db);
    },
  },

  // Orders
  orders: {
    getAll: () => getAll('orders'),
    getById: id => getById('orders', 'Order_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('O', db.orders, 'Order_ID');
      return create('orders', { Order_ID: id, Order_date: new Date().toISOString().slice(0,10), ...data });
    },
    update: (id, data) => update('orders', 'Order_ID', id, data),
    delete: id => remove('orders', 'Order_ID', id),
    getByCustomer: async cid => { const all = await getAll('orders'); return all.filter(o => o.Customer_ID === cid); },
  },

  // Order Items
  orderItems: {
    getAll: () => getAll('order_items'),
    getByOrder: async oid => { const all = await getAll('order_items'); return all.filter(i => i.Order_ID === oid); },
    create: data => create('order_items', data),
    delete: async oid => {
      await delay();
      const db = getDB();
      db.order_items = db.order_items.filter(i => i.Order_ID !== oid);
      saveDB(db);
    },
  },

  // Payments
  payments: {
    getAll: () => getAll('payments'),
    getById: id => getById('payments', 'Payment_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('PAY', db.payments, 'Payment_ID');
      return create('payments', { Payment_ID: id, ...data });
    },
    update: (id, data) => update('payments', 'Payment_ID', id, data),
    delete: id => remove('payments', 'Payment_ID', id),
    getByOrder: async oid => { const all = await getAll('payments'); return all.filter(p => p.Order_ID === oid); },
    getByCustomer: async cid => {
      const orders = await getAll('orders');
      const cOrders = new Set(orders.filter(o => o.Customer_ID === cid).map(o => o.Order_ID));
      const all = await getAll('payments');
      return all.filter(p => cOrders.has(p.Order_ID));
    },
    markPaid: (id, method) => update('payments', 'Payment_ID', id, {
      Payment_status: 'Paid',
      Payment_method: method,
      Payment_Date: new Date().toISOString().slice(0, 10)
    }),
  },

  // Deliveries
  deliveries: {
    getAll: () => getAll('deliveries'),
    getById: id => getById('deliveries', 'Delivery_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('D', db.deliveries, 'Delivery_ID');
      return create('deliveries', { Delivery_ID: id, ...data });
    },
    update: (id, data) => update('deliveries', 'Delivery_ID', id, data),
    delete: id => remove('deliveries', 'Delivery_ID', id),
    getByCustomer: async cid => {
      const orders = await getAll('orders');
      const cOrders = new Set(orders.filter(o => o.Customer_ID === cid).map(o => o.Order_ID));
      const all = await getAll('deliveries');
      return all.filter(d => cOrders.has(d.Order_ID));
    },
  },

  // Delivery Persons
  deliveryPersons: {
    getAll: () => getAll('delivery_persons'),
    getById: id => getById('delivery_persons', 'DeliveryPerson_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('DP', db.delivery_persons, 'DeliveryPerson_ID');
      return create('delivery_persons', { DeliveryPerson_ID: id, ...data });
    },
    update: (id, data) => update('delivery_persons', 'DeliveryPerson_ID', id, data),
    delete: id => remove('delivery_persons', 'DeliveryPerson_ID', id),
  },

  // Delivery Schedules
  deliverySchedules: {
    getAll: () => getAll('delivery_schedules'),
    getById: id => getById('delivery_schedules', 'Schedule_ID', id),
    create: data => {
      const db = getDB();
      const id = genId('SCH', db.delivery_schedules, 'Schedule_ID');
      return create('delivery_schedules', { Schedule_ID: id, ...data });
    },
    update: (id, data) => update('delivery_schedules', 'Schedule_ID', id, data),
    delete: id => remove('delivery_schedules', 'Schedule_ID', id),
  },

  // Supplier Products
  supplierProducts: {
    getAll: () => getAll('supplier_products'),
    getBySupplier: async sid => { const all = await getAll('supplier_products'); return all.filter(sp => sp.Supplier_ID === sid); },
    getByProduct: async pid => { const all = await getAll('supplier_products'); return all.filter(sp => sp.Product_ID === pid); },
    create: data => create('supplier_products', data),
    delete: async (sid, pid) => {
      await delay();
      const db = getDB();
      db.supplier_products = db.supplier_products.filter(sp => !(sp.Supplier_ID === sid && sp.Product_ID === pid));
      saveDB(db);
    },
  },

  // Dashboard Stats
  stats: {
    getAdminStats: async () => {
      const [customers, subscriptions, orders, deliveries, payments] = await Promise.all([
        getAll('customers'), getAll('subscriptions'), getAll('orders'),
        getAll('deliveries'), getAll('payments')
      ]);
      const today = new Date().toISOString().slice(0,10);
      return {
        totalCustomers: customers.length,
        activeCustomers: customers.filter(c => c.Account_Status === 'Active').length,
        activeSubscriptions: subscriptions.filter(s => s.Status === 'Active').length,
        todayDeliveries: deliveries.filter(d => d.Delivery_date === today).length,
        pendingDeliveries: deliveries.filter(d => d.Delivery_Status === 'Pending').length,
        totalOrders: orders.length,
        totalRevenue: payments.filter(p => p.Payment_status === 'Paid').reduce((s,p) => s + p.Amount, 0),
        pendingPayments: payments.filter(p => p.Payment_status === 'Pending').reduce((s,p) => s + p.Amount, 0),
        weeklyDeliveries: [4,6,5,8,3,7,6],
        weeklyRevenue: [1200,1800,1500,2200,900,2100,1960],
      };
    },
    getCustomerStats: async cid => {
      const [subs, orders, payments, deliveries] = await Promise.all([
        API.subscriptions.getByCustomer(cid), API.orders.getByCustomer(cid),
        API.payments.getByCustomer(cid), API.deliveries.getByCustomer(cid),
      ]);
      return {
        activeSubscriptions: subs.filter(s => s.Status === 'Active').length,
        totalOrders: orders.length,
        totalPaid: payments.filter(p => p.Payment_status === 'Paid').reduce((s,p) => s + p.Amount, 0),
        pendingAmount: payments.filter(p => p.Payment_status === 'Pending').reduce((s,p) => s + p.Amount, 0),
        deliveredCount: deliveries.filter(d => d.Delivery_Status === 'Delivered').length,
        upcomingDeliveries: deliveries.filter(d => d.Delivery_Status === 'Pending').length,
      };
    }
  }
};

initDB();
window.API = API;
window.resetDB = resetDB;
