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
        <div className="min-h-screen p-8 space-y-8">
            {/* Header: Business Identity */}
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-white dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/[0.06] rounded-2xl p-8 shadow-sm dark:shadow-[0_4px_24px_rgba(0,0,0,0.2)] dark:backdrop-blur-xl">
                <div className="flex items-center gap-6">
                    <div className="p-4 gradient-cobalt rounded-xl shadow-lg shadow-blue-500/20">
                        <Briefcase size={32} strokeWidth={1.5} className="text-white" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-zinc-100 font-heading">{businessIdentity.name}</h1>
                        <p className="text-gray-500 dark:text-zinc-600 font-medium uppercase tracking-widest text-xs mt-1">{businessIdentity.niche}</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    <span className="px-3 py-1 bg-emerald-50 dark:bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 rounded-full text-[10px] font-medium uppercase tracking-wider border border-emerald-200/60 dark:border-emerald-500/20 flex items-center gap-1">
                        <Activity size={12} strokeWidth={1.5} /> {businessIdentity.voice} Voice Active
                    </span>
                    <button className="p-3 bg-gray-100 dark:bg-white/5 text-gray-500 dark:text-zinc-500 rounded-xl hover:bg-gray-200 dark:hover:bg-white/10 transition-all border border-gray-200/60 dark:border-white/5">
                        <LayoutDashboard size={18} strokeWidth={1.5} />
                    </button>
                </div>
            </header>

            {/* Grid Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Left Column: Workforce & Activity */}
                <div className="lg:col-span-2 space-y-8">

                    {/* Agent Activity Theater */}
                    <div className="bg-white dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/[0.06] rounded-2xl overflow-hidden shadow-sm dark:shadow-[0_4px_24px_rgba(0,0,0,0.2)] dark:backdrop-blur-xl">
                        <AgentActivityTheater selectedWorkflowName="Active Strategic Operations" />
                    </div>

                    {/* Workforce Overview Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        {[
                            { label: "Elite Workforce", val: agentStats.total, icon: Users, color: "text-blue-500" },
                            { label: "Active Nodes", val: agentStats.active, icon: Activity, color: "text-emerald-500" },
                            { label: "Success Rate", val: `${agentStats.success_rate}%`, icon: ShieldCheck, color: "text-cyan-500" },
                            { label: "Deliverables", val: agentStats.tasks_completed, icon: Zap, color: "text-amber-500" }
                        ].map((stat, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: i * 0.1 }}
                                className="bg-white dark:bg-white/[0.04] p-5 rounded-2xl border border-gray-200/60 dark:border-white/[0.06] shadow-sm dark:shadow-[0_4px_24px_rgba(0,0,0,0.2)] hover:shadow-md dark:hover:shadow-[0_8px_32px_rgba(0,0,0,0.3)] transition-all group dark:backdrop-blur-xl"
                            >
                                <div className={`p-2 w-9 h-9 rounded-lg bg-gray-100 dark:bg-white/5 ${stat.color} mb-3 flex items-center justify-center group-hover:scale-110 transition-transform`}>
                                    <stat.icon size={18} strokeWidth={1.5} />
                                </div>
                                <h3 className="text-2xl font-bold text-gray-900 dark:text-zinc-100 font-heading">{stat.val}</h3>
                                <p className="text-[10px] text-gray-400 dark:text-zinc-600 font-medium uppercase tracking-widest mt-1">{stat.label}</p>
                            </motion.div>
                        ))}
                    </div>

                    {/* Strategic Roadmap */}
                    <section className="bg-white dark:bg-white/[0.04] p-8 rounded-2xl border border-gray-200/60 dark:border-white/[0.06] shadow-sm dark:shadow-[0_4px_24px_rgba(0,0,0,0.2)] dark:backdrop-blur-xl">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-lg font-semibold flex items-center gap-3 font-heading text-gray-900 dark:text-zinc-100">
                                <Target className="text-blue-500" size={22} strokeWidth={1.5} /> 90-Day Strategic Anchors
                            </h2>
                            <button className="text-blue-600 dark:text-blue-400 text-xs font-medium uppercase tracking-wider hover:text-blue-700 dark:hover:text-white flex items-center gap-2 transition-colors">
                                Launch Strategic Engine <ArrowRight size={14} strokeWidth={1.5} />
                            </button>
                        </div>
                        <div className="space-y-3">
                            {roadmap.map((milestone, i) => (
                                <div key={i} className="flex items-center gap-6 p-4 rounded-xl bg-gray-50 dark:bg-white/[0.02] border border-gray-200/40 dark:border-white/5 hover:bg-gray-100 dark:hover:bg-white/[0.04] transition-all group">
                                    <div className="min-w-[60px] text-[10px] font-medium text-gray-400 dark:text-zinc-700 uppercase tracking-tight">{milestone.date}</div>
                                    <div className="flex-1">
                                        <h4 className="font-medium text-gray-700 dark:text-zinc-300 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors text-sm">{milestone.title}</h4>
                                        <p className="text-[10px] text-gray-400 dark:text-zinc-700 font-medium uppercase mt-0.5">Status: {milestone.status}</p>
                                    </div>
                                    {milestone.status === "In Progress" ? (
                                        <div className="p-2 bg-amber-50 dark:bg-amber-500/10 rounded-full">
                                            <Clock size={14} strokeWidth={1.5} className="text-amber-500 dark:text-amber-400" />
                                        </div>
                                    ) : (
                                        <div className="p-2 bg-emerald-50 dark:bg-emerald-500/10 rounded-full">
                                            <CheckCircle2 size={14} strokeWidth={1.5} className="text-emerald-500 dark:text-emerald-400" />
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </section>

                </div>

                {/* Right Column: Authorization & Metrics */}
                <div className="space-y-8">

                    {/* Authorization Board */}
                    <section className="bg-white dark:bg-white/[0.04] p-6 rounded-2xl border border-gray-200/60 dark:border-white/[0.06] shadow-sm dark:shadow-[0_4px_24px_rgba(0,0,0,0.2)] dark:backdrop-blur-xl relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-6 opacity-5">
                            <ShieldCheck size={70} strokeWidth={1} />
                        </div>
                        <div className="flex items-center justify-between mb-6 relative z-10">
                            <h2 className="text-lg font-semibold flex items-center gap-2 font-heading text-gray-900 dark:text-zinc-100">
                                <ShieldCheck className="text-blue-500" size={22} strokeWidth={1.5} /> Authority Board
                            </h2>
                            <span className="px-2.5 py-1 bg-blue-50 dark:bg-blue-500/10 text-blue-700 dark:text-blue-400 text-[10px] font-medium rounded-full border border-blue-200/60 dark:border-blue-500/20 uppercase tracking-wider">
                                {authQueue.length} Pending
                            </span>
                        </div>
                        <div className="space-y-3 relative z-10">
                            {authQueue.map((req, i) => (
                                <div key={i} className="bg-gray-50 dark:bg-white/[0.03] backdrop-blur-sm p-5 rounded-xl border border-gray-200/40 dark:border-white/5 hover:bg-gray-100 dark:hover:bg-white/[0.05] transition-all cursor-pointer group">
                                    <div className="flex justify-between items-start mb-3">
                                        <span className="text-[10px] font-medium text-gray-400 dark:text-zinc-600 uppercase tracking-wider group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">@{req.agent}</span>
                                        <span className={`text-[9px] font-medium px-2 py-0.5 rounded-full uppercase tracking-tight border ${req.risk === 'High' ? 'bg-red-50 text-red-600 border-red-200/60 dark:bg-red-500/10 dark:text-red-400 dark:border-red-500/20' : 'bg-amber-50 text-amber-600 border-amber-200/60 dark:bg-amber-500/10 dark:text-amber-400 dark:border-amber-500/20'}`}>
                                            {req.risk} Risk
                                        </span>
                                    </div>
                                    <h4 className="font-medium text-sm mb-4 text-gray-700 dark:text-zinc-300 leading-relaxed">{req.action}</h4>
                                    <div className="flex gap-2">
                                        <button className="flex-1 py-2.5 bg-gradient-to-b from-blue-500 to-blue-600 text-white text-[10px] font-medium uppercase tracking-wider rounded-lg transition-all shadow-md shadow-blue-500/20 hover:shadow-lg hover:from-blue-600 hover:to-blue-700 active:scale-[0.98]">Authorize</button>
                                        <button className="px-4 py-2.5 bg-gray-100 dark:bg-white/5 hover:bg-gray-200 dark:hover:bg-white/10 text-[10px] font-medium uppercase tracking-wider rounded-lg transition-all text-gray-600 dark:text-zinc-500 border border-gray-200/60 dark:border-white/5">Review</button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* Quick Insights */}
                    <section className="bg-white dark:bg-white/[0.04] p-6 rounded-2xl border border-gray-200/60 dark:border-white/[0.06] shadow-sm dark:shadow-[0_4px_24px_rgba(0,0,0,0.2)] dark:backdrop-blur-xl overflow-hidden relative">
                        <div className="absolute top-0 right-0 p-6 opacity-[0.03]">
                            <TrendingUp size={80} strokeWidth={1} />
                        </div>
                        <h2 className="text-lg font-semibold mb-6 flex items-center gap-2 relative z-10 font-heading text-gray-900 dark:text-zinc-100">
                            <TrendingUp className="text-blue-500" size={22} strokeWidth={1.5} /> Strategic Signal Room
                        </h2>
                        <div className="space-y-3 relative z-10">
                            <div className="p-4 bg-emerald-50 dark:bg-emerald-500/5 border border-emerald-200/40 dark:border-emerald-500/10 rounded-xl group hover:bg-emerald-100 dark:hover:bg-emerald-500/10 transition-all cursor-pointer">
                                <p className="text-[10px] font-medium text-emerald-600 dark:text-emerald-400 uppercase tracking-wider mb-1.5">High Impact Opportunity</p>
                                <h5 className="font-medium text-gray-700 dark:text-zinc-300 text-sm">Switch to YouTube Shorts</h5>
                                <p className="text-xs text-gray-500 dark:text-zinc-500 mt-1.5">Expected ROI: <span className="text-emerald-600 dark:text-emerald-400 font-medium">+45% Reach</span></p>
                            </div>
                            <div className="p-4 bg-blue-50 dark:bg-blue-500/5 border border-blue-200/40 dark:border-blue-500/10 rounded-xl group hover:bg-blue-100 dark:hover:bg-blue-500/10 transition-all cursor-pointer">
                                <p className="text-[10px] font-medium text-blue-600 dark:text-blue-400 uppercase tracking-wider mb-1.5">Operations Signal</p>
                                <h5 className="font-medium text-gray-700 dark:text-zinc-300 text-sm">Automate Lead Scoring</h5>
                                <p className="text-xs text-gray-500 dark:text-zinc-500 mt-1.5">Efficiency Gain: <span className="text-blue-600 dark:text-blue-400 font-medium">2.7h daily</span></p>
                            </div>
                        </div>
                        <button className="w-full mt-4 py-2.5 border border-gray-200/60 dark:border-white/5 rounded-xl text-[10px] font-medium uppercase tracking-wider text-gray-400 dark:text-zinc-600 hover:bg-gray-50 dark:hover:bg-white/5 hover:text-gray-600 dark:hover:text-zinc-500 transition-all flex items-center justify-center gap-2">
                            Full Growth Dashboard <ArrowRight size={12} strokeWidth={1.5} />
                        </button>
                    </section>

                </div>

            </div>
        </div>
    );
};

export default ExecutiveDashboard;
