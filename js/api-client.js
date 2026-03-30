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

// Customer API
const CustomerAPI = {
  async getAll() {
    return await apiRequest('/customers');
  },

  async getById(id) {
    return await apiRequest(`/customers/${id}`);
  },

  async create(data) {
    return await apiRequest('/customers', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  async update(id, data) {
    return await apiRequest(`/customers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  async delete(id) {
    return await apiRequest(`/customers/${id}`, {
      method: 'DELETE',
    });
  },
};

// Export for use in HTML pages
window.CustomerAPI = CustomerAPI;
