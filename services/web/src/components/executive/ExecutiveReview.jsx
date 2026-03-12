import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Check, X, AlertTriangle, CreditCard, Send, Lock, Eye } from 'lucide-react';

const ExecutiveReview = () => {
    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [threshold, setThreshold] = useState(0);

    useEffect(() => {
        // In a real app, this would fetch from /api/auth/pending
        const mockRequests = [
            {
                id: 'req_1',
                action_type: 'financial',
                description: 'Create invoice for Client: Acme Corp',
                params: { amount: 500, customer_id: 'cus_Acme', description: 'Monthly SaaS Retainer' },
                agent_id: 'FinancialAdvisorAgent',
                created_at: new Date().toISOString(),
            },
            {
                id: 'req_2',
                action_type: 'financial',
                description: 'Refund payment for Order #1234',
                params: { amount: 45, charge_id: 'ch_123', reason: 'Customer requested cancellation' },
                agent_id: 'SupportAgent',
                created_at: new Date().toISOString(),
            }
        ];
        setTimeout(() => {
            setRequests(mockRequests);
            setLoading(false);
        }, 800);
    }, []);

    const handleAuthorize = (id) => {
        setRequests(prev => prev.filter(req => req.id !== id));
        // Call API /api/auth/authorize
    };

    const handleDeny = (id) => {
        setRequests(prev => prev.filter(req => req.id !== id));
        // Call API /api/auth/deny
    };

    return (
        <div className="p-8 bg-slate-950 min-h-screen text-slate-100 font-sans">
            <div className="max-w-4xl mx-auto">
                <header className="flex justify-between items-center mb-10">
                    <div>
                        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                            Executive Review Hub
                        </h1>
                        <p className="text-zinc-600 mt-1">Authorize sensitive AI actions and financial transactions.</p>
                    </div>
                    <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex items-center gap-4">
                        <Shield className="text-blue-400 w-5 h-5" strokeWidth={1.5} />
                        <div>
                            <label className="text-xs text-zinc-500 uppercase tracking-wider block mb-1">Safety Threshold</label>
                            <div className="flex items-center gap-2">
                                <span className="text-xl font-mono text-white">${threshold}</span>
                                <button
                                    onClick={() => setThreshold(t => t + 50)}
                                    className="px-2 py-0.5 bg-slate-800 hover:bg-slate-700 rounded text-xs transition-colors"
                                >
                                    Adjust
                                </button>
                            </div>
                        </div>
                    </div>
                </header>

                {loading ? (
                    <div className="flex justify-center p-20">
                        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500" />
                    </div>
                ) : (
                    <div className="space-y-6">
                        <AnimatePresence>
                            {requests.length === 0 ? (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="text-center p-20 bg-slate-900/50 rounded-2xl border border-dashed border-slate-800"
                                >
                                    <Lock className="mx-auto text-zinc-400 w-12 h-12 mb-4" strokeWidth={1.5} />
                                    <h3 className="text-xl font-medium text-zinc-600">All Clear</h3>
                                    <p className="text-zinc-500">No pending actions require your authorization.</p>
                                </motion.div>
                            ) : (
                                requests.map((req) => (
                                    <motion.div
                                        key={req.id}
                                        layout
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, x: -100 }}
                                        className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl"
                                    >
                                        <div className="p-6 flex items-start gap-6">
                                            <div className={`p-4 rounded-xl ${req.action_type === 'financial' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-blue-500/10 text-blue-400'}`}>
                                                {req.action_type === 'financial' ? <CreditCard strokeWidth={1.5} /> : <Send strokeWidth={1.5} />}
                                            </div>

                                            <div className="flex-1">
                                                <div className="flex justify-between items-start">
                                                    <div>
                                                        <span className="text-xs font-mono text-zinc-500 uppercase tracking-tighter mb-1 block">
                                                            {req.agent_id} • {new Date(req.created_at).toLocaleTimeString()}
                                                        </span>
                                                        <h3 className="text-lg font-semibold">{req.description}</h3>
                                                    </div>
                                                    <div className="text-right">
                                                        {req.params.amount && (
                                                            <span className="text-2xl font-bold text-white">${req.params.amount}</span>
                                                        )}
                                                    </div>
                                                </div>

                                                <div className="mt-4 p-3 bg-slate-950/50 rounded-lg text-sm font-mono text-zinc-600 overflow-x-auto">
                                                    <pre>{JSON.stringify(req.params, null, 2)}</pre>
                                                </div>

                                                <div className="mt-6 flex justify-end gap-3">
                                                    <button
                                                        onClick={() => handleDeny(req.id)}
                                                        className="flex items-center gap-2 px-6 py-2 rounded-lg bg-slate-800 hover:bg-red-500/20 text-zinc-600 hover:text-red-400 transition-all border border-transparent hover:border-red-500/30"
                                                    >
                                                        <X size={18} strokeWidth={1.5} /> Deny
                                                    </button>
                                                    <button
                                                        onClick={() => handleAuthorize(req.id)}
                                                        className="flex items-center gap-2 px-6 py-2 rounded-lg bg-blue-600 hover:bg-[#1a6fff] text-white transition-all shadow-lg hover:shadow-blue-500/20"
                                                    >
                                                        <Check size={18} strokeWidth={1.5} /> Authorize Action
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </motion.div>
                                ))
                            )}
                        </AnimatePresence>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ExecutiveReview;
