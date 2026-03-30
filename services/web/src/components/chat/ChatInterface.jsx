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
        <div className="flex flex-col h-screen">
            {/* Executive Header */}
            <div className="bg-white/80 dark:bg-[#0C1222]/80 backdrop-blur-xl border-b border-gray-200/60 dark:border-white/[0.06] px-8 py-5 flex items-center justify-between sticky top-0 z-10">
                <div className="max-w-5xl mx-auto w-full flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-b from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
                            <Bot className="w-6 h-6 text-white" strokeWidth={1.5} />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-gray-900 dark:text-zinc-100 tracking-tight font-heading">Executive Orchestrator</h1>
                            <div className="flex items-center gap-2">
                                <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                                <p className="text-xs font-medium text-gray-500 dark:text-zinc-500 uppercase tracking-widest">System Voice Active</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        <div className="text-right hidden md:block">
                            <p className="text-[10px] font-medium text-gray-400 dark:text-zinc-600 uppercase">Strategic Focus</p>
                            <p className="text-xs font-semibold text-blue-600 dark:text-blue-400">Q1 Growth: Artisanal Scaling</p>
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
                                    <div className={`flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center shadow-sm ${message.role === 'user'
                                            ? 'bg-gray-800 dark:bg-zinc-800'
                                            : 'bg-white dark:bg-white/[0.06] border border-gray-200/60 dark:border-white/[0.06]'
                                        }`}>
                                        {message.role === 'user' ? <User className="w-5 h-5 text-white" strokeWidth={1.5} /> : <Bot className="w-5 h-5 text-blue-600 dark:text-blue-400" strokeWidth={1.5} />}
                                    </div>

                                    {/* Message Bundle */}
                                    <div className="space-y-3">
                                        <div className={`px-6 py-4 rounded-2xl shadow-sm border ${message.role === 'user'
                                            ? 'bg-gradient-to-b from-blue-500 to-blue-600 text-white border-blue-600 shadow-md shadow-blue-500/20'
                                            : message.isError
                                                ? 'bg-red-50 dark:bg-red-500/10 text-red-900 dark:text-red-300 border-red-200 dark:border-red-500/20'
                                                : 'bg-white dark:bg-white/[0.04] text-gray-800 dark:text-zinc-200 border-gray-200/60 dark:border-white/[0.06]'
                                            }`}>
                                            <div className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</div>
                                            <div className={`text-[10px] mt-3 font-medium uppercase tracking-wider opacity-50 ${message.role === 'user' ? 'text-white' : 'text-gray-500 dark:text-zinc-600'}`}>
                                                {formatTime(message.timestamp)}
                                            </div>
                                        </div>

                                        {/* Thought reflection block */}
                                        {message.thoughts && message.role === 'assistant' && (
                                            <div className="bg-gray-50 dark:bg-white/[0.03] border border-gray-200/60 dark:border-white/[0.06] rounded-xl overflow-hidden transition-all">
                                                <button
                                                    onClick={() => toggleThoughts(message.id)}
                                                    className="w-full px-4 py-2 flex items-center justify-between hover:bg-gray-100 dark:hover:bg-white/[0.05] transition-colors"
                                                >
                                                    <span className="text-[10px] font-medium text-gray-500 dark:text-zinc-500 uppercase flex items-center gap-2">
                                                        <Brain size={12} className="text-indigo-500 dark:text-indigo-400" strokeWidth={1.5} /> Orchestrator Logic
                                                    </span>
                                                    {showThoughts[message.id] ? <ChevronUp size={12} className="text-gray-400 dark:text-zinc-600" strokeWidth={1.5} /> : <ChevronDown size={12} className="text-gray-400 dark:text-zinc-600" strokeWidth={1.5} />}
                                                </button>
                                                <AnimatePresence>
                                                    {showThoughts[message.id] && (
                                                        <motion.div
                                                            initial={{ height: 0, opacity: 0 }}
                                                            animate={{ height: 'auto', opacity: 1 }}
                                                            exit={{ height: 0, opacity: 0 }}
                                                            className="px-4 py-3 border-t border-gray-200/60 dark:border-white/[0.06]"
                                                        >
                                                            <div className="text-[11px] font-mono text-gray-500 dark:text-zinc-500 leading-relaxed max-h-40 overflow-y-auto italic">
                                                                {message.thoughts}
                                                            </div>
                                                        </motion.div>
                                                    )}
                                                </AnimatePresence>
                                            </div>
                                        )}

                                        {/* Action Widgets */}
                                        {message.type === 'authorization' && (
                                            <div className="bg-gray-900 dark:bg-white/[0.06] p-5 rounded-2xl text-white dark:text-zinc-200 space-y-4 border border-gray-800 dark:border-white/[0.06]">
                                                <div className="flex items-center gap-2">
                                                    <ShieldAlert size={18} className="text-emerald-400" strokeWidth={1.5} />
                                                    <span className="text-xs font-bold uppercase">Authorization Required</span>
                                                </div>
                                                <p className="text-sm text-gray-400 dark:text-zinc-500">Agent `SEOAgency` requires approval to execute a high-budget keyword strategy.</p>
                                                <div className="flex gap-2">
                                                    <button className="flex-1 py-2 bg-emerald-500 text-white rounded-lg text-xs font-bold hover:bg-emerald-600 transition-colors">Authorize</button>
                                                    <button className="flex-1 py-2 bg-gray-700 dark:bg-white/5 text-gray-300 dark:text-zinc-500 rounded-lg text-xs font-bold hover:bg-gray-600 dark:hover:bg-white/10 transition-colors">Details</button>
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
                                <div className="w-10 h-10 rounded-xl bg-white dark:bg-white/[0.06] border border-gray-200/60 dark:border-white/[0.06] ai-active-glow flex items-center justify-center shadow-sm">
                                    <Brain className="w-5 h-5 text-blue-600 dark:text-blue-400" strokeWidth={1.5} />
                                </div>
                                <div className="bg-white dark:bg-white/[0.04] border border-gray-200/60 dark:border-white/[0.06] px-6 py-4 rounded-2xl shadow-sm text-xs font-medium text-gray-500 dark:text-zinc-500 uppercase tracking-widest flex items-center gap-3">
                                    <Activity size={14} className="text-indigo-500 dark:text-indigo-400 animate-pulse" strokeWidth={1.5} /> Synchronizing Workforce...
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
                        <div className="absolute -inset-1 bg-gradient-to-r from-blue-500/10 to-indigo-500/10 dark:from-blue-500/20 dark:to-indigo-500/20 rounded-2xl blur opacity-40 group-hover:opacity-60 transition duration-500"></div>
                        <div className="relative flex gap-3 bg-white dark:bg-white/[0.04] p-2 rounded-2xl border border-gray-200/60 dark:border-white/[0.06] shadow-lg dark:shadow-[0_4px_24px_rgba(0,0,0,0.3)]">
                            <textarea
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Command your workforce..."
                                className="flex-1 px-4 py-4 text-sm font-medium focus:outline-none resize-none bg-transparent text-gray-900 dark:text-zinc-200 placeholder:text-gray-400 dark:placeholder:text-zinc-600"
                                rows={1}
                                disabled={isLoading}
                            />
                            <button
                                onClick={() => handleSendMessage()}
                                disabled={isLoading || !inputValue.trim()}
                                className="px-6 py-3 bg-gradient-to-b from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:grayscale transition-all duration-200 shadow-md shadow-blue-500/20 hover:shadow-lg flex items-center gap-2 active:scale-[0.98]"
                            >
                                <Send className="w-4 h-4" strokeWidth={1.5} />
                                <span className="font-semibold text-xs uppercase tracking-wider">Execute</span>
                            </button>
                        </div>
                    </div>
                    <p className="text-[10px] text-center text-gray-400 dark:text-zinc-600 font-medium uppercase tracking-widest mt-4">
                        Powered by Guild Strategic Engine v2.4
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
