import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Home, ShoppingCart, Users, Package, FileText, BarChart3, UserCircle, DollarSign, LogOut } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import POS from './pages/POS';
import Customers from './pages/Customers';
import Inventory from './pages/Inventory';
import Invoices from './pages/Invoices';
import Staff from './pages/Staff';
import Expenses from './pages/Expenses';
import Reports from './pages/Reports';
import Login from './pages/Login';

const navItems = [
  { path: '/', label: 'Dashboard', icon: Home },
  { path: '/pos', label: 'New Invoice', icon: ShoppingCart, highlight: true },
  { path: '/invoices', label: 'Invoices', icon: FileText },
  { path: '/customers', label: 'Customers', icon: Users },
  { path: '/inventory', label: 'Inventory', icon: Package },
  { path: '/staff', label: 'Staff', icon: UserCircle },
  { path: '/expenses', label: 'Expenses', icon: DollarSign },
  { path: '/reports', label: 'Reports', icon: BarChart3 },
];

function NavLink({ item }: { item: typeof navItems[0] }) {
  const location = useLocation();
  const isActive = location.pathname === item.path;
  const Icon = item.icon;

  return (
    <Link to={item.path}
      className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${isActive
          ? (item.highlight ? 'bg-indigo-600 shadow-sm' : 'bg-indigo-800/60')
          : item.highlight
            ? 'bg-indigo-600/40 hover:bg-indigo-600'
            : 'hover:bg-indigo-800/40'
        }`}>
      <Icon className="w-5 h-5" />
      <span className="font-medium">{item.label}</span>
    </Link>
  );
}

function Layout({ children, user, onLogout }: { children: React.ReactNode; user: any; onLogout: () => void }) {
  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className="w-64 bg-indigo-900 text-white flex flex-col shadow-xl z-10">
        <div className="p-6 border-b border-indigo-800">
          <h2 className="text-xl font-bold tracking-tight">Techware BillSoft</h2>
          <p className="text-indigo-300 text-xs mt-1">v2.0 — Billing & Inventory</p>
        </div>
        <nav className="flex-1 px-3 space-y-1 mt-4 overflow-auto">
          {navItems.map(item => <NavLink key={item.path} item={item} />)}
        </nav>
        <div className="p-4 border-t border-indigo-800">
          <div className="flex items-center justify-between">
            <div className="min-w-0">
              <p className="text-sm font-medium truncate">{user?.first_name || 'User'}</p>
              <p className="text-xs text-indigo-300 truncate">{user?.role || 'cashier'}</p>
            </div>
            <button onClick={onLogout} className="text-indigo-300 hover:text-white p-2 rounded-lg hover:bg-indigo-800 transition-colors"
              title="Sign Out">
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {children}
      </main>
    </div>
  );
}

function App() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (stored) {
      try { setUser(JSON.parse(stored)); } catch { /* ignore */ }
    }
  }, []);

  const handleLogin = (u: any) => setUser(u);
  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
  };

  if (!user) return <Login onLogin={handleLogin} />;

  return (
    <BrowserRouter>
      <Layout user={user} onLogout={handleLogout}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/pos" element={<POS />} />
          <Route path="/invoices" element={<Invoices />} />
          <Route path="/customers" element={<Customers />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/staff" element={<Staff />} />
          <Route path="/expenses" element={<Expenses />} />
          <Route path="/reports" element={<Reports />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
