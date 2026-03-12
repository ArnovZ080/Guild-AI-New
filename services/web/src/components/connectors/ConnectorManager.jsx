import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Settings, Search, Filter, CheckCircle, AlertCircle,
    ExternalLink, Key, Shield, Zap, Database, Globe,
    DollarSign, Users, Calendar, FileText, Camera,
    BarChart, Wrench, Plus, X, Video,
    Monitor, MousePointer
} from 'lucide-react';
import ConnectModal from './ConnectModal';

const ConnectorManager = () => {
    const [activeTab, setActiveTab] = useState('available');
    const [searchTerm, setSearchTerm] = useState('');
    const [filterCategory, setFilterCategory] = useState('all');
    const [selectedConnector, setSelectedConnector] = useState(null);
    const [showConnectModal, setShowConnectModal] = useState(false);
    const [isRecording, setIsRecording] = useState(false);
    const [recordingSteps, setRecordingSteps] = useState([]);

    // Mock available connectors (simplified list)
    const availableConnectors = [
        { id: 'asana', name: 'Asana', category: 'project_management', status: 'active', capabilities: ['tasks', 'projects'], description: 'Coordinate tasks and projects', icon: Calendar, color: 'bg-purple-500', documentation_url: 'https://developers.asana.com' },
        { id: 'stripe', name: 'Stripe', category: 'payments', status: 'active', capabilities: ['payments', 'customers'], description: 'Payment processing infrastructure', icon: DollarSign, color: 'bg-[#1a6fff]', documentation_url: 'https://stripe.com/docs' },
        { id: 'hubspot', name: 'HubSpot', category: 'crm', status: 'active', capabilities: ['contacts', 'companies'], description: 'CRM and marketing automation', icon: Database, color: 'bg-orange-500', documentation_url: 'https://developers.hubspot.com' },
        { id: 'gmail', name: 'Gmail', category: 'communication', status: 'active', capabilities: ['send_email', 'labels'], description: 'Send emails and manage inbox', icon: Users, color: 'bg-red-500', documentation_url: 'https://developers.google.com/gmail' },
        { id: 'slack', name: 'Slack', category: 'communication', status: 'active', capabilities: ['messages', 'channels'], description: 'Team communication', icon: Users, color: 'bg-purple-500', documentation_url: 'https://api.slack.com' }
    ];

    const connectedServices = [
        { id: 'stripe', name: 'Stripe', category: 'payments', connected_at: new Date().toISOString(), status: 'active', icon: DollarSign, color: 'bg-[#1a6fff]' }
    ];

    const categories = [
        { id: 'all', name: 'All Connectors', icon: Settings },
        { id: 'project_management', name: 'Project Management', icon: Calendar },
        { id: 'payments', name: 'Payments', icon: DollarSign },
        { id: 'crm', name: 'CRM', icon: Database },
        { id: 'communication', name: 'Communication', icon: Users }
    ];

    const filteredConnectors = availableConnectors.filter(c =>
        (filterCategory === 'all' || c.category === filterCategory) &&
        (c.name.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    const startScreenRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getDisplayMedia({ video: { mediaSource: 'screen' } });
            setIsRecording(true);
            // Mock recording simple steps
            setRecordingSteps([{ type: 'start', ts: Date.now() }]);
            stream.getVideoTracks()[0].onended = () => {
                setIsRecording(false);
                alert('Recording finished! (Mock)');
            };
        } catch (e) {
            console.error("Recording failed", e);
        }
    };

    return (
        <div className="p-6 max-w-7xl mx-auto">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Connector Manager</h1>
                <p className="text-gray-600">Connect and manage external integrations.</p>
            </div>

            <div className="flex space-x-1 mb-6 bg-gray-100 p-1 rounded-lg w-fit">
                {[{ id: 'available', label: 'Available' }, { id: 'connected', label: 'Connected' }, { id: 'create', label: 'Create Custom' }].map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${activeTab === tab.id ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600 hover:text-gray-900'}`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {activeTab === 'available' && (
                <>
                    <div className="flex gap-4 mb-6">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-zinc-500 w-4 h-4" strokeWidth={1.5} />
                            <input
                                type="text"
                                placeholder="Search..."
                                className="w-full pl-10 pr-4 py-2 border rounded-lg"
                                value={searchTerm}
                                onChange={e => setSearchTerm(e.target.value)}
                            />
                        </div>
                        <div className="relative">
                            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-zinc-500 w-4 h-4" strokeWidth={1.5} />
                            <select
                                className="pl-10 pr-8 py-2 border rounded-lg appearance-none bg-white"
                                value={filterCategory}
                                onChange={e => setFilterCategory(e.target.value)}
                            >
                                {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                            </select>
                        </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredConnectors.map(c => {
                            const Icon = c.icon;
                            return (
                                <motion.div key={c.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-white rounded-lg shadow p-6 border hover:shadow-lg transition-shadow">
                                    <div className="flex justify-between mb-4">
                                        <div className={`p-3 rounded-lg ${c.color}`}><Icon className="w-6 h-6 text-white" strokeWidth={1.5} /></div>
                                        <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full h-fit flex items-center gap-1"><CheckCircle size={10} strokeWidth={1.5} /> Active</span>
                                    </div>
                                    <h3 className="font-bold text-lg">{c.name}</h3>
                                    <p className="text-sm text-gray-600 mb-4">{c.description}</p>
                                    <button
                                        onClick={() => { setSelectedConnector(c); setShowConnectModal(true); }}
                                        className="w-full bg-[#1a6fff] text-white py-2 rounded-lg hover:bg-[#4d8fff] transition-colors"
                                    >
                                        Connect
                                    </button>
                                </motion.div>
                            );
                        })}
                    </div>
                </>
            )}

            {activeTab === 'connected' && (
                <div className="space-y-4">
                    {connectedServices.map(s => {
                        const Icon = s.icon;
                        return (
                            <div key={s.id} className="bg-white p-6 rounded-lg shadow border flex justify-between items-center">
                                <div className="flex items-center gap-4">
                                    <div className={`p-3 rounded-lg ${s.color}`}><Icon className="w-6 h-6 text-white" strokeWidth={1.5} /></div>
                                    <div>
                                        <h3 className="font-bold">{s.name}</h3>
                                        <p className="text-sm text-zinc-500">Connected on {new Date(s.connected_at).toLocaleDateString()}</p>
                                    </div>
                                </div>
                                <button className="text-red-500 hover:bg-red-50 px-3 py-1 rounded-lg">Disconnect</button>
                            </div>
                        );
                    })}
                </div>
            )}

            {activeTab === 'create' && (
                <div className="bg-white rounded-lg shadow p-8 text-center">
                    <Video className="w-12 h-12 text-purple-600 mx-auto mb-4" strokeWidth={1.5} />
                    <h2 className="text-2xl font-bold mb-2">Create Custom Connection</h2>
                    <p className="text-gray-600 mb-6">Record your screen to teach an agent how to use any website or tool.</p>
                    <button
                        onClick={startScreenRecording}
                        disabled={isRecording}
                        className={`px-6 py-3 rounded-lg font-bold text-white flex items-center gap-2 mx-auto ${isRecording ? 'bg-red-500 animate-pulse' : 'bg-[#1a6fff] hover:bg-[#4d8fff]'}`}
                    >
                        {isRecording ? <><Monitor strokeWidth={1.5} /> Recording...</> : <><Video strokeWidth={1.5} /> Start Recording</>}
                    </button>
                </div>
            )}

            <AnimatePresence>
                {showConnectModal && selectedConnector && (
                    <ConnectModal
                        connector={selectedConnector}
                        onClose={() => setShowConnectModal(false)}
                        onConnect={(data) => {
                            console.log("Connected:", data);
                            setShowConnectModal(false);
                        }}
                    />
                )}
            </AnimatePresence>
        </div>
    );
};

export default ConnectorManager;
