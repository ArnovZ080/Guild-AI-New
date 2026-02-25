import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Calendar as CalendarIcon,
    Plus,
    Clock,
    Users,
    DollarSign,
    Target,
    Bell,
    ChevronLeft,
    ChevronRight,
    Filter,
    Search,
    RefreshCw,
    ExternalLink,
    Brain,
    X,
    MessageSquare,
    Send,
    Bot,
    Zap,
    Anchor,
    ShieldCheck
} from 'lucide-react';
import { format, addDays, startOfWeek, endOfWeek, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isSameDay, parseISO } from 'date-fns';

// Phase 3: Strategic Anchors (Milestones from Phase 2)
const strategicAnchors = [
    {
        id: 'anchor_1',
        title: 'Q1 Growth Infrastructure',
        date: new Date(2026, 1, 15), // Feb 15
        type: 'milestone',
        status: 'completed',
        details: 'Deployment of Strategic Planning Engine & Project Manager.'
    },
    {
        id: 'anchor_2',
        title: 'Executive Suite Integration',
        date: new Date(2026, 1, 20), // Feb 20 (Today-ish)
        type: 'milestone',
        status: 'in_progress',
        details: 'Unifying legacy UI into the Orchestrator-led suite.'
    },
    {
        id: 'anchor_3',
        title: 'Scale High-Performing Reels',
        date: new Date(2026, 2, 10), // Mar 10
        type: 'milestone',
        status: 'planned',
        details: 'Automated cross-posting and viral sentiment analysis.'
    }
];

// Phase 3: Autonomous Routines (Triggers from Phase 2)
const autonomousRoutines = [
    { id: 'trig_1', title: 'Daily Sentiment Sync', time: '09:00', icon: Zap, color: 'text-amber-500' },
    { id: 'trig_2', title: 'Weekly ROI Audit', day: 'Monday', icon: ShieldCheck, color: 'text-emerald-500' },
    { id: 'trig_3', title: 'Ad-Spend Reallocation', trigger: 'Drift Detected', icon: DollarSign, color: 'text-indigo-500' }
];

const CalendarView = () => {
    const [currentDate, setCurrentDate] = useState(new Date(2026, 1, 1)); // Set to February 2026 for demo
    const [viewMode, setViewMode] = useState('month');
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [showPAChat, setShowPAChat] = useState(false);

    // PA Chat State (Refactored to Orchestrator Voice)
    const [paMessages, setPaMessages] = useState([
        {
            id: 1,
            role: 'assistant',
            content: "Strategic Calendar active. Your 90-day roadmap anchors are synchronized with the workforce. I've noted a slight drift in Content ROI; shall I re-prioritize the upcoming 'Sourdough Masterclass' milestones?",
            timestamp: new Date()
        }
    ]);
    const [paInput, setPaInput] = useState('');

    const handlePAMessage = (e) => {
        e.preventDefault();
        if (!paInput.trim()) return;

        const userMsg = { id: Date.now(), role: 'user', content: paInput, timestamp: new Date() };
        setPaMessages(prev => [...prev, userMsg]);
        setPaInput('');

        setTimeout(() => {
            const botMsg = {
                id: Date.now() + 1,
                role: 'assistant',
                content: "Adjustments acknowledged. Orchestrating milestone shift in the Strategic Engine. Your calendar will reflect these updates momentarily.",
                timestamp: new Date()
            };
            setPaMessages(prev => [...prev, botMsg]);
        }, 1000);
    };

    const nextPeriod = () => {
        setCurrentDate(addDays(currentDate, 30));
    };

    const prevPeriod = () => {
        setCurrentDate(addDays(currentDate, -30));
    };

    const getDaysInView = () => {
        const start = startOfWeek(startOfMonth(currentDate));
        const end = endOfWeek(endOfMonth(currentDate));
        return eachDayOfInterval({ start, end });
    };

    return (
        <div className="p-8 max-w-7xl mx-auto space-y-8 bg-[#F8FAFC] min-h-screen">
            {/* Premium Header */}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                    <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight flex items-center gap-3">
                        <CalendarIcon className="text-indigo-600" size={32} /> Strategic Calendar
                    </h1>
                    <p className="text-slate-500 font-medium">Visualizing the 90-day Roadmap & Autonomous Routines</p>
                </div>
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => setShowPAChat(!showPAChat)}
                        className={`px-4 py-2 rounded-xl transition-all flex items-center gap-2 font-bold text-sm ${showPAChat ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'}`}
                    >
                        <Bot size={18} />
                        <span>Orchestrator Sync</span>
                    </button>
                    <div className="flex items-center gap-1 bg-slate-100 rounded-xl p-1.5 border border-slate-200">
                        <button onClick={prevPeriod} className="p-1.5 hover:bg-white rounded-lg shadow-sm transition-all text-slate-500"><ChevronLeft size={18} /></button>
                        <span className="px-4 text-sm font-black text-slate-700 w-40 text-center uppercase tracking-widest">{format(currentDate, 'MMMM yyyy')}</span>
                        <button onClick={nextPeriod} className="p-1.5 hover:bg-white rounded-lg shadow-sm transition-all text-slate-500"><ChevronRight size={18} /></button>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                {/* Main Calendar Area */}
                <div className="lg:col-span-3 space-y-6">
                    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 min-h-[700px]">
                        <div className="grid grid-cols-7 gap-px rounded-xl overflow-hidden border border-slate-200 bg-slate-200">
                            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                                <div key={day} className="bg-slate-50/80 backdrop-blur-sm p-4 text-center text-[10px] font-black text-slate-400 uppercase tracking-widest">
                                    {day}
                                </div>
                            ))}
                            {getDaysInView().map((day, i) => {
                                const isToday = isSameDay(day, new Date());
                                const isCurrentMonth = isSameMonth(day, currentDate);
                                const dayAnchors = strategicAnchors.filter(a => isSameDay(a.date, day));

                                return (
                                    <div key={i} className={`bg-white min-h-[120px] p-3 transition-all hover:bg-slate-50/50 relative group ${!isCurrentMonth ? 'opacity-30 grayscale-[0.5]' : ''}`}>
                                        <div className={`text-sm font-black mb-3 ${isToday ? 'bg-indigo-600 text-white w-7 h-7 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-200' : 'text-slate-400'}`}>
                                            {format(day, 'd')}
                                        </div>

                                        <div className="space-y-1.5">
                                            {dayAnchors.map(anchor => (
                                                <div
                                                    key={anchor.id}
                                                    className={`p-1.5 rounded-lg text-[10px] font-bold border flex items-center gap-1 shadow-sm transition-transform cursor-pointer hover:scale-105 ${anchor.status === 'completed' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
                                                            anchor.status === 'in_progress' ? 'bg-indigo-50 text-indigo-700 border-indigo-100' :
                                                                'bg-slate-50 text-slate-600 border-slate-200'
                                                        }`}
                                                >
                                                    <Anchor size={10} className={anchor.status === 'in_progress' ? 'animate-pulse' : ''} />
                                                    <span className="truncate">{anchor.title}</span>
                                                </div>
                                            ))}
                                        </div>

                                        {isToday && (
                                            <div className="absolute top-3 right-3 flex gap-1">
                                                <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-ping" />
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </div>

                {/* Sidebar / Orchestrator Sync */}
                <div className="space-y-8">
                    <AnimatePresence>
                        {showPAChat && (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                                className="bg-white rounded-2xl shadow-2xl border border-indigo-100 overflow-hidden flex flex-col h-[500px]"
                            >
                                <div className="bg-indigo-600 p-5 text-white flex items-center justify-between">
                                    <h3 className="font-black text-xs uppercase tracking-widest flex items-center gap-2">
                                        <Bot size={18} /> Orchestrator Sync
                                    </h3>
                                    <button onClick={() => setShowPAChat(false)} className="hover:rotate-90 transition-transform"><X size={18} /></button>
                                </div>
                                <div className="flex-1 p-5 overflow-y-auto space-y-4 bg-slate-50/50">
                                    {paMessages.map(msg => (
                                        <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                            <div className={`max-w-[85%] p-4 rounded-2xl text-xs leading-relaxed font-medium shadow-sm ${msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white border border-slate-200 text-slate-700'}`}>
                                                {msg.content}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                                <form onSubmit={handlePAMessage} className="p-4 bg-white border-t border-slate-100 flex gap-2">
                                    <input
                                        type="text"
                                        value={paInput}
                                        onChange={e => setPaInput(e.target.value)}
                                        placeholder="Strategic command..."
                                        className="flex-1 border border-slate-200 rounded-xl px-4 py-3 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-slate-50"
                                    />
                                    <button type="submit" className="bg-indigo-600 text-white p-3 rounded-xl hover:bg-indigo-700 shadow-lg shadow-indigo-100 transition-all"><Send size={16} /></button>
                                </form>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Autonomous Routines Panel */}
                    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                        <h3 className="font-black text-xs text-slate-400 uppercase tracking-widest mb-6 flex items-center gap-2">
                            <Zap size={14} className="text-amber-500" /> Autonomous Routines
                        </h3>
                        <div className="space-y-4">
                            {autonomousRoutines.map(routine => (
                                <div key={routine.id} className="p-4 rounded-xl bg-slate-50/50 border border-slate-100 hover:border-indigo-200 transition-all cursor-pointer group">
                                    <div className="flex justify-between items-start mb-2">
                                        <div className={`p-1.5 rounded-lg bg-white shadow-sm ${routine.color}`}>
                                            <routine.icon size={14} />
                                        </div>
                                        <span className="text-[10px] font-black text-slate-400 uppercase tracking-tighter">
                                            {routine.time || routine.day || routine.trigger}
                                        </span>
                                    </div>
                                    <h4 className="font-bold text-xs text-slate-800 group-hover:text-indigo-600 transition-colors uppercase tracking-tight">{routine.title}</h4>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Strategic Health Map */}
                    <div className="bg-slate-900 text-white p-6 rounded-2xl shadow-xl overflow-hidden relative">
                        <div className="absolute top-0 right-0 p-4 opacity-10">
                            <Target size={64} />
                        </div>
                        <h3 className="font-bold text-sm mb-4">Strategic Health</h3>
                        <div className="space-y-4">
                            <div className="flex justify-between items-center text-xs">
                                <span className="text-slate-400 font-bold uppercase tracking-widest">Q1 Roadmap</span>
                                <span className="font-black text-emerald-400">72%</span>
                            </div>
                            <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: '72%' }}
                                    className="h-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"
                                />
                            </div>
                            <p className="text-[10px] text-slate-500 italic">"Autonomous workforce is operating within ±2% efficiency drift."</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CalendarView;
