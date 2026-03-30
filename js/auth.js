/* ============================================================
   FRESH DELIVER — Auth Layer
   ============================================================ */

const SESSION_KEY = 'freshdeliver_session';

const DEMO_ACCOUNTS = {
  admin: {
    username: 'admin',
    password: 'admin123',
    role: 'admin',
    name: 'System Admin',
    id: 'ADMIN001'
  },
  customers: [
    { username: 'priya',  password: 'pass123', role: 'customer', id: 'C001', name: 'Priya Sharma' },
    { username: 'ramesh', password: 'pass123', role: 'customer', id: 'C002', name: 'Ramesh Patel' },
    { username: 'meena',  password: 'pass123', role: 'customer', id: 'C003', name: 'Meena Iyer' },
    { username: 'sunita', password: 'pass123', role: 'customer', id: 'C005', name: 'Sunita Reddy' },
    { username: 'vikram', password: 'pass123', role: 'customer', id: 'C006', name: 'Vikram Singh' },
  ],
  suppliers: [
    { username: 'nandini', password: 'supp123', role: 'supplier', id: 'S001', name: 'Nandini Dairy Farm' },
    { username: 'greenvalley', password: 'supp123', role: 'supplier', id: 'S002', name: 'Green Valley Farms' },
    { username: 'karnataka', password: 'supp123', role: 'supplier', id: 'S003', name: 'Karnataka Agro Co.' },
  ],
  deliveryPersons: [
    { username: 'raju',   password: 'del123', role: 'delivery', id: 'DP001', name: 'Raju Kumar' },
    { username: 'suresh', password: 'del123', role: 'delivery', id: 'DP002', name: 'Suresh Babu' },
    { username: 'manoj',  password: 'del123', role: 'delivery', id: 'DP003', name: 'Manoj Yadav' },
    { username: 'deepak', password: 'del123', role: 'delivery', id: 'DP004', name: 'Deepak Reddy' },
    { username: 'arjun',  password: 'del123', role: 'delivery', id: 'DP005', name: 'Arjun Nair' },
  ],
};

function login(usernameOrRole, password) {
  // Quick demo login by role
  if (usernameOrRole === 'admin_demo') {
    const session = { ...DEMO_ACCOUNTS.admin, loginTime: Date.now() };
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
    return { success: true, session };
  }
  if (usernameOrRole === 'customer_demo') {
    const acc = DEMO_ACCOUNTS.customers[0];
    const session = { ...acc, loginTime: Date.now() };
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
    return { success: true, session };
  }
  if (usernameOrRole === 'supplier_demo') {
    const acc = DEMO_ACCOUNTS.suppliers[0];
    const session = { ...acc, loginTime: Date.now() };
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
    return { success: true, session };
  }
  if (usernameOrRole === 'delivery_demo') {
    const acc = DEMO_ACCOUNTS.deliveryPersons[0];
    const session = { ...acc, loginTime: Date.now() };
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
    return { success: true, session };
  }

  // Admin check
  if (usernameOrRole === DEMO_ACCOUNTS.admin.username && password === DEMO_ACCOUNTS.admin.password) {
    const session = { ...DEMO_ACCOUNTS.admin, loginTime: Date.now() };
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
    return { success: true, session };
  }

  // Customer, Supplier, Delivery search
  const allAccounts = [
    ...DEMO_ACCOUNTS.customers,
    ...DEMO_ACCOUNTS.suppliers,
    ...DEMO_ACCOUNTS.deliveryPersons,
  ];
  const acc = allAccounts.find(a => a.username === usernameOrRole && a.password === password);
  if (acc) {
    const session = { ...acc, loginTime: Date.now() };
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
    return { success: true, session };
  }

  return { success: false, error: 'Invalid credentials' };
}

function logout() {
  sessionStorage.removeItem(SESSION_KEY);
  window.location.href = 'index.html';
}

function getSession() {
  const raw = sessionStorage.getItem(SESSION_KEY);
  if (!raw) return null;
  return JSON.parse(raw);
}
/*
const ROLE_HOME = {
  admin:    'admin-dashboard.html',
  customer: 'customer-dashboard.html',
  supplier: 'supplier-dashboard.html',
  delivery: 'delivery-dashboard.html',
};
*/

function requireAuth(requiredRole) {
  const session = getSession();
  if (!session) { window.location.href = 'index.html'; return null; }
  if (requiredRole && session.role !== requiredRole) {
    window.location.href = ROLE_HOME[session.role] || 'index.html';
    return null;
  }
  return session;
}

function initSidebarUser() {
  const session = getSession();
  if (!session) return;
  const nameEl  = document.getElementById('sidebar-user-name');
  const roleEl  = document.getElementById('sidebar-user-role');
  const initEl  = document.getElementById('sidebar-user-init');
  const roleLabels = { admin:'Administrator', customer:'Customer', supplier:'Supplier', delivery:'Delivery Agent' };
  if (nameEl) nameEl.textContent = session.name;
  if (roleEl) roleEl.textContent = roleLabels[session.role] || session.role;
  if (initEl) initEl.textContent = session.name.charAt(0).toUpperCase();
}

// Mobile sidebar toggle
function initMobileSidebar() {
  const toggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (!toggle || !sidebar) return;
  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay && overlay.classList.toggle('open');
  });
  overlay && overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
  });
}

// Toast notifications
function showToast(msg, type = 'success') {
  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span class="toast-icon">${icons[type]||'ℹ️'}</span><span class="toast-msg">${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

function createToastContainer() {
  const el = document.createElement('div');
  el.id = 'toast-container';
  el.className = 'toast-container';
  document.body.appendChild(el);
  return el;
}

// Modal helpers
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('open');
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('open');
}
function initModalClosers() {
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', e => {
      if (e.target === overlay) overlay.classList.remove('open');
    });
  });
  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.modal-overlay').classList.remove('open');
    });
  });
}

// Confirm dialog helper
function confirmAction(msg) { return window.confirm(msg); }

// Format currency
function formatCurrency(n) { return '₹' + Number(n).toFixed(2); }

// Format date
function formatDate(d) {
  if (!d) return '-';
  return new Date(d).toLocaleDateString('en-IN', { day:'2-digit', month:'short', year:'numeric' });
}

// Badge HTML
function statusBadge(status) {
  const map = {
    'Active':      'badge-success',
    'Inactive':    'badge-muted',
    'Paused':      'badge-warning',
    'Cancelled':   'badge-danger',
    'Delivered':   'badge-success',
    'Pending':     'badge-warning',
    'Failed':      'badge-danger',
    'Processing':  'badge-info',
    'Paid':        'badge-success',
    'Completed':   'badge-success',
    'Unpaid':      'badge-danger',
  };
  return `<span class="badge ${map[status]||'badge-muted'}">${status}</span>`;
}

window.Auth = { login, logout, getSession, requireAuth, initSidebarUser, initMobileSidebar };
window.showToast = showToast;
window.openModal = openModal;
window.closeModal = closeModal;
window.initModalClosers = initModalClosers;
window.confirmAction = confirmAction;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.statusBadge = statusBadge;
