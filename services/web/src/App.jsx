import React, { useState, useEffect, Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import {
  MessageSquare, FileText, Activity, TrendingUp, GitBranch, Settings as SettingsIcon,
  LogOut, ChevronLeft,
} from 'lucide-react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { ThemeProvider } from './components/ThemeProvider';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import ErrorBoundary from './components/ErrorBoundary';
import AmbientEmbers from './components/AmbientEmbers';

/* ── Lazy-loaded views (code-split) ── */
const ChatInterface = lazy(() => import('./components/chat/ChatInterface'));
const ContentQueue = lazy(() => import('./components/content/ContentQueue'));
const AgentActivityTheater = lazy(() => import('./components/theater/AgentActivityTheater'));
const GrowthDashboard = lazy(() => import('./components/dashboard/GrowthDashboard'));
const WorkflowBuilder = lazy(() => import('./components/workflows/WorkflowBuilder'));
const SettingsPage = lazy(() => import('./components/settings/SettingsPage'));
const OnboardingFlow = lazy(() => import('./components/onboarding/OnboardingFlow'));

/* ── Public pages ── */
import LandingPage from './pages/LandingPage';
import PricingPage from './pages/PricingPage';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import WaitlistPage from './pages/WaitlistPage';
import PrivacyPolicyPage from './pages/legal/PrivacyPolicyPage';
import TermsPage from './pages/legal/TermsPage';
import RefundPolicyPage from './pages/legal/RefundPolicyPage';
import AboutUsPage from './pages/AboutUsPage';
import ContactPage from './pages/ContactPage';
import AffiliatesPage from './pages/AffiliatesPage';
import FeaturesPage from './pages/FeaturesPage';
import AIAgentsPage from './pages/AIAgentsPage';
import IntegrationsPage from './pages/IntegrationsPage';


/* ── Suspense fallback ── */
const ViewLoader = () => (
  <div className="flex items-center justify-center h-full min-h-[300px]">
    <div className="w-6 h-6 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin" />
  </div>
);



/* ═══════════════════════════════════════════
   Sidebar NavLink
   ═══════════════════════════════════════════ */
function NavLink({ to, icon: Icon, label, isActive, collapsed, badge }) {
  return (
    <Link
      to={to}
      className={`group relative flex items-center gap-3 px-3 py-2.5 rounded-xl font-medium transition-all duration-200
        ${isActive
          ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20'
          : 'text-zinc-500 hover:bg-white/5 hover:text-zinc-300 border border-transparent'
        }
        ${collapsed ? 'justify-center' : ''}
      `}
      title={collapsed ? label : undefined}
    >
      <Icon size={18} strokeWidth={1.5} />
      {!collapsed && <span className="text-sm">{label}</span>}
      {badge > 0 && (
        <span className={`absolute ${collapsed ? '-top-1 -right-1' : 'right-2'} min-w-[18px] h-[18px] flex items-center justify-center text-[10px] font-bold rounded-full bg-indigo-500 text-white`}>
          {badge > 99 ? '99+' : badge}
        </span>
      )}
      {collapsed && (
        <span className="absolute left-full ml-2 px-2 py-1 text-xs rounded-md bg-zinc-800 text-zinc-200 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50">
          {label}
        </span>
      )}
    </Link>
  );
}

/* ═══════════════════════════════════════════
   Mobile Bottom TabBar
   ═══════════════════════════════════════════ */
function MobileTabBar({ navItems, currentPath }) {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 flex items-center justify-around h-16 bg-surface-base/95 backdrop-blur-xl border-t border-white/[0.06] md:hidden">
      {navItems.map(({ to, icon: Icon, label, badge }) => {
        const active = currentPath === to || (to !== '/' && currentPath.startsWith(to));
        return (
          <Link
            key={to}
            to={to}
            className={`relative flex flex-col items-center gap-0.5 py-1 px-3 rounded-lg transition-colors ${active ? 'text-indigo-400' : 'text-zinc-600'}`}
          >
            <Icon size={20} strokeWidth={1.5} />
            <span className="text-[10px]">{label}</span>
            {badge > 0 && (
              <span className="absolute -top-0.5 right-0 min-w-[14px] h-[14px] flex items-center justify-center text-[8px] font-bold rounded-full bg-indigo-500 text-white">
                {badge}
              </span>
            )}
          </Link>
        );
      })}
    </nav>
  );
}



/* ═══════════════════════════════════════════
   Main App Content (with sidebar)
   ═══════════════════════════════════════════ */
function AppContent() {
  const location = useLocation();
  const { user, logout } = useAuth();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const publicPaths = [
    '/landing', '/login', '/signup', '/waitlist', '/pricing', 
    '/privacy', '/terms', '/refund', '/about', '/contact', 
    '/affiliates', '/features', '/agents', '/integrations'
  ];

  const isPublicPage = publicPaths.includes(location.pathname);

  const navItems = [
    { to: '/', icon: MessageSquare, label: 'Chat', badge: 0 },
    { to: '/content', icon: FileText, label: 'Content', badge: 0 },
    { to: '/theater', icon: Activity, label: 'Theater', badge: 0 },
    { to: '/growth', icon: TrendingUp, label: 'Growth', badge: 0 },
    { to: '/workflows', icon: GitBranch, label: 'Workflows', badge: 0 },
    { to: '/settings', icon: SettingsIcon, label: 'Settings', badge: 0 },
  ];

  const currentPath = location.pathname;

  return (
    <div className="flex h-screen">
      {/* ── Desktop Sidebar ── */}
      {!isPublicPage && user && (
        <aside
          className={`hidden md:flex flex-col fixed h-full z-20 transition-all duration-300 bg-surface-base/80 backdrop-blur-xl border-r border-white/[0.06]
            ${sidebarCollapsed ? 'w-[68px]' : 'w-60'}
          `}
        >
          {/* Logo */}
          <div className="p-4 border-b border-white/[0.06] flex items-center gap-2">
            <div className="w-8 h-8 gradient-cobalt rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20 flex-shrink-0">
              <span className="font-bold text-white text-sm">G</span>
            </div>
            {!sidebarCollapsed && (
              <span className="text-gradient-cobalt font-heading text-lg font-bold tracking-tight">Guild AI</span>
            )}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className={`ml-auto p-1 rounded-md text-zinc-600 hover:text-zinc-400 hover:bg-white/5 transition-colors ${sidebarCollapsed ? 'rotate-180' : ''}`}
            >
              <ChevronLeft size={16} strokeWidth={1.5} />
            </button>
          </div>

          {/* Nav Links */}
          <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                {...item}
                isActive={currentPath === item.to || (item.to !== '/' && currentPath.startsWith(item.to))}
                collapsed={sidebarCollapsed}
              />
            ))}
          </nav>

          {/* Bottom section */}
          <div className="p-3 border-t border-white/[0.06] space-y-2">
            {user && (
              <div className="flex items-center gap-2 px-1">
                <div className="w-7 h-7 rounded-full gradient-cobalt border border-blue-500/20 flex-shrink-0" />
                {!sidebarCollapsed && (
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-zinc-300 truncate">{user.displayName || user.email?.split('@')[0]}</p>
                    <p className="text-[10px] text-zinc-600 truncate">{user.email}</p>
                  </div>
                )}
                <button onClick={logout} className="p-1.5 rounded-md text-zinc-600 hover:text-red-400 hover:bg-white/5 transition-colors" title="Logout">
                  <LogOut size={14} strokeWidth={1.5} />
                </button>
              </div>
            )}
          </div>
        </aside>
      )}

      {/* ── Mobile Bottom Tab Bar ── */}
      {!isPublicPage && user && (
        <MobileTabBar navItems={navItems.slice(0, 5)} currentPath={currentPath} />
      )}

      {/* ── Main Content ── */}
      <main
        className={`flex-1 overflow-y-auto transition-all duration-300
          ${!isPublicPage && user ? (sidebarCollapsed ? 'md:ml-[68px]' : 'md:ml-60') : ''}
          ${!isPublicPage && user ? 'pb-16 md:pb-0' : ''}
        `}
      >
        <Routes>
          {/* Public Routes */}
          <Route path="/landing" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/waitlist" element={<WaitlistPage />} />
          <Route path="/pricing" element={<PricingPage />} />
          <Route path="/privacy" element={<PrivacyPolicyPage />} />
          <Route path="/terms" element={<TermsPage />} />
          <Route path="/refund" element={<RefundPolicyPage />} />
          <Route path="/about" element={<AboutUsPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/affiliates" element={<AffiliatesPage />} />
          <Route path="/features" element={<FeaturesPage />} />
          <Route path="/agents" element={<AIAgentsPage />} />
          <Route path="/integrations" element={<IntegrationsPage />} />


          {/* Protected Routes (lazy-loaded with ErrorBoundary) */}
          <Route path="/" element={<ProtectedRoute><ErrorBoundary><Suspense fallback={<ViewLoader />}><ChatInterface /></Suspense></ErrorBoundary></ProtectedRoute>} />
          <Route path="/content" element={<ProtectedRoute><ErrorBoundary><Suspense fallback={<ViewLoader />}><ContentQueue /></Suspense></ErrorBoundary></ProtectedRoute>} />
          <Route path="/theater" element={<ProtectedRoute><ErrorBoundary><Suspense fallback={<ViewLoader />}><AgentActivityTheater /></Suspense></ErrorBoundary></ProtectedRoute>} />
          <Route path="/growth" element={<ProtectedRoute><ErrorBoundary><Suspense fallback={<ViewLoader />}><GrowthDashboard /></Suspense></ErrorBoundary></ProtectedRoute>} />
          <Route path="/workflows" element={<ProtectedRoute><ErrorBoundary><Suspense fallback={<ViewLoader />}><WorkflowBuilder /></Suspense></ErrorBoundary></ProtectedRoute>} />
          <Route path="/settings" element={<ProtectedRoute><ErrorBoundary><Suspense fallback={<ViewLoader />}><SettingsPage /></Suspense></ErrorBoundary></ProtectedRoute>} />
          <Route path="/onboarding" element={<ProtectedRoute><ErrorBoundary><Suspense fallback={<ViewLoader />}><div className="p-8 max-w-4xl mx-auto"><OnboardingFlow /></div></Suspense></ErrorBoundary></ProtectedRoute>} />

          {/* Catch-all → Chat */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      <ToastContainer
        position="bottom-right"
        theme="dark"
        toastClassName="!bg-surface-raised !border !border-white/[0.06] !text-zinc-200 !rounded-xl !shadow-2xl"
      />
    </div>
  );
}

import ScrollToTop from './components/ScrollToTop';

/* ── Root App ── */
function App() {
  return (
    <ThemeProvider>
      <Router>
        <ScrollToTop />
        <AuthProvider>
          <AmbientEmbers />
          <AppContent />
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default App;
