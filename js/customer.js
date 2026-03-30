/* ============================================================
   Customer JS — shared customer sidebar nav init
   ============================================================ */

const CUSTOMER_NAV = [
  { label: 'Dashboard', href: 'customer-dashboard.html', icon: '🏠', section: 'MAIN' },
  { label: 'My Profile', href: 'customer-profile.html', icon: '👤', section: 'ACCOUNT' },
  { label: 'My Subscriptions', href: 'customer-subscriptions.html', icon: '🔄', section: 'SERVICES' },
  { label: 'My Orders', href: 'customer-orders.html', icon: '📋', section: 'SERVICES' },
  { label: 'Deliveries', href: 'customer-deliveries.html', icon: '🚚', section: 'SERVICES' },
  { label: 'Payments', href: 'customer-payments.html', icon: '💳', section: 'BILLING' },
];

function buildCustomerSidebar(activePage) {
  const nav = document.getElementById('customer-nav');
  if (!nav) return;
  let currentSection = '';
  let html = '';
  CUSTOMER_NAV.forEach(item => {
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

window.buildCustomerSidebar = buildCustomerSidebar;
