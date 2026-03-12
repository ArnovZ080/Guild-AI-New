import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    X, Eye, EyeOff, Shield, ExternalLink, Info, CheckCircle,
    AlertTriangle, BookOpen, Key, Link, Activity, Clock, Zap,
    ChevronRight, ChevronDown, HelpCircle, Lock
} from 'lucide-react';

const ConnectModal = ({ connector, onClose, onConnect, isConnecting }) => {
    const [apiKey, setApiKey] = useState('');
    const [showApiKey, setShowApiKey] = useState(false);
    const [additionalFields, setAdditionalFields] = useState({});
    const [activeTab, setActiveTab] = useState('overview');
    const [expandedSteps, setExpandedSteps] = useState({});
    const [showTooltip, setShowTooltip] = useState({});

    if (!connector) return null;

    const Icon = connector.icon;
    const instructions = connector.api_key_instructions || {};

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!apiKey.trim()) return;
        onConnect({
            connector_id: connector.id,
            api_key: apiKey,
            additional_config: additionalFields
        });
    };

    const toggleStep = (index) => {
        setExpandedSteps(prev => ({ ...prev, [index]: !prev[index] }));
    };

    const getComplexityColor = (complexity) => {
        switch (complexity) {
            case 'easy': return 'bg-green-100 text-green-800 border-green-300';
            case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
            case 'high': return 'bg-red-100 text-red-800 border-red-300';
            default: return 'bg-gray-100 text-gray-800 border-gray-300';
        }
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col shadow-2xl"
            >
                <div className={`${connector.color} text-white p-6`}>
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-4">
                            <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                                <Icon className="w-8 h-8 text-white" strokeWidth={1.5} />
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold">Connect {connector.name}</h2>
                                <p className="text-sm opacity-90 mt-1">{connector.category?.replace('_', ' ').toUpperCase()}</p>
                            </div>
                        </div>
                        <button onClick={onClose} className="text-white hover:bg-white/20 p-2 rounded-lg transition-colors"><X className="w-6 h-6" strokeWidth={1.5} /></button>
                    </div>
                    <div className="flex flex-wrap gap-3">
                        <div className={`px-3 py-1 rounded-full border text-sm ${getComplexityColor(connector.setup_complexity)} bg-white`}>
                            <span className="font-medium">Setup: {connector.setup_complexity || 'Medium'}</span>
                        </div>
                        <div className="px-3 py-1 bg-white/20 rounded-full text-sm flex items-center space-x-1">
                            <Clock className="w-4 h-4" strokeWidth={1.5} /><span>{connector.estimated_setup_time || '5m'}</span>
                        </div>
                    </div>
                </div>

                <div className="border-b border-gray-200 px-6 bg-gray-50 flex space-x-1">
                    {[
                        { id: 'overview', label: 'Overview', icon: Info },
                        { id: 'instructions', label: 'Setup Instructions', icon: BookOpen },
                        { id: 'security', label: 'Security', icon: Shield },
                        { id: 'transparency', label: 'Transparency', icon: Activity }
                    ].map(tab => {
                        const TabIcon = tab.icon;
                        return (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`flex items-center space-x-2 px-4 py-3 text-sm font-medium transition-colors border-b-2 ${activeTab === tab.id ? 'border-blue-500 text-blue-600 bg-white' : 'border-transparent text-gray-600 hover:text-gray-900 hover:bg-gray-100'}`}
                            >
                                <TabIcon className="w-4 h-4" strokeWidth={1.5} /><span>{tab.label}</span>
                            </button>
                        );
                    })}
                </div>

                <div className="flex-1 overflow-y-auto p-6">
                    <AnimatePresence mode="wait">
                        {activeTab === 'overview' && (
                            <motion.div key="overview" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} className="space-y-6">
                                <div>
                                    <h3 className="text-lg font-semibold text-gray-900 mb-3">What is {connector.name}?</h3>
                                    <p className="text-gray-700 leading-relaxed">{connector.description}</p>
                                </div>
                                {connector.use_cases && (
                                    <div>
                                        <h3 className="text-lg font-semibold text-gray-900 mb-3">What Agents Can Do</h3>
                                        <div className="space-y-2">
                                            {connector.use_cases.map((useCase, index) => (
                                                <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg border border-blue-100">
                                                    <CheckCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
                                                    <p className="text-gray-800 text-sm">{useCase}</p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </motion.div>
                        )}

                        {activeTab === 'instructions' && (
                            <motion.div key="instructions" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} className="space-y-6">
                                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                    <div className="flex items-start space-x-3">
                                        <BookOpen className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
                                        <div>
                                            <h3 className="font-semibold text-blue-900 mb-1">How to Connect</h3>
                                            <p className="text-sm text-blue-800">Follow these steps to obtain your API credentials.</p>
                                        </div>
                                    </div>
                                </div>
                                <div className="p-8 text-center text-zinc-500 bg-gray-50 rounded-lg border border-dashed border-gray-300">
                                    <BookOpen className="w-12 h-12 mx-auto mb-3 text-zinc-500" strokeWidth={1.5} />
                                    <p>Detailed instructions placeholder for {connector.name}</p>
                                    <a href={connector.documentation_url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline mt-2 inline-block">View Official Docs</a>
                                </div>
                            </motion.div>
                        )}

                        {activeTab === 'security' && (
                            <motion.div key="security" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} className="space-y-6">
                                <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                                    <div className="flex items-start space-x-4">
                                        <Shield className="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
                                        <div>
                                            <h3 className="text-lg font-semibold text-green-900 mb-2">How We Protect Your Data</h3>
                                            <p className="text-green-800 leading-relaxed">Your credentials are encrypted using industry-standard AES-256 encryption.</p>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        )}

                        {activeTab === 'transparency' && (
                            <motion.div key="transparency" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} className="space-y-6">
                                <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
                                    <div className="flex items-start space-x-4">
                                        <Activity className="w-6 h-6 text-purple-600 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
                                        <div>
                                            <h3 className="text-lg font-semibold text-purple-900 mb-2">Full Transparency</h3>
                                            <p className="text-purple-800 leading-relaxed">We believe in complete transparency. You will see every action taken by agents in the Activity Feed.</p>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                <div className="border-t border-gray-200 p-6 bg-gray-50">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center space-x-2">
                                <Key className="w-4 h-4" strokeWidth={1.5} /><span>API Key / Token</span>
                            </label>
                            <div className="relative">
                                <input
                                    type={showApiKey ? 'text' : 'password'}
                                    value={apiKey}
                                    onChange={(e) => setApiKey(e.target.value)}
                                    placeholder={`Enter your ${connector.name} API key`}
                                    className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 pr-10"
                                    required
                                />
                                <button type="button" onClick={() => setShowApiKey(!showApiKey)} className="absolute right-3 top-1/2 transform -translate-y-1/2 text-zinc-500 hover:text-gray-600">
                                    {showApiKey ? <EyeOff className="w-4 h-4" strokeWidth={1.5} /> : <Eye className="w-4 h-4" strokeWidth={1.5} />}
                                </button>
                            </div>
                        </div>
                        <div className="bg-green-50 border border-green-200 rounded-lg p-3 flex items-start space-x-2">
                            <Shield className="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
                            <p className="text-xs text-green-800">Your credentials are encrypted with AES-256 and stored securely.</p>
                        </div>
                        <div className="flex justify-end space-x-3">
                            <button type="button" onClick={onClose} className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors font-medium" disabled={isConnecting}>Cancel</button>
                            <button type="submit" disabled={!apiKey.trim() || isConnecting} className="px-6 py-2 bg-[#1a6fff] text-white rounded-lg hover:bg-[#4d8fff] transition-colors flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed font-medium">
                                {isConnecting ? <span>Connecting...</span> : <span>Connect {connector.name}</span>}
                            </button>
                        </div>
                    </form>
                </div>
            </motion.div>
        </div>
    );
};

export default ConnectModal;
