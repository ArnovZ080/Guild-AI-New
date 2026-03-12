import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Search, Filter, Plus, CheckCircle, AlertCircle,
    ExternalLink, Settings, Info, Shield, Zap, Database, Globe, DollarSign
} from 'lucide-react';
import { integrationConfigs, integrationCategories } from './integrationConfigs';
import IntegrationModal from './IntegrationModal';

const IntegrationsHub = () => {
    const [activeTab, setActiveTab] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [integrations, setIntegrations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedIntegration, setSelectedIntegration] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        fetchIntegrations();
    }, []);

    const fetchIntegrations = async () => {
        setLoading(true);
        try {
            // In production, this would be a real API call: GET /api/integrations
            // For now, we simulate with metadata from configs and connection status
            const response = await fetch('http://localhost:8001/integrations/');
            const apiData = await response.json();

            // Merge API data with frontend configs
            const mergedData = apiData.map(item => ({
                ...item,
                ...(integrationConfigs[item.platform] || {})
            }));

            setIntegrations(mergedData);
        } catch (error) {
            console.error('Error fetching integrations:', error);
            // Fallback for demo
            const demoData = Object.values(integrationConfigs).map(config => ({
                ...config,
                is_connected: Math.random() > 0.7
            }));
            setIntegrations(demoData);
        } finally {
            setLoading(false);
        }
    };

    const filteredIntegrations = integrations.filter(item => {
        const matchesTab = activeTab === 'all' || item.category === activeTab;
        const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.description.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesTab && matchesSearch;
    });

    const handleOpenModal = (integration) => {
        setSelectedIntegration(integration);
        setIsModalOpen(true);
    };

    return (
        <div className="flex flex-col h-full bg-[#0a0a0b] text-white p-8">
            {/* Header */}
            <div className="flex justify-between items-end mb-8">
                <div>
                    <h1 className="text-3xl font-bold mb-2 text-white">
                        Integration Hub
                    </h1>
                    <p className="text-zinc-500 max-w-2xl">
                        Give your AI workforce "hands" by connecting your favorite external tools.
                        All connections are encrypted and under your direct control.
                    </p>
                </div>
                <div className="flex gap-4">
                    <div className="flex items-center bg-zinc-950/40 border border-white/5 rounded-lg px-3 py-2">
                        <Shield className="w-4 h-4 text-emerald-400 mr-2" strokeWidth={1.5} />
                        <span className="text-xs font-medium uppercase tracking-wider text-zinc-500">Military-Grade Encryption</span>
                    </div>
                </div>
            </div>

            {/* Toolbar */}
            <div className="flex flex-col md:flex-row gap-4 mb-8">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500 w-4 h-4" strokeWidth={1.5} />
                    <input
                        type="text"
                        placeholder="Search connectors..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full bg-zinc-950/40 border border-white/5 rounded-xl pl-10 pr-4 py-3 text-sm focus:outline-none focus:border-white/5 transition-all"
                    />
                </div>
                <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0">
                    {integrationCategories.map(cat => (
                        <button
                            key={cat.id}
                            onClick={() => setActiveTab(cat.id)}
                            className={`px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all flex items-center gap-2 ${activeTab === cat.id
                                ? 'bg-white text-black shadow-[0_0_20px_rgba(255,255,255,0.1)]'
                                : 'bg-zinc-950/40 text-zinc-500 border border-white/5 hover:border-white/5'
                                }`}
                        >
                            {cat.icon && <cat.icon className="w-4 h-4" strokeWidth={1.5} />}
                            {cat.name}
                        </button>
                    ))}
                </div>
            </div>

            {/* Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 overflow-y-auto pr-2 custom-scrollbar">
                <AnimatePresence mode="popLayout">
                    {filteredIntegrations.map((item) => (
                        <motion.div
                            layout
                            key={item.id}
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            whileHover={{ y: -4 }}
                            className="bg-zinc-950/40 border border-white/5 rounded-2xl p-6 flex flex-col group cursor-pointer hover:border-white/5 transition-all hover:shadow-[0_8px_30px_rgb(0,0,0,0.12)]"
                            onClick={() => handleOpenModal(item)}
                        >
                            <div className="flex justify-between items-start mb-4">
                                <div className={`w-12 h-12 rounded-xl ${item.color || 'bg-gray-800'} flex items-center justify-center p-2.5`}>
                                    {item.icon ? <item.icon className="text-white" strokeWidth={1.5} /> : <Database className="text-white" strokeWidth={1.5} />}
                                </div>
                                {item.is_connected ? (
                                    <div className="flex items-center gap-1.5 bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border border-emerald-500/20">
                                        <CheckCircle className="w-3 h-3" strokeWidth={1.5} />
                                        Connected
                                    </div>
                                ) : (
                                    <div className="bg-white/5 text-zinc-500 px-2 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border border-white/5 group-hover:bg-white group-hover:text-black transition-colors">
                                        Disconnected
                                    </div>
                                )}
                            </div>

                            <h3 className="text-lg font-bold text-white mb-2">{item.name}</h3>
                            <p className="text-zinc-500 text-sm line-clamp-2 mb-6 flex-grow">
                                {item.description}
                            </p>

                            <div className="flex items-center justify-between pt-4 border-t border-white/5 italic text-zinc-500 text-[11px]">
                                <div className="flex gap-2">
                                    {item.capabilities?.slice(0, 3).map(cap => (
                                        <span key={cap}>• {cap}</span>
                                    ))}
                                </div>
                                <Zap className={`w-3 h-3 ${item.is_connected ? 'text-amber-400' : 'text-gray-700'}`} strokeWidth={1.5} />
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>

            {isModalOpen && (
                <IntegrationModal
                    integration={selectedIntegration}
                    onClose={() => setIsModalOpen(false)}
                    onSuccess={fetchIntegrations}
                />
            )}
        </div>
    );
};

export default IntegrationsHub;
