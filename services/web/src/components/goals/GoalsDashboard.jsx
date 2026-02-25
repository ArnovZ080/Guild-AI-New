import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    Target,
    TrendingUp,
    CheckCircle2,
    Plus,
    MoreVertical,
    Zap,
    BarChart3,
    Calendar,
    ArrowUpRight
} from 'lucide-react';

const GoalsDashboard = () => {
    const [goals, setGoals] = useState([
        {
            id: 1,
            title: "Increase Q1 Revenue",
            metric: "Revenue",
            current: 45000,
            target: 60000,
            deadline: "2024-03-31",
            status: "on_track",
            milestones: [
                { id: "m1", title: "Launch new product line", completed: true },
                { id: "m2", title: "Optimize ad spend", completed: false },
                { id: "m3", title: "Close 5 enterprise deals", completed: false }
            ]
        },
        {
            id: 2,
            title: "Expand Customer Base",
            metric: "Users",
            current: 1200,
            target: 2000,
            deadline: "2024-06-30",
            status: "at_risk",
            milestones: [
                { id: "m4", title: "Referral program v2", completed: true },
                { id: "m5", title: "Content marketing push", completed: true },
                { id: "m6", title: "Partnership outreach", completed: false }
            ]
        }
    ]);

    const calculateProgress = (current, target) => Math.min(Math.round((current / target) * 100), 100);

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-8">
            <header className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Q1 Goals & OKRs</h1>
                    <p className="text-slate-500 mt-1">Strategic objectives and key results tracker.</p>
                </div>
                <button className="bg-indigo-600 text-white px-5 py-2.5 rounded-xl font-bold text-sm shadow-md hover:bg-indigo-700 transition-all flex items-center gap-2">
                    <Plus size={18} /> New Goal
                </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {goals.map(goal => (
                    <motion.div
                        key={goal.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200 hover:shadow-md transition-shadow"
                    >
                        <div className="flex justify-between items-start mb-6">
                            <div className="flex items-center gap-3">
                                <div className={`p-3 rounded-xl ${goal.status === 'on_track' ? 'bg-emerald-100 text-emerald-600' : 'bg-amber-100 text-amber-600'}`}>
                                    <Target size={24} />
                                </div>
                                <div>
                                    <h3 className="font-bold text-lg text-slate-900">{goal.title}</h3>
                                    <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{goal.metric}</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className={`px-2 py-0.5 rounded text-xs font-bold uppercase ${goal.status === 'on_track' ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'}`}>
                                    {goal.status.replace('_', ' ')}
                                </span>
                                <button className="text-slate-400 hover:text-slate-600"><MoreVertical size={16} /></button>
                            </div>
                        </div>

                        <div className="space-y-2 mb-6">
                            <div className="flex justify-between text-sm font-bold text-slate-600">
                                <span>{calculateProgress(goal.current, goal.target)}% Complete</span>
                                <span>{goal.current.toLocaleString()} / {goal.target.toLocaleString()}</span>
                            </div>
                            <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                                <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${calculateProgress(goal.current, goal.target)}%` }}
                                    className={`h-full rounded-full ${goal.status === 'on_track' ? 'bg-emerald-500' : 'bg-amber-500'}`}
                                />
                            </div>
                        </div>

                        <div className="space-y-3">
                            <h4 className="text-xs font-bold text-slate-400 uppercase mb-2">Key Milestones</h4>
                            {goal.milestones.map(ms => (
                                <div key={ms.id} className="flex items-center gap-3 p-2 hover:bg-slate-50 rounded-lg transition-colors cursor-pointer group">
                                    <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${ms.completed ? 'bg-indigo-600 border-indigo-600' : 'border-slate-300'}`}>
                                        {ms.completed && <CheckCircle2 size={12} className="text-white" />}
                                    </div>
                                    <span className={`text-sm font-medium ${ms.completed ? 'text-slate-400 line-through' : 'text-slate-700'}`}>
                                        {ms.title}
                                    </span>
                                </div>
                            ))}
                        </div>

                        <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                            <div className="flex items-center gap-2 text-xs font-bold text-slate-500">
                                <Calendar size={14} /> Deadline: {goal.deadline}
                            </div>
                            <button className="text-indigo-600 text-sm font-bold hover:underline flex items-center gap-1">
                                View Details <ArrowUpRight size={14} />
                            </button>
                        </div>
                    </motion.div>
                ))}

                {/* AI Insights Card */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="bg-indigo-900 rounded-2xl p-6 shadow-xl text-white relative overflow-hidden"
                >
                    <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500 rounded-full blur-3xl opacity-20 -mr-10 -mt-10" />
                    <div className="relative z-10">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-3 bg-white/10 rounded-xl backdrop-blur-sm">
                                <Zap size={24} className="text-amber-400" />
                            </div>
                            <h3 className="font-bold text-lg">AI Strategic Insights</h3>
                        </div>
                        <div className="space-y-4">
                            <div className="bg-white/10 p-4 rounded-xl border border-white/5 backdrop-blur-sm hover:bg-white/15 transition-colors cursor-pointer">
                                <h5 className="font-bold text-sm mb-1 text-indigo-100">Revenue Acceleration</h5>
                                <p className="text-xs text-indigo-200 leading-relaxed">Based on current trends, launching the referral program early could boost Q1 revenue by an additional 12%.</p>
                            </div>
                            <div className="bg-white/10 p-4 rounded-xl border border-white/5 backdrop-blur-sm hover:bg-white/15 transition-colors cursor-pointer">
                                <h5 className="font-bold text-sm mb-1 text-indigo-100">Risk Alert</h5>
                                <p className="text-xs text-indigo-200 leading-relaxed">Customer acquisition cost (CAC) has increased by 15% this week. Suggest reviewing "Optimize ad spend" milestone.</p>
                            </div>
                        </div>
                        <button className="w-full mt-6 py-3 bg-white text-indigo-900 font-bold rounded-xl hover:bg-indigo-50 transition-colors shadow-lg">
                            Generate New Strategy
                        </button>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default GoalsDashboard;
