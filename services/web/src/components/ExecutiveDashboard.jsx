import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Briefcase,
    ShieldCheck,
    TrendingUp,
    Users,
    Clock,
    AlertCircle,
    CheckCircle2,
    ArrowRight,
    Target,
    Activity,
    Zap,
    LayoutDashboard
} from 'lucide-react';
import { AgentActivityTheater } from './theater/AgentActivityTheater';
import AgentActivityFeed from './transparency/AgentActivityFeed';

const ExecutiveDashboard = () => {
    const [activeTab, setActiveTab] = useState('overview');

    // Mock Data (In production, these come from our new backend services)
    const businessIdentity = {
        name: "The Artisanal Bakery",
        niche: "High-end sourdough and French pastries",
        voice: "Warm, authentic, premium"
    };

    const agentStats = {
        total: 124,
        active: 18,
        success_rate: 99.4,
        tasks_completed: 892
    };

    const authQueue = [
        { id: "req_1", agent: "ContentStrategist", action: "Post Instagram Reels Series", risk: "Medium" },
        { id: "req_2", agent: "GrowthIntelligence", action: "Reallocate $1,200 Ad Budget", risk: "High" }
    ];

    const roadmap = [
        { date: "Feb 20", title: "Executive Suite UI Integration", status: "In Progress" },
        { date: "Mar 10", title: "Scale High-Performing Reels", status: "Planned" },
        { date: "Apr 15", title: "Launch AI-Powered Retention Campaign", status: "Planned" }
    ];

    return (
        <div className="min-h-screen bg-[#F8FAFC] text-slate-900 p-8 space-y-8">
            {/* Header: Business Identity */}
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-white/70 backdrop-blur-xl p-8 rounded-3xl premium-shadow border border-white/40">
                <div className="flex items-center gap-6">
                    <div className="p-4 bg-indigo-600 rounded-2xl text-white shadow-lg shadow-indigo-100">
                        <Briefcase size={36} />
                    </div>
                    <div>
                        <h1 className="text-4xl font-black tracking-tight text-slate-900">{businessIdentity.name}</h1>
                        <p className="text-slate-400 font-bold uppercase tracking-widest text-xs mt-1">{businessIdentity.niche}</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    <span className="px-3 py-1 bg-emerald-50 text-emerald-600 rounded-full text-[10px] font-black uppercase tracking-wider border border-emerald-100 flex items-center gap-1">
                        <Activity size={12} /> {businessIdentity.voice} Voice Active
                    </span>
                    <button className="p-3 bg-slate-900 text-white rounded-2xl hover:bg-slate-800 transition-all shadow-xl">
                        <LayoutDashboard size={20} />
                    </button>
                </div>
            </header>

            {/* Grid Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">

                {/* Left Column: Workforce & Activity */}
                <div className="lg:col-span-2 space-y-10">

                    {/* Agent Activity Theater - Visual Command Center */}
                    <div className="premium-shadow rounded-3xl overflow-hidden border border-slate-200">
                        <AgentActivityTheater selectedWorkflowName="Active Strategic Operations" />
                    </div>

                    {/* Workforce Overview Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                        {[
                            { label: "Elite Workforce", val: agentStats.total, icon: Users, color: "text-indigo-600", bg: "bg-indigo-50" },
                            { label: "Active Nodes", val: agentStats.active, icon: Activity, color: "text-emerald-600", bg: "bg-emerald-50" },
                            { label: "Success Rate", val: `${agentStats.success_rate}%`, icon: ShieldCheck, color: "text-blue-600", bg: "bg-blue-50" },
                            { label: "Deliverables", val: agentStats.tasks_completed, icon: Zap, color: "text-pink-600", bg: "bg-pink-50" }
                        ].map((stat, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: i * 0.1 }}
                                className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm hover:border-indigo-200 transition-all group"
                            >
                                <div className={`p-2 w-10 h-10 rounded-xl ${stat.bg} ${stat.color} mb-4 flex items-center justify-center group-hover:scale-110 transition-transform`}>
                                    <stat.icon size={20} />
                                </div>
                                <h3 className="text-3xl font-black text-slate-900">{stat.val}</h3>
                                <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">{stat.label}</p>
                            </motion.div>
                        ))}
                    </div>

                    {/* Strategic Roadmap */}
                    <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-200">
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-xl font-bold flex items-center gap-3">
                                <Target className="text-indigo-600" size={28} /> 90-Day Strategic Anchors
                            </h2>
                            <button className="text-indigo-600 text-xs font-black uppercase tracking-widest hover:underline flex items-center gap-2">
                                Launch Strategic Engine <ArrowRight size={14} />
                            </button>
                        </div>
                        <div className="space-y-4">
                            {roadmap.map((milestone, i) => (
                                <div key={i} className="flex items-center gap-6 p-5 rounded-2xl bg-slate-50/50 border border-slate-100 hover:bg-white hover:shadow-md transition-all group">
                                    <div className="min-w-[70px] text-[10px] font-black text-slate-400 uppercase tracking-tighter">{milestone.date}</div>
                                    <div className="flex-1">
                                        <h4 className="font-bold text-slate-900 group-hover:text-indigo-600 transition-colors">{milestone.title}</h4>
                                        <p className="text-[10px] text-slate-400 font-bold uppercase mt-1">Status: {milestone.status}</p>
                                    </div>
                                    {milestone.status === "In Progress" ? (
                                        <div className="p-2 bg-amber-50 rounded-full">
                                            <Clock size={16} className="text-amber-500 animate-spin-slow" />
                                        </div>
                                    ) : (
                                        <div className="p-2 bg-emerald-50 rounded-full">
                                            <CheckCircle2 size={16} className="text-emerald-400" />
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </section>

                </div>

                {/* Right Column: Authorization & Metrics */}
                <div className="space-y-10">

                    {/* Authorization Board */}
                    <section className="bg-slate-900 text-white p-8 rounded-3xl shadow-2xl relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-8 opacity-10">
                            <ShieldCheck size={80} />
                        </div>
                        <div className="flex items-center justify-between mb-8 relative z-10">
                            <h2 className="text-xl font-bold flex items-center gap-3">
                                <ShieldCheck className="text-emerald-400" size={28} /> Authority Board
                            </h2>
                            <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 text-[10px] font-black rounded-lg border border-emerald-500/30 uppercase tracking-widest">
                                {authQueue.length} Pending
                            </span>
                        </div>
                        <div className="space-y-4 relative z-10">
                            {authQueue.map((req, i) => (
                                <div key={i} className="bg-white/5 backdrop-blur-md p-5 rounded-2xl border border-white/10 hover:bg-white/10 transition-all cursor-pointer group">
                                    <div className="flex justify-between items-start mb-3">
                                        <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest italic group-hover:text-indigo-400">@{req.agent}</span>
                                        <span className={`text-[9px] font-black px-2 py-0.5 rounded uppercase tracking-tighter ${req.risk === 'High' ? 'bg-red-500/20 text-red-300' : 'bg-amber-500/20 text-amber-300'}`}>
                                            {req.risk} Risk
                                        </span>
                                    </div>
                                    <h4 className="font-bold text-sm mb-4 leading-relaxed">{req.action}</h4>
                                    <div className="flex gap-2">
                                        <button className="flex-1 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all shadow-lg shadow-emerald-900/40">Authorize</button>
                                        <button className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-[10px] font-black uppercase tracking-widest rounded-xl transition-all text-slate-400">Review</button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* Quick Insights (Aggregated from Growth Dashboard) */}
                    <section className="bg-white p-8 rounded-3xl shadow-sm border border-slate-200 overflow-hidden relative">
                        <div className="absolute top-0 right-0 p-8 opacity-5">
                            <TrendingUp size={100} className="text-indigo-600" />
                        </div>
                        <h2 className="text-xl font-bold mb-8 flex items-center gap-3 relative z-10">
                            <TrendingUp className="text-indigo-600" size={28} /> Strategic Signal Room
                        </h2>
                        <div className="space-y-4 relative z-10">
                            <div className="p-5 bg-emerald-50 border border-emerald-100 rounded-2xl group hover:shadow-lg hover:scale-[1.02] transition-all cursor-pointer">
                                <p className="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-2">High Impact Opportunity</p>
                                <h5 className="font-bold text-slate-800 text-sm">Switch to YouTube Shorts</h5>
                                <p className="text-xs text-slate-500 mt-2 font-medium">Expected ROI: <span className="text-emerald-600 font-bold">+45% Reach</span></p>
                            </div>
                            <div className="p-5 bg-indigo-50 border border-indigo-100 rounded-2xl group hover:shadow-lg hover:scale-[1.02] transition-all cursor-pointer">
                                <p className="text-[10px] font-black text-indigo-600 uppercase tracking-widest mb-2">Operations Signal</p>
                                <h5 className="font-bold text-slate-800 text-sm">Automate Lead Scoring</h5>
                                <p className="text-xs text-slate-500 mt-2 font-medium">Efficiency Gain: <span className="text-indigo-600 font-bold">2.7h daily</span></p>
                            </div>
                        </div>
                        <button className="w-full mt-6 py-3 border border-slate-200 rounded-2xl text-[10px] font-black uppercase tracking-widest text-slate-400 hover:bg-slate-50 transition-all flex items-center justify-center gap-2">
                            Full Growth Dashboard <ArrowRight size={12} />
                        </button>
                    </section>

                </div>

            </div>
        </div>
    );
};

export default ExecutiveDashboard;
