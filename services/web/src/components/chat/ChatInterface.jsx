import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Loader2, Brain, ChevronDown, ChevronUp, Activity, CheckCircle2, ShieldAlert } from 'lucide-react';
import { agentAPI } from '../../services/api';

const ChatInterface = () => {
    const [messages, setMessages] = useState([
        {
            id: 'init',
            role: 'assistant',
            content: "Welcome back, Executive. Internal systems are operational. I've analyzed your 90-day roadmap and have several optimization signals ready. How shall we proceed today?",
            timestamp: new Date(),
            thoughts: "Initializing Executive Suite. Loading strategic context from Project 'The Artisanal Bakery'. Checking recurring triggers..."
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showThoughts, setShowThoughts] = useState({});
    const messagesEndRef = useRef(null);

    // Auto-scroll to bottom
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const toggleThoughts = (id) => {
        setShowThoughts(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const handleSendMessage = async (messageText = inputValue) => {
        if (!messageText.trim()) return;

        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: messageText,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            // In Phase 3, we interact with the Orchestrator as the primary voice
            const response = await agentAPI.runAgent('OrchestratorAgent', {
                objective: messageText
            });

            const assistantMessage = {
                id: Date.now() + 1,
                role: 'assistant',
                content: response.data?.output || "I've processed your request through the workforce. Tactical adjustments have been applied to the content hub.",
                timestamp: new Date(),
                thoughts: response.process_log?.join('\n') || "Deconstructing objective... Identifying optimal agent roster... Enforcing 'Smart Contract' budget check...",
                educational: response.educational_takeaway,
                type: response.metadata?.type || 'standard'
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (error) {
            const errorMessage = {
                id: Date.now() + 1,
                role: 'assistant',
                content: `Disruption detected in orchestration: ${error.message}. I am stabilizing the workforce connection.`,
                isError: true,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="flex flex-col h-screen bg-[#F8FAFC]">
            {/* Executive Header */}
            <div className="bg-white/80 backdrop-blur-md border-b border-slate-200 px-8 py-5 flex items-center justify-between sticky top-0 z-10">
                <div className="max-w-5xl mx-auto w-full flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-[#1a6fff] rounded-xl flex items-center justify-center shadow-lg shadow-cobalt/20">
                            <Bot className="w-6 h-6 text-white" strokeWidth={1.5} />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-slate-900 tracking-tight">Executive Orchestrator</h1>
                            <div className="flex items-center gap-2">
                                <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                                <p className="text-xs font-bold text-zinc-500 uppercase tracking-widest">System Voice Active</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        <div className="text-right hidden md:block">
                            <p className="text-[10px] font-bold text-zinc-600 uppercase">Strategic Focus</p>
                            <p className="text-xs font-bold text-[#1a6fff]">Q1 Growth: Artisanal Scaling</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto px-6 py-10">
                <div className="max-w-4xl mx-auto space-y-10">
                    <AnimatePresence>
                        {messages.map((message) => (
                            <motion.div
                                key={message.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div className={`flex gap-4 max-w-[85%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                                    {/* Avatar */}
                                    <div className={`flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center shadow-sm ${message.role === 'user' ? 'bg-slate-800' : 'glass-panel'
                                        }`}>
                                        {message.role === 'user' ? <User className="w-5 h-5 text-white" strokeWidth={1.5} /> : <Bot className="w-5 h-5 text-[#1a6fff]" strokeWidth={1.5} />}
                                    </div>

                                    {/* Message Bundle */}
                                    <div className="space-y-3">
                                        <div className={`px-6 py-4 rounded-2xl shadow-sm border ${message.role === 'user'
                                            ? 'bg-[#1a6fff] text-white border-indigo-500'
                                            : message.isError
                                                ? 'bg-red-50 text-red-900 border-red-200'
                                                : 'bg-white text-slate-800 border-slate-200'
                                            }`}>
                                            <div className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</div>
                                            <div className={`text-[10px] mt-3 font-bold uppercase tracking-wider opacity-50 ${message.role === 'user' ? 'text-white' : 'text-zinc-600'}`}>
                                                {formatTime(message.timestamp)}
                                            </div>
                                        </div>

                                        {/* Thought reflection block */}
                                        {message.thoughts && message.role === 'assistant' && (
                                            <div className="bg-white/[0.03]/80 border border-slate-200 rounded-xl overflow-hidden transition-all">
                                                <button
                                                    onClick={() => toggleThoughts(message.id)}
                                                    className="w-full px-4 py-2 flex items-center justify-between hover:bg-white/5/50 transition-colors"
                                                >
                                                    <span className="text-[10px] font-bold text-zinc-500 uppercase flex items-center gap-2">
                                                        <Brain size={12} className="text-indigo-500" strokeWidth={1.5} /> Orchestrator Logic
                                                    </span>
                                                    {showThoughts[message.id] ? <ChevronUp size={12} strokeWidth={1.5} /> : <ChevronDown size={12} strokeWidth={1.5} />}
                                                </button>
                                                <AnimatePresence>
                                                    {showThoughts[message.id] && (
                                                        <motion.div
                                                            initial={{ height: 0, opacity: 0 }}
                                                            animate={{ height: 'auto', opacity: 1 }}
                                                            exit={{ height: 0, opacity: 0 }}
                                                            className="px-4 py-3 border-t border-slate-200"
                                                        >
                                                            <div className="text-[11px] font-mono text-zinc-500 leading-relaxed max-h-40 overflow-y-auto italic">
                                                                {message.thoughts}
                                                            </div>
                                                        </motion.div>
                                                    )}
                                                </AnimatePresence>
                                            </div>
                                        )}

                                        {/* Action Widgets (Mock for Phase 3) */}
                                        {message.type === 'authorization' && (
                                            <div className="bg-zinc-900/60 p-5 rounded-2xl text-white space-y-4">
                                                <div className="flex items-center gap-2">
                                                    <ShieldAlert size={18} className="text-emerald-400" strokeWidth={1.5} />
                                                    <span className="text-xs font-bold uppercase">Authorization Required</span>
                                                </div>
                                                <p className="text-sm text-zinc-600">Agent `SEOAgency` requires approval to execute a high-budget keyword strategy.</p>
                                                <div className="flex gap-2">
                                                    <button className="flex-1 py-2 bg-emerald-500 text-white rounded-lg text-xs font-bold">Authorize</button>
                                                    <button className="flex-1 py-2 bg-slate-700 text-zinc-600 rounded-lg text-xs font-bold">Details</button>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {/* Loading Indicator */}
                    {isLoading && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                            <div className="flex gap-4">
                                <div className="w-10 h-10 rounded-xl glass-panel ai-active-glow flex items-center justify-center shadow-sm">
                                    <Brain className="w-5 h-5 text-[#1a6fff]" strokeWidth={1.5} />
                                </div>
                                <div className="glass-panel px-6 py-4 rounded-2xl shadow-sm text-xs font-bold text-zinc-600 uppercase tracking-widest flex items-center gap-3">
                                    <Activity size={14} className="text-indigo-400 animate-pulse" strokeWidth={1.5} /> Synchronizing Workforce...
                                </div>
                            </div>
                        </motion.div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Elegant Input Area */}
            <div className="p-8 bg-transparent">
                <div className="max-w-4xl mx-auto">
                    <div className="relative group">
                        <div className="absolute -inset-1 bg-gradient-to-r from-blue-500/20 to-indigo-500/20 rounded-2xl blur opacity-20 group-hover:opacity-30 transition duration-1000 group-hover:duration-200"></div>
                        <div className="relative flex gap-3 bg-white p-2 rounded-2xl border border-slate-200 shadow-xl">
                            <textarea
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Command your workforce..."
                                className="flex-1 px-4 py-4 text-sm font-medium focus:outline-none resize-none bg-transparent"
                                rows={1}
                                disabled={isLoading}
                            />
                            <button
                                onClick={() => handleSendMessage()}
                                disabled={isLoading || !inputValue.trim()}
                                className="px-6 py-3 bg-[#1a6fff] text-white rounded-xl hover:bg-[#4d8fff] disabled:opacity-50 disabled:grayscale transition-all duration-200 shadow-lg shadow-cobalt/20 flex items-center gap-2"
                            >
                                <Send className="w-4 h-4" strokeWidth={1.5} />
                                <span className="font-bold text-xs uppercase tracking-wider">Execute</span>
                            </button>
                        </div>
                    </div>
                    <p className="text-[10px] text-center text-zinc-600 font-bold uppercase tracking-widest mt-4">
                        Powered by Antigravity Strategic Engine v2.4
                    </p>
                </div>
            </div>
        </div>
    );
};

// Utility
const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

export default ChatInterface;
