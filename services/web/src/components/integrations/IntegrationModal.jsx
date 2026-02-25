import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    X, Shield, Info, ExternalLink, Key, CheckCircle,
    AlertTriangle, Lock, Eye, EyeOff, Loader2
} from 'lucide-react';

const IntegrationModal = ({ integration, onClose, onSuccess }) => {
    const [activeTab, setActiveTab] = useState('overview');
    const [credentials, setCredentials] = useState({});
    const [showKey, setShowKey] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

    if (!integration) return null;

    const handleInputChange = (field, value) => {
        setCredentials(prev => ({ ...prev, [field]: value }));
    };

    const handleConnect = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await fetch('http://localhost:8001/integrations/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    platform: integration.id,
                    credentials: credentials
                })
            });

            const data = await response.json();
            if (response.ok) {
                setSuccess(true);
                setTimeout(() => {
                    onSuccess();
                    onClose();
                }, 1500);
            } else {
                setError(data.detail || 'Failed to connect. Please check your credentials.');
            }
        } catch (err) {
            setError('Connection failed. Is the backend server running?');
        } finally {
            setLoading(false);
        }
    };

    const handleOAuth = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await fetch(`http://localhost:8001/oauth/authorize/${integration.id}`);
            const data = await response.json();

            if (data.auth_url) {
                // Open OAuth flow in new window
                const popup = window.open(
                    data.auth_url,
                    'oauth',
                    'width=600,height=700,scrollbars=yes,resizable=yes'
                );

                // Listen for OAuth completion
                const checkClosed = setInterval(() => {
                    if (popup.closed) {
                        clearInterval(checkClosed);
                        setLoading(false);
                        onSuccess();
                        onClose();
                    }
                }, 1000);
            } else {
                setError('Failed to start OAuth flow.');
                setLoading(false);
            }
        } catch (err) {
            setError('OAuth initiation failed.');
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
            <motion.div
                initial={{ opacity: 0, scale: 0.9, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                className="bg-[#161618] border border-white/10 rounded-3xl w-full max-w-2xl overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)]"
            >
                {/* Modal Header */}
                <div className="p-6 border-b border-white/5 flex justify-between items-center">
                    <div className="flex items-center gap-4">
                        <div className={`w-10 h-10 rounded-xl ${integration.color} flex items-center justify-center`}>
                            {integration.icon && <integration.icon className="w-6 h-6 text-white" />}
                        </div>
                        <div>
                            <h2 className="text-xl font-bold text-white">{integration.name}</h2>
                            <p className="text-xs text-gray-500 uppercase tracking-widest">{integration.category}</p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-white/5 rounded-full transition-colors text-gray-400"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex border-b border-white/5 px-6">
                    {['overview', 'setup', 'security'].map(tab => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`px-4 py-4 text-sm font-medium transition-all relative ${activeTab === tab ? 'text-white' : 'text-gray-500 hover:text-gray-300'
                                }`}
                        >
                            {tab.charAt(0).toUpperCase() + tab.slice(1)}
                            {activeTab === tab && (
                                <motion.div
                                    layoutId="tab-underline"
                                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-white"
                                />
                            )}
                        </button>
                    ))}
                </div>

                {/* Content Area */}
                <div className="p-8 max-h-[60vh] overflow-y-auto">
                    {activeTab === 'overview' && (
                        <div className="space-y-6">
                            <p className="text-gray-300 leading-relaxed italic border-l-2 border-white/10 pl-4">
                                "{integration.description}"
                            </p>

                            <div>
                                <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
                                    <Zap className="w-4 h-4 text-amber-400" />
                                    Key Capabilities
                                </h4>
                                <div className="grid grid-cols-2 gap-2">
                                    {integration.capabilities?.map(cap => (
                                        <div key={cap} className="flex items-center gap-2 text-sm text-gray-400 bg-white/5 p-2 rounded-lg">
                                            <CheckCircle className="w-3 h-3 text-emerald-500" />
                                            {cap}
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
                                    <Info className="w-4 h-4 text-blue-400" />
                                    Common Use Cases
                                </h4>
                                <ul className="space-y-2">
                                    {integration.use_cases?.map((use, idx) => (
                                        <li key={idx} className="text-sm text-gray-400 flex gap-2">
                                            <span className="text-gray-600">•</span> {use}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}

                    {activeTab === 'setup' && (
                        <div className="space-y-6">
                            {integration.auth_type === 'oauth' ? (
                                <div className="bg-[#1c1c1e] border border-white/5 rounded-2xl p-12 text-center">
                                    <Shield className="w-12 h-12 mx-auto mb-4 text-emerald-400 opacity-50" />
                                    <h4 className="text-lg font-bold text-white mb-2">Secure OAuth Connection</h4>
                                    <p className="text-sm text-gray-400 mb-8 max-w-xs mx-auto">
                                        Authorizing {integration.name} allows Guild AI to securely access requested data without ever seeing your password.
                                    </p>
                                    <button
                                        onClick={handleOAuth}
                                        disabled={loading}
                                        className="bg-white text-black px-10 py-3 rounded-xl font-bold flex items-center gap-2 mx-auto hover:scale-105 transition-all"
                                    >
                                        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <ExternalLink className="w-4 h-4" />}
                                        Authorize {integration.name}
                                    </button>
                                </div>
                            ) : integration.api_key_instructions ? (
                                <div className="bg-[#1c1c1e] border border-white/5 rounded-2xl p-6">
                                    <h4 className="text-md font-bold text-white mb-4">{integration.api_key_instructions.title}</h4>
                                    <div className="space-y-4">
                                        {integration.api_key_instructions.steps.map(step => (
                                            <div key={step.step} className="flex gap-4">
                                                <div className="bg-white/10 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0">
                                                    {step.step}
                                                </div>
                                                <div>
                                                    <p className="text-sm font-medium text-white">{step.action}</p>
                                                    <p className="text-xs text-gray-500">{step.details}</p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ) : (
                                <div className="p-12 text-center text-gray-500">
                                    <ExternalLink className="w-12 h-12 mx-auto mb-4 opacity-20" />
                                    <p>Click "Authorize" to start the OAuth flow with {integration.name}.</p>
                                </div>
                            )}

                            {integration.auth_type !== 'oauth' && (
                                <div className="space-y-3">
                                    <label className="text-xs font-bold text-gray-400 uppercase tracking-widest">API Key / Access Token</label>
                                    <div className="relative">
                                        <Key className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4" />
                                        <input
                                            type={showKey ? "text" : "password"}
                                            placeholder="Enter token..."
                                            className="w-full bg-white/5 border border-white/5 rounded-xl pl-10 pr-12 py-3 text-sm focus:outline-none focus:border-white/20"
                                            onChange={(e) => handleInputChange('api_key', e.target.value)}
                                        />
                                        <button
                                            onClick={() => setShowKey(!showKey)}
                                            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white"
                                        >
                                            {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                        </button>
                                    </div>
                                    <div className="flex justify-between items-center text-[10px] text-gray-500 font-medium italic">
                                        <span>Estimated setup: {integration.estimated_setup_time}</span>
                                        <a href={integration.documentation_url} target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-white">
                                            Official Docs <ExternalLink className="w-2 h-2" />
                                        </a>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {activeTab === 'security' && (
                        <div className="space-y-6">
                            <div className="flex items-start gap-4 p-4 bg-emerald-500/5 border border-emerald-500/10 rounded-2xl">
                                <Shield className="w-6 h-6 text-emerald-400 shrink-0" />
                                <div>
                                    <h4 className="text-sm font-bold text-emerald-400 mb-1">Secure & Transparent</h4>
                                    <p className="text-xs text-gray-400 leading-relaxed">
                                        Your credentials are encrypted using AES-256 and stored in a secure vault. Guild AI never sells your data; it only uses requested scopes to perform actions on your behalf.
                                    </p>
                                </div>
                            </div>

                            <div>
                                <h4 className="text-sm font-bold text-white mb-3">Required Permissions</h4>
                                <div className="space-y-2">
                                    {(integration.required_permissions || ['Read/Write Access']).map(perm => (
                                        <div key={perm} className="flex items-center gap-2 text-xs text-gray-400">
                                            <Lock className="w-3 h-3 text-gray-600" />
                                            {perm}
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="flex items-center gap-2 p-3 bg-white/5 rounded-xl text-xs text-gray-500 italic">
                                <AlertTriangle className="w-4 h-4 text-amber-500" />
                                You can disconnect this service at any time, which immediately deletes all stored credentials.
                            </div>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="p-6 border-t border-white/5 bg-white/[0.02] flex justify-between items-center">
                    {error ? (
                        <div className="flex items-center gap-2 text-red-400 text-xs font-medium">
                            <AlertCircle className="w-4 h-4" />
                            {error}
                        </div>
                    ) : success ? (
                        <div className="flex items-center gap-2 text-emerald-400 text-sm font-bold">
                            <CheckCircle className="w-5 h-5" />
                            Connection Successful!
                        </div>
                    ) : (
                        <div />
                    )}

                    <button
                        onClick={integration.auth_type === 'oauth' ? handleOAuth : handleConnect}
                        disabled={loading || success}
                        className={`px-8 py-3 rounded-xl font-bold text-sm transition-all flex items-center gap-2 ${loading ? 'bg-white/10 text-gray-500' : 'bg-white text-black hover:scale-105 active:scale-95'
                            }`}
                    >
                        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> :
                            integration.auth_type === 'oauth' ? 'Start Authorization' : 'Connect Service'}
                    </button>
                </div>
            </motion.div>
        </div>
    );
};

export default IntegrationModal;
