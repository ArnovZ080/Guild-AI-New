import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, TrendingUp, Calendar, Check, X, Lightbulb, BarChart3, Clock, Zap } from 'lucide-react';

const AdaptiveInsights = () => {
    const [preferences, setPreferences] = useState([]);
    const [patterns, setPatterns] = useState([]);
    const [performance, setPerformance] = useState({});
    const [activeTab, setActiveTab] = useState('preferences');

    useEffect(() => {
        // In production: fetch from /api/learning/dashboard
        const mockData = {
            preferences: [
                { id: '1', rule: 'No meetings on Tuesdays', rule_key: 'no_meetings_tuesday', category: 'scheduling', confidence: 'confirmed', signal_count: 8 },
                { id: '2', rule: 'Prefer finance review on Mondays', rule_key: 'finance_monday', category: 'finance', confidence: 'likely', signal_count: 5 },
                { id: '3', rule: 'Auto-generate weekly report on Fridays at 9:00', rule_key: 'weekly_report_friday', category: 'general', confidence: 'suggested', signal_count: 3 },
            ],
            patterns: [
                { id: '1', insight: 'LinkedIn posts at 10am get 2.3x more engagement', recommendation: 'Schedule LinkedIn content between 9-11am', confidence_score: 0.85, sample_size: 24 },
                { id: '2', insight: 'Follow-up emails within 2hrs close 40% more deals', recommendation: 'Auto-trigger CRM follow-ups within 2 hours', confidence_score: 0.72, sample_size: 15 },
                { id: '3', insight: 'Tuesday blog posts outperform by 1.8x', recommendation: 'Prioritize blog publishing on Tuesdays', confidence_score: 0.68, sample_size: 12 },
            ],
            performance: { total_actions: 156, avg_score: 3.8, excellent_rate: 0.32, failure_rate: 0.05 }
        };
        setPreferences(mockData.preferences);
        setPatterns(mockData.patterns);
        setPerformance(mockData.performance);
    }, []);

    const confidenceStyles = {
        confirmed: { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/30', icon: '🟢' },
        likely: { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/30', icon: '🟡' },
        suggested: { bg: 'bg-blue-500/10', text: 'text-blue-400', border: 'border-blue-500/30', icon: '🔵' },
    };

    const tabs = [
        { id: 'preferences', label: 'Your Preferences', icon: Calendar },
        { id: 'optimizations', label: 'Business Insights', icon: TrendingUp },
        { id: 'performance', label: 'Performance', icon: BarChart3 },
    ];

    return (
        <div className="p-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
            <div className="max-w-5xl mx-auto">
                {/* Header */}
                <header className="mb-10">
                    <div className="flex items-center gap-3 mb-2">
                        <Brain className="text-violet-400 w-8 h-8" strokeWidth={1.5} />
                        <h1 className="text-3xl font-bold text-white">
                            Engine Intelligence
                        </h1>
                    </div>
                    <p className="text-zinc-600">Your AI is learning. Here's what it has discovered about you and your business.</p>
                </header>

                {/* Tabs */}
                <div className="flex gap-2 mb-8 border-b border-slate-800 pb-1">
                    {tabs.map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center gap-2 px-5 py-3 rounded-t-lg text-sm font-medium transition-all
                ${activeTab === tab.id
                                    ? 'glass-panel text-zinc-100 border-b-2 border-violet-500'
                                    : 'text-zinc-500 hover:text-zinc-600'}`}
                        >
                            <tab.icon size={16} strokeWidth={1.5} />
                            {tab.label}
                        </button>
                    ))}
                </div>

                {/* Preferences Tab */}
                {activeTab === 'preferences' && (
                    <div className="space-y-4">
                        <AnimatePresence>
                            {preferences.map((pref, i) => {
                                const style = confidenceStyles[pref.confidence] || confidenceStyles.suggested;
                                return (
                                    <motion.div
                                        key={pref.id}
                                        initial={{ opacity: 0, y: 10 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: i * 0.1 }}
                                        className={`p-5 rounded-2xl border ${style.border} ${style.bg} flex items-center justify-between`}
                                    >
                                        <div className="flex items-center gap-4">
                                            <span className="text-2xl">{style.icon}</span>
                                            <div>
                                                <h3 className="text-lg font-semibold text-white">{pref.rule}</h3>
                                                <p className="text-sm text-zinc-600 mt-1">
                                                    <span className="capitalize">{pref.category}</span> • Observed {pref.signal_count}x • {pref.confidence}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="flex gap-2">
                                            {pref.confidence !== 'confirmed' && (
                                                <button className="p-2 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-400 transition-colors" title="Confirm">
                                                    <Check size={18} strokeWidth={1.5} />
                                                </button>
                                            )}
                                            <button className="p-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 transition-colors" title="Dismiss">
                                                <X size={18} strokeWidth={1.5} />
                                            </button>
                                        </div>
                                    </motion.div>
                                );
                            })}
                        </AnimatePresence>
                    </div>
                )}

                {/* Optimizations Tab */}
                {activeTab === 'optimizations' && (
                    <div className="space-y-4">
                        {patterns.map((pattern, i) => (
                            <motion.div
                                key={pattern.id}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: i * 0.1 }}
                                className="p-6 rounded-2xl bg-slate-900 border border-slate-800"
                            >
                                <div className="flex items-start gap-4">
                                    <div className="p-3 rounded-xl bg-violet-500/10">
                                        <Lightbulb className="text-violet-400" strokeWidth={1.5} />
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="text-lg font-semibold">{pattern.insight}</h3>
                                        <div className="mt-3 p-3 rounded-lg bg-slate-950 border border-slate-800 flex items-center gap-2">
                                            <Zap size={14} className="text-amber-400" strokeWidth={1.5} />
                                            <span className="text-sm text-amber-300">{pattern.recommendation}</span>
                                        </div>
                                        <div className="mt-3 flex gap-4 text-xs text-zinc-500">
                                            <span>Confidence: {Math.round(pattern.confidence_score * 100)}%</span>
                                            <span>•</span>
                                            <span>Based on {pattern.sample_size} data points</span>
                                        </div>
                                    </div>
                                    {/* Confidence Bar */}
                                    <div className="w-16">
                                        <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                                            <div
                                                className="h-full bg-blue-500 rounded-full transition-all"
                                                style={{ width: `${pattern.confidence_score * 100}%` }}
                                            />
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                )}

                {/* Performance Tab */}
                {activeTab === 'performance' && (
                    <div className="grid grid-cols-4 gap-4">
                        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center">
                            <p className="text-4xl font-bold text-white">{performance.total_actions}</p>
                            <p className="text-sm text-zinc-600 mt-2">Total Actions</p>
                        </motion.div>
                        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center">
                            <p className="text-4xl font-bold text-emerald-400">{performance.avg_score?.toFixed(1)}/5</p>
                            <p className="text-sm text-zinc-600 mt-2">Avg Score</p>
                        </motion.div>
                        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2 }} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center">
                            <p className="text-4xl font-bold text-violet-400">{Math.round((performance.excellent_rate || 0) * 100)}%</p>
                            <p className="text-sm text-zinc-600 mt-2">Excellence Rate</p>
                        </motion.div>
                        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.3 }} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center">
                            <p className="text-4xl font-bold text-red-400">{Math.round((performance.failure_rate || 0) * 100)}%</p>
                            <p className="text-sm text-zinc-600 mt-2">Failure Rate</p>
                        </motion.div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdaptiveInsights;
