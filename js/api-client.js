/* ============================================================
   FRESH DELIVER — API Client for FastAPI Backend
   ============================================================ */

const API_BASE_URL = 'http://localhost:8000/api';

// Helper function for API requests
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Request failed:', error);
    throw error;
  }
}

// ==================== CUSTOMER API ====================
const CustomerAPI = {
  async getAll() {
    return await apiRequest('/customers');
  },
  async getById(id) {
    return await apiRequest(`/customers/${id}`);
  },
  async create(data) {
    return await apiRequest('/customers', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/customers/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/customers/${id}`, { method: 'DELETE' });
  },
};

// ==================== SUPPLIER API ====================
const SupplierAPI = {
  async getAll() {
    return await apiRequest('/suppliers');
  },
  async getById(id) {
    return await apiRequest(`/suppliers/${id}`);
  },
  async create(data) {
    return await apiRequest('/suppliers', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/suppliers/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/suppliers/${id}`, { method: 'DELETE' });
  },
};

// ==================== PRODUCT API ====================
const ProductAPI = {
  async getAll() {
    return await apiRequest('/products');
  },
  async getById(id) {
    return await apiRequest(`/products/${id}`);
  },
  async create(data) {
    return await apiRequest('/products', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/products/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/products/${id}`, { method: 'DELETE' });
  },
};

// ==================== INVENTORY API ====================
const InventoryAPI = {
  async getAll() {
    return await apiRequest('/inventory');
  },
  async getById(id) {
    return await apiRequest(`/inventory/${id}`);
  },
  async create(data) {
    return await apiRequest('/inventory', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/inventory/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/inventory/${id}`, { method: 'DELETE' });
  },
};

// ==================== SUBSCRIPTION API ====================
const SubscriptionAPI = {
  async getAll() {
    return await apiRequest('/subscriptions');
  },
  async getById(id) {
    return await apiRequest(`/subscriptions/${id}`);
  },
  async create(data) {
    return await apiRequest('/subscriptions', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/subscriptions/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/subscriptions/${id}`, { method: 'DELETE' });
  },
};

// ==================== SUBSCRIPTION DETAIL API ====================
const SubscriptionDetailAPI = {
  async getAll() {
    return await apiRequest('/subscription-details');
  },
  async getById(subscriptionId, productId) {
    return await apiRequest(`/subscription-details/${subscriptionId}/${productId}`);
  },
  async create(data) {
    return await apiRequest('/subscription-details', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(subscriptionId, productId, data) {
    return await apiRequest(`/subscription-details/${subscriptionId}/${productId}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(subscriptionId, productId) {
    return await apiRequest(`/subscription-details/${subscriptionId}/${productId}`, { method: 'DELETE' });
  },
};

// ==================== DELIVERY PERSON API ====================
const DeliveryPersonAPI = {
  async getAll() {
    return await apiRequest('/delivery-persons');
  },
  async getById(id) {
    return await apiRequest(`/delivery-persons/${id}`);
  },
  async create(data) {
    return await apiRequest('/delivery-persons', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/delivery-persons/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/delivery-persons/${id}`, { method: 'DELETE' });
  },
};

// ==================== ORDER API ====================
const OrderAPI = {
  async getAll() {
    return await apiRequest('/orders');
  },
  async getById(id) {
    return await apiRequest(`/orders/${id}`);
  },
  async create(data) {
    return await apiRequest('/orders', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/orders/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/orders/${id}`, { method: 'DELETE' });
  },
};

// ==================== ORDER ITEM API ====================
const OrderItemAPI = {
  async getAll() {
    return await apiRequest('/order-items');
  },
  async getById(orderId, productId) {
    return await apiRequest(`/order-items/${orderId}/${productId}`);
  },
  async create(data) {
    return await apiRequest('/order-items', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(orderId, productId, data) {
    return await apiRequest(`/order-items/${orderId}/${productId}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(orderId, productId) {
    return await apiRequest(`/order-items/${orderId}/${productId}`, { method: 'DELETE' });
  },
};

// ==================== PAYMENT API ====================
const PaymentAPI = {
  async getAll() {
    return await apiRequest('/payments');
  },
  async getById(id) {
    return await apiRequest(`/payments/${id}`);
  },
  async create(data) {
    return await apiRequest('/payments', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/payments/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/payments/${id}`, { method: 'DELETE' });
  },
};

// ==================== DELIVERY API ====================
const DeliveryAPI = {
  async getAll() {
    return await apiRequest('/deliveries');
  },
  async getById(id) {
    return await apiRequest(`/deliveries/${id}`);
  },
  async create(data) {
    return await apiRequest('/deliveries', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/deliveries/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/deliveries/${id}`, { method: 'DELETE' });
  },
};

// ==================== DELIVERY SCHEDULE API ====================
const DeliveryScheduleAPI = {
  async getAll() {
    return await apiRequest('/delivery-schedules');
  },
  async getById(id) {
    return await apiRequest(`/delivery-schedules/${id}`);
  },
  async create(data) {
    return await apiRequest('/delivery-schedules', { method: 'POST', body: JSON.stringify(data) });
  },
  async update(id, data) {
    return await apiRequest(`/delivery-schedules/${id}`, { method: 'PUT', body: JSON.stringify(data) });
  },
  async delete(id) {
    return await apiRequest(`/delivery-schedules/${id}`, { method: 'DELETE' });
  },
};

// Export all for use in HTML pages
window.CustomerAPI = CustomerAPI;
window.SupplierAPI = SupplierAPI;
window.ProductAPI = ProductAPI;
window.InventoryAPI = InventoryAPI;
window.SubscriptionAPI = SubscriptionAPI;
window.SubscriptionDetailAPI = SubscriptionDetailAPI;
window.DeliveryPersonAPI = DeliveryPersonAPI;
window.OrderAPI = OrderAPI;
window.OrderItemAPI = OrderItemAPI;
window.PaymentAPI = PaymentAPI;
window.DeliveryAPI = DeliveryAPI;
window.DeliveryScheduleAPI = DeliveryScheduleAPI;
