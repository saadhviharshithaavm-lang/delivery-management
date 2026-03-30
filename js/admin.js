/* ============================================================
   Admin JS — shared admin sidebar nav init + page-specific logic
   ============================================================ */

// ── Sidebar Navigation Items ────────────────────────────────
const ADMIN_NAV = [
  { label: 'Overview', href: 'admin-dashboard.html', icon: '📊', section: 'MAIN' },
  { label: 'Customers', href: 'admin-customers.html', icon: '👥', section: 'MANAGEMENT' },
  { label: 'Suppliers', href: 'admin-suppliers.html', icon: '🏭', section: 'MANAGEMENT' },
  { label: 'Products', href: 'admin-products.html', icon: '🛒', section: 'MANAGEMENT' },
  { label: 'Inventory', href: 'admin-inventory.html', icon: '📦', section: 'MANAGEMENT' },
  { label: 'Subscriptions', href: 'admin-subscriptions.html', icon: '🔄', section: 'OPERATIONS' },
  { label: 'Orders', href: 'admin-orders.html', icon: '📋', section: 'OPERATIONS' },
  { label: 'Deliveries', href: 'admin-deliveries.html', icon: '🚚', section: 'OPERATIONS' },
  { label: 'Payments', href: 'admin-payments.html', icon: '💳', section: 'OPERATIONS' },
  { label: 'Delivery Personnel', href: 'admin-delivery-persons.html', icon: '🧑‍💼', section: 'STAFF' },
  { label: 'Delivery Schedules', href: 'admin-delivery-schedule.html', icon: '📅', section: 'STAFF' },
];

function buildAdminSidebar(activePage) {
  const nav = document.getElementById('admin-nav');
  if (!nav) return;
  let currentSection = '';
  let html = '';
  ADMIN_NAV.forEach(item => {
    if (item.section !== currentSection) {
      currentSection = item.section;
      html += `<div class="nav-section-title">${currentSection}</div>`;
    }
    const active = activePage === item.href ? 'active' : '';
    html += `<a href="${item.href}" class="nav-item ${active}">
      <span class="nav-icon">${item.icon}</span>
      <span>${item.label}</span>
    </a>`;
  });
  nav.innerHTML = html;
}

window.buildAdminSidebar = buildAdminSidebar;
