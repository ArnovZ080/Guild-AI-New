import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
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

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-slate-50">
        {/* Sidebar Navigation */}
        <aside className="w-64 bg-slate-900 text-white flex flex-col fixed h-full z-10">
          <div className="p-6 border-b border-slate-800">
            <h2 className="text-xl font-bold tracking-tight flex items-center gap-2">
              <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                <span className="font-bold text-white">E</span>
              </div>
              Executive
            </h2>
          </div>

          <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
            <Link to="/" className="flex items-center gap-3 px-4 py-3 bg-indigo-600 rounded-xl text-white font-medium shadow-lg shadow-indigo-900/20 hover:bg-indigo-700 transition-colors">
              <LayoutDashboard size={20} /> Dashboard
            </Link>
            <Link to="/chat" className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 rounded-xl text-slate-300 hover:text-white font-medium transition-colors">
              <MessageSquare size={20} /> Executive Chat
            </Link>
            <Link to="/calendar" className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 rounded-xl text-slate-300 hover:text-white font-medium transition-colors">
              <Calendar size={20} /> Strategic Calendar
            </Link>
            <Link to="/content" className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 rounded-xl text-slate-300 hover:text-white font-medium transition-colors">
              <Sparkles size={20} /> Content Hub
            </Link>
            <Link to="/workflows" className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 rounded-xl text-slate-300 hover:text-white font-medium transition-colors">
              <Sliders size={20} /> Workflow Builder
            </Link>
            <div className="pt-4 mt-4 border-t border-slate-800">
              <p className="px-4 text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Platform</p>
              <Link to="/memory" className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 rounded-xl text-slate-300 hover:text-white font-medium transition-colors">
                <Brain size={20} /> Memory
              </Link>
              <Link to="/connectors" className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 rounded-xl text-slate-300 hover:text-white font-medium transition-colors">
                <LinkIcon size={20} /> Connectors
              </Link>
              <Link to="/onboarding" className="flex items-center gap-3 px-4 py-3 hover:bg-slate-800 rounded-xl text-slate-300 hover:text-white font-medium transition-colors">
                <Sparkles size={20} /> Onboarding
              </Link>
            </div>
          </nav>

          <div className="p-4 border-t border-slate-800">
            <div className="flex items-center gap-3 px-2">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 border border-white/20" />
              <div>
                <p className="text-sm font-bold">Arno van Zyl</p>
                <p className="text-xs text-slate-400">CEO</p>
              </div>
            </div>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 ml-64 overflow-y-auto">
          <Routes>
            <Route path="/" element={<ExecutiveDashboard />} />
            <Route path="/chat" element={<ChatInterface />} />
            <Route path="/calendar" element={<CalendarView />} />
            <Route path="/content" element={<ContentHub />} />
            <Route path="/workflows" element={<WorkflowBuilder />} />
            <Route path="/memory" element={<MemoryAgent />} />
            <Route path="/connectors" element={<ConnectorManager />} />
            <Route path="/onboarding" element={<div className="p-8 max-w-4xl mx-auto"><OnboardingFlow /></div>} />
            <Route path="/settings" element={<div className="p-8 text-slate-500">Settings Coming Soon</div>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
