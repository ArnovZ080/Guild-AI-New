import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Calendar, Target, Settings, Sliders, Brain, Link as LinkIcon, Sparkles, MessageSquare, Sun, Moon, Monitor } from 'lucide-react';
import { ThemeProvider, useTheme } from './components/ThemeProvider';
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

function ThemeToggle() {
    const { theme, setTheme, resolvedTheme } = useTheme();
    return (
        <div className="flex items-center gap-1 p-1 rounded-xl bg-gray-100 dark:bg-white/5 border border-gray-200/60 dark:border-white/5">
            <button
                onClick={() => setTheme('light')}
                className={`p-1.5 rounded-lg transition-all ${theme === 'light' ? 'bg-white dark:bg-white/10 shadow-sm text-amber-500' : 'text-gray-400 dark:text-zinc-600 hover:text-gray-600 dark:hover:text-zinc-400'}`}
                title="Light mode"
            >
                <Sun size={14} strokeWidth={1.5} />
            </button>
            <button
                onClick={() => setTheme('system')}
                className={`p-1.5 rounded-lg transition-all ${theme === 'system' ? 'bg-white dark:bg-white/10 shadow-sm text-blue-500' : 'text-gray-400 dark:text-zinc-600 hover:text-gray-600 dark:hover:text-zinc-400'}`}
                title="System preference"
            >
                <Monitor size={14} strokeWidth={1.5} />
            </button>
            <button
                onClick={() => setTheme('dark')}
                className={`p-1.5 rounded-lg transition-all ${theme === 'dark' ? 'bg-white dark:bg-white/10 shadow-sm text-indigo-500' : 'text-gray-400 dark:text-zinc-600 hover:text-gray-600 dark:hover:text-zinc-400'}`}
                title="Dark mode"
            >
                <Moon size={14} strokeWidth={1.5} />
            </button>
        </div>
    );
}

function NavLink({ to, icon: Icon, label, isActive }) {
    return (
        <Link
            to={to}
            className={`flex items-center gap-3 px-4 py-2.5 rounded-xl font-medium transition-all duration-200 ${isActive
                    ? 'bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400 border border-blue-200/40 dark:border-blue-500/20'
                    : 'text-gray-500 hover:bg-gray-100 hover:text-gray-800 dark:text-zinc-500 dark:hover:bg-white/5 dark:hover:text-zinc-300 border border-transparent'
                }`}
        >
            <Icon size={18} strokeWidth={1.5} />
            {label}
        </Link>
    );
}

function AppContent() {
    const location = useLocation();
    const publicPaths = ['/landing', '/login', '/signup', '/waitlist', '/pricing', '/privacy', '/terms', '/refund'];
    const isPublicPage = publicPaths.includes(location.pathname);

    const navItems = [
        { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
        { to: '/chat', icon: MessageSquare, label: 'Executive Chat' },
        { to: '/calendar', icon: Calendar, label: 'Strategic Calendar' },
        { to: '/content', icon: Sparkles, label: 'Content Hub' },
        { to: '/workflows', icon: Sliders, label: 'Workflow Builder' },
    ];

    const platformItems = [
        { to: '/memory', icon: Brain, label: 'Memory' },
        { to: '/connectors', icon: LinkIcon, label: 'Connectors' },
        { to: '/onboarding', icon: Sparkles, label: 'Onboarding' },
    ];

    return (
        <div className="flex h-screen">
            {/* Sidebar Navigation */}
            {!isPublicPage && (
                <aside className="w-64 flex flex-col fixed h-full z-10 bg-white/80 dark:bg-[#0C1222]/80 backdrop-blur-xl border-r border-gray-200/60 dark:border-white/[0.06]">
                    <div className="p-6 border-b border-gray-200/60 dark:border-white/[0.06]">
                        <h2 className="text-xl font-bold tracking-tight flex items-center gap-2 font-heading">
                            <div className="w-8 h-8 gradient-cobalt rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
                                <span className="font-bold text-white text-sm">G</span>
                            </div>
                            <span className="text-gradient-cobalt">Guild AI</span>
                        </h2>
                    </div>

                    <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
                        {navItems.map(item => (
                            <NavLink
                                key={item.to}
                                to={item.to}
                                icon={item.icon}
                                label={item.label}
                                isActive={location.pathname === item.to}
                            />
                        ))}
                        <div className="pt-4 mt-4 border-t border-gray-200/60 dark:border-white/[0.06]">
                            <p className="px-4 text-[10px] font-medium text-gray-400 dark:text-zinc-700 uppercase tracking-wider mb-2">Platform</p>
                            {platformItems.map(item => (
                                <NavLink
                                    key={item.to}
                                    to={item.to}
                                    icon={item.icon}
                                    label={item.label}
                                    isActive={location.pathname === item.to}
                                />
                            ))}
                        </div>
                    </nav>

                    <div className="p-4 border-t border-gray-200/60 dark:border-white/[0.06] space-y-3">
                        <ThemeToggle />
                        <div className="flex items-center gap-3 px-2">
                            <div className="w-8 h-8 rounded-full gradient-cobalt border border-blue-500/20" />
                            <div>
                                <p className="text-sm font-medium text-gray-800 dark:text-zinc-300">Arno van Zyl</p>
                                <p className="text-xs text-gray-400 dark:text-zinc-600">CEO</p>
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
                    <Route path="/settings" element={<div className="p-8 text-gray-500 dark:text-zinc-500">Settings Coming Soon</div>} />
                </Routes>
            </main>
        </div>
    );
}

function App() {
    return (
        <ThemeProvider>
            <div className="ambient-bg" aria-hidden="true" />
            <Router>
                <AppContent />
            </Router>
        </ThemeProvider>
    );
}

export default App;
