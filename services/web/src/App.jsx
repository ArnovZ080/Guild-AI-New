import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Calendar, Target, Settings, Sliders, Brain, Link as LinkIcon, Sparkles, MessageSquare } from 'lucide-react';
import ChatInterface from './components/chat/ChatInterface';
import ExecutiveDashboard from './components/ExecutiveDashboard';
import CalendarView from './components/calendar/CalendarView';
import GoalsDashboard from './components/goals/GoalsDashboard';
import MemoryAgent from './components/memory/MemoryAgent';
import ConnectorManager from './components/connectors/ConnectorManager';
import WorkflowBuilder from './components/workflows/WorkflowBuilder';
import OnboardingFlow from './components/onboarding/OnboardingFlow';
import ContentHub from './components/dashboard/ContentHub';

// New Launch Pages
import LandingPage from './pages/LandingPage';
import PricingPage from './pages/PricingPage';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import WaitlistPage from './pages/WaitlistPage';
import PrivacyPolicyPage from './pages/legal/PrivacyPolicyPage';
import TermsPage from './pages/legal/TermsPage';
import RefundPolicyPage from './pages/legal/RefundPolicyPage';

function AppContent() {
  const location = useLocation();
  const publicPaths = ['/landing', '/login', '/signup', '/waitlist', '/pricing', '/privacy', '/terms', '/refund'];
  const isPublicPage = publicPaths.includes(location.pathname);

  return (
    <div className="flex h-screen" style={{ backgroundColor: '#090a0f' }}>
      {/* Liquid ambient background — always behind everything */}
      {/* Liquid ambient background now lives in App root */}

      {/* Sidebar Navigation - Hidden on Public Pages */}
      {!isPublicPage && (
        <aside className="w-64 glass-panel text-zinc-400 flex flex-col fixed h-full z-10 border-r border-white/5">
          <div className="p-6 border-b border-white/5">
            <h2 className="text-xl font-bold tracking-tight flex items-center gap-2 font-heading">
              <div className="w-8 h-8 gradient-cobalt rounded-lg flex items-center justify-center shadow-lg shadow-cobalt/20">
                <span className="font-bold text-white text-sm">G</span>
              </div>
              <span className="text-gradient-cobalt">Guild AI</span>
            </h2>
          </div>

          <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
            <Link to="/" className="flex items-center gap-3 px-4 py-2.5 bg-cobalt/15 rounded-lg text-zinc-100 font-medium border border-cobalt/20 transition-all duration-200">
              <LayoutDashboard size={18} strokeWidth={1.5} /> Dashboard
            </Link>
            <Link to="/chat" className="flex items-center gap-3 px-4 py-2.5 hover:bg-white/5 rounded-lg text-zinc-500 hover:text-zinc-300 font-medium transition-all duration-200">
              <MessageSquare size={18} strokeWidth={1.5} /> Executive Chat
            </Link>
            <Link to="/calendar" className="flex items-center gap-3 px-4 py-2.5 hover:bg-white/5 rounded-lg text-zinc-500 hover:text-zinc-300 font-medium transition-all duration-200">
              <Calendar size={18} strokeWidth={1.5} /> Strategic Calendar
            </Link>
            <Link to="/content" className="flex items-center gap-3 px-4 py-2.5 hover:bg-white/5 rounded-lg text-zinc-500 hover:text-zinc-300 font-medium transition-all duration-200">
              <Sparkles size={18} strokeWidth={1.5} /> Content Hub
            </Link>
            <Link to="/workflows" className="flex items-center gap-3 px-4 py-2.5 hover:bg-white/5 rounded-lg text-zinc-500 hover:text-zinc-300 font-medium transition-all duration-200">
              <Sliders size={18} strokeWidth={1.5} /> Workflow Builder
            </Link>
            <div className="pt-4 mt-4 border-t border-white/5">
              <p className="px-4 text-[10px] font-medium text-zinc-700 uppercase tracking-wider mb-2">Platform</p>
              <Link to="/memory" className="flex items-center gap-3 px-4 py-2.5 hover:bg-white/5 rounded-lg text-zinc-500 hover:text-zinc-300 font-medium transition-all duration-200">
                <Brain size={18} strokeWidth={1.5} /> Memory
              </Link>
              <Link to="/connectors" className="flex items-center gap-3 px-4 py-2.5 hover:bg-white/5 rounded-lg text-zinc-500 hover:text-zinc-300 font-medium transition-all duration-200">
                <LinkIcon size={18} strokeWidth={1.5} /> Connectors
              </Link>
              <Link to="/onboarding" className="flex items-center gap-3 px-4 py-2.5 hover:bg-white/5 rounded-lg text-zinc-500 hover:text-zinc-300 font-medium transition-all duration-200">
                <Sparkles size={18} strokeWidth={1.5} /> Onboarding
              </Link>
            </div>
          </nav>

          <div className="p-4 border-t border-white/5">
            <div className="flex items-center gap-3 px-2">
              <div className="w-8 h-8 rounded-full gradient-cobalt border border-white/5" />
              <div>
                <p className="text-sm font-medium text-zinc-300">Arno van Zyl</p>
                <p className="text-xs text-zinc-600">CEO</p>
              </div>
            </div>
          </div>
        </aside>
      )}

      {/* Main Content Area */}
      <main className={`flex-1 overflow-y-auto ${!isPublicPage ? 'ml-64' : ''}`}>
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

          {/* Protected Routes (Dashboard) */}
          <Route path="/" element={<ExecutiveDashboard />} />
          <Route path="/chat" element={<ChatInterface />} />
          <Route path="/calendar" element={<CalendarView />} />
          <Route path="/content" element={<ContentHub />} />
          <Route path="/workflows" element={<WorkflowBuilder />} />
          <Route path="/memory" element={<MemoryAgent />} />
          <Route path="/connectors" element={<ConnectorManager />} />
          <Route path="/onboarding" element={<div className="p-8 max-w-4xl mx-auto"><OnboardingFlow /></div>} />
          <Route path="/settings" element={<div className="p-8 text-zinc-500">Settings Coming Soon</div>} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <>
      <div className="ambient-bg" aria-hidden="true" />
      <Router>
        <AppContent />
      </Router>
    </>
  );
}

export default App;
