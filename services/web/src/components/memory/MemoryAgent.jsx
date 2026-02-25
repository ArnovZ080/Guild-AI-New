import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Brain, Database, Search, Plus, Trash2, Edit, Save, X,
    Clock, User, Bot, MessageSquare, FileText, Tag, Star,
    TrendingUp, TrendingDown, Filter, Download, Upload,
    Lightbulb, Target, Zap, CheckCircle, AlertCircle
} from 'lucide-react';

const MemoryAgent = () => {
    const [memories, setMemories] = useState([
        {
            id: 1,
            type: 'preference',
            content: "Marketing team prefers 'friendly but professional' tone for all external comms.",
            confidence: 0.95,
            source: "User Feedback",
            timestamp: new Date().toISOString()
        },
        {
            id: 2,
            type: 'fact',
            content: "Q1 Revenue Target is $150,000.",
            confidence: 1.0,
            source: "Strategic Plan Document",
            timestamp: new Date().toISOString()
        },
        {
            id: 3,
            type: 'insight',
            content: "Customer engagement peaks on Tuesdays at 10 AM EST.",
            confidence: 0.85,
            source: "Analytics Agent",
            timestamp: new Date().toISOString()
        }
    ]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterType, setFilterType] = useState('all');

    const filteredMemories = memories.filter(m =>
        (filterType === 'all' || m.type === filterType) &&
        (m.content.toLowerCase().includes(searchTerm.toLowerCase()) || m.source.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    return (
        <div className="p-6 max-w-7xl mx-auto">
            <div className="mb-8 flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
                        <Brain className="w-8 h-8 text-indigo-600" />
                        Organizational Memory
                    </h1>
                    <p className="text-gray-600">The collective intelligence and context of your AI workforce.</p>
                </div>
                <div className="flex gap-2">
                    <button className="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-50 flex items-center gap-2">
                        <Upload size={18} /> Import
                    </button>
                    <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 flex items-center gap-2">
                        <Plus size={18} /> Add Memory
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                {/* Stats Column */}
                <div className="space-y-4">
                    <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
                        <div className="text-sm font-bold text-gray-500 uppercase mb-2">Total Memories</div>
                        <div className="text-3xl font-bold text-indigo-900">{memories.length}</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
                        <div className="text-sm font-bold text-gray-500 uppercase mb-2">Graph Connections</div>
                        <div className="text-3xl font-bold text-purple-900">42</div>
                    </div>
                    <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
                        <div className="text-sm font-bold text-gray-500 uppercase mb-2">Knowledge Gaps</div>
                        <div className="text-3xl font-bold text-amber-600">3</div>
                        <p className="text-xs text-amber-600 mt-1">Detected in "Competitor Analysis"</p>
                    </div>
                </div>

                {/* Main Content */}
                <div className="lg:col-span-3 space-y-6">
                    {/* Search Bar */}
                    <div className="flex gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                            <input
                                type="text"
                                placeholder="Search memories..."
                                className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                                value={searchTerm}
                                onChange={e => setSearchTerm(e.target.value)}
                            />
                        </div>
                        <select
                            className="pl-4 pr-8 py-3 border border-gray-200 rounded-xl bg-white shadow-sm outline-none"
                            value={filterType}
                            onChange={e => setFilterType(e.target.value)}
                        >
                            <option value="all">All Types</option>
                            <option value="fact">Facts</option>
                            <option value="preference">Preferences</option>
                            <option value="insight">Insights</option>
                        </select>
                    </div>

                    {/* Memory List */}
                    <div className="space-y-4">
                        <AnimatePresence>
                            {filteredMemories.map(m => (
                                <motion.div
                                    key={m.id}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, scale: 0.95 }}
                                    className="bg-white p-5 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow group"
                                >
                                    <div className="flex justify-between items-start mb-2">
                                        <div className="flex items-center gap-2">
                                            <span className={`px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider ${m.type === 'fact' ? 'bg-blue-100 text-blue-700' :
                                                    m.type === 'preference' ? 'bg-pink-100 text-pink-700' :
                                                        'bg-purple-100 text-purple-700'
                                                }`}>
                                                {m.type}
                                            </span>
                                            <span className="text-xs text-gray-400 flex items-center gap-1">
                                                <Clock size={12} /> {new Date(m.timestamp).toLocaleDateString()}
                                            </span>
                                        </div>
                                        <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button className="p-1 hover:bg-gray-100 rounded text-gray-500"><Edit size={16} /></button>
                                        </div>
                                    </div>
                                    <p className="text-gray-800 text-lg font-medium leading-relaxed mb-3">
                                        "{m.content}"
                                    </p>
                                    <div className="flex items-center justify-between text-sm">
                                        <div className="flex items-center gap-2 text-gray-500">
                                            <Database size={14} /> Source: <span className="font-semibold text-gray-700">{m.source}</span>
                                        </div>
                                        <div className="flex items-center gap-1 text-emerald-600 font-bold">
                                            <CheckCircle size={14} /> {(m.confidence * 100).toFixed(0)}% Confidence
                                        </div>
                                    </div>
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MemoryAgent;
