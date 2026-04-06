/**
 * Guild-AI — Chat Interface (Primary View)
 *
 * Claude-style layout with:
 * - Collapsible conversation sidebar (date-grouped history)
 * - Message bubbles (user right, assistant left)
 * - Inline agent activity events + approval cards
 * - WebSocket real-time updates
 * - Onboarding mode when identity is incomplete
 */
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Plus, Send, PanelLeftClose, PanelLeft, Bot, User, Sparkles,
  CheckCircle2, XCircle, Clock, Loader2, ChevronDown,
} from 'lucide-react';
import { api } from '../../services/api';
import { guildWS } from '../../services/websocket';
import { useAuth } from '../../contexts/AuthContext';

/* ─── Helpers ─── */
function groupByDate(conversations) {
  const groups = { Today: [], Yesterday: [], 'This Week': [], Earlier: [] };
  const now = new Date();
  conversations.forEach((c) => {
    const d = new Date(c.created_at || Date.now());
    const diffDays = Math.floor((now - d) / 86400000);
    if (diffDays === 0) groups.Today.push(c);
    else if (diffDays === 1) groups.Yesterday.push(c);
    else if (diffDays < 7) groups['This Week'].push(c);
    else groups.Earlier.push(c);
  });
  return groups;
}

/* ─── Message Bubble ─── */
function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${isUser ? 'bg-indigo-500/20 text-indigo-400' : 'gradient-cobalt text-white'}`}>
        {isUser ? <User size={14} strokeWidth={1.5} /> : <Bot size={14} strokeWidth={1.5} />}
      </div>
      <div className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${isUser ? 'bg-indigo-500/15 text-zinc-200 rounded-tr-md' : 'glass-panel text-zinc-300 rounded-tl-md'}`}>
        {message.content}
        {message.tokens && (
          <span className="block mt-1 text-[10px] text-zinc-600">{message.tokens} tokens</span>
        )}
      </div>
    </motion.div>
  );
}

/* ─── Agent Activity Inline Event ─── */
function AgentEvent({ event }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="mx-auto max-w-md glass-panel rounded-xl px-4 py-2.5 flex items-center gap-3 text-xs"
    >
      <div className="w-6 h-6 rounded-full bg-emerald-500/20 flex items-center justify-center">
        <Sparkles size={12} className="text-emerald-400" />
      </div>
      <div className="flex-1 min-w-0">
        <span className="text-zinc-400 font-medium">{event.agent || 'Agent'}</span>
        <span className="text-zinc-600 mx-1">—</span>
        <span className="text-zinc-500">{event.description || 'processing...'}</span>
      </div>
      {event.progress != null && (
        <div className="w-12 h-1 rounded-full bg-white/5 overflow-hidden">
          <div className="h-full rounded-full bg-emerald-500 transition-all" style={{ width: `${event.progress * 100}%` }} />
        </div>
      )}
    </motion.div>
  );
}

/* ─── Approval Card (inline) ─── */
function ApprovalCard({ approval, onApprove, onReject }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="mx-auto max-w-lg glass-panel rounded-xl p-4 space-y-3"
    >
      <div className="flex items-center gap-2 text-amber-400 text-sm font-medium">
        <Clock size={14} strokeWidth={1.5} />
        Approval Required
      </div>
      <p className="text-sm text-zinc-300">{approval.description || 'An agent needs your approval to proceed.'}</p>
      <div className="flex gap-2">
        <button onClick={() => onApprove(approval)} className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg bg-emerald-500/20 text-emerald-400 text-sm font-medium hover:bg-emerald-500/30 transition-colors">
          <CheckCircle2 size={14} strokeWidth={1.5} /> Approve
        </button>
        <button onClick={() => onReject(approval)} className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 rounded-lg bg-red-500/20 text-red-400 text-sm font-medium hover:bg-red-500/30 transition-colors">
          <XCircle size={14} strokeWidth={1.5} /> Reject
        </button>
      </div>
    </motion.div>
  );
}

/* ─── Thinking Indicator ─── */
function ThinkingIndicator({ agent }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex gap-3 items-center"
    >
      <div className="w-8 h-8 rounded-full gradient-cobalt flex items-center justify-center ai-active-glow">
        <Bot size={14} className="text-white" />
      </div>
      <div className="glass-panel rounded-2xl rounded-tl-md px-4 py-3 flex items-center gap-2 text-sm text-zinc-400">
        <Loader2 size={14} className="animate-spin text-indigo-400" />
        {agent ? `${agent} is thinking...` : 'Thinking...'}
      </div>
    </motion.div>
  );
}

/* ═══════════════════════════════════════════
   Main Chat Interface
   ═══════════════════════════════════════════ */
export default function ChatInterface() {
  const { user, identityComplete } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [activeConvId, setActiveConvId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [thinkingAgent, setThinkingAgent] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [agentEvents, setAgentEvents] = useState([]);
  const messagesEndRef = useRef(null);

  /* Scroll to bottom on new message */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, agentEvents, thinkingAgent]);

  /* Subscribe to WebSocket events */
  useEffect(() => {
    const unsub1 = guildWS.on('agent_event', (data) => {
      setAgentEvents((prev) => [...prev.slice(-20), data]);
      setThinkingAgent(data.agent_id || data.agent || null);
    });
    const unsub2 = guildWS.on('workflow_complete', () => {
      setThinkingAgent(null);
    });
    return () => { unsub1(); unsub2(); };
  }, []);

  /* ── Send message ── */
  const handleSend = useCallback(async () => {
    if (!input.trim() || sending) return;
    const userMsg = { role: 'user', content: input.trim(), timestamp: Date.now() };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setSending(true);
    setThinkingAgent('Guild');

    try {
      let response;
      if (!identityComplete) {
        // Onboarding mode
        response = await api.onboarding.chat(userMsg.content);
      } else {
        // Normal orchestrator mode
        response = await api.agents.run('OrchestratorAgent', { goal: userMsg.content });
      }
      const assistantMsg = {
        role: 'assistant',
        content: response.response || response.result || response.reply || JSON.stringify(response),
        tokens: response.tokens_used,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'assistant', content: `Sorry, something went wrong: ${err.message}`, timestamp: Date.now() }]);
    } finally {
      setSending(false);
      setThinkingAgent(null);
      setAgentEvents([]);
    }
  }, [input, sending, identityComplete]);

  /* ── New chat ── */
  const handleNewChat = () => {
    setMessages([]);
    setAgentEvents([]);
    setActiveConvId(null);
  };

  /* ── Keyboard shortcut ── */
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const grouped = groupByDate(conversations);

  return (
    <div className="flex h-full">
      {/* ── Sidebar (conversation history) ── */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.aside
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 280, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="h-full border-r border-white/[0.06] flex flex-col bg-surface-base/50 overflow-hidden hidden md:flex"
          >
            <div className="p-3 border-b border-white/[0.06]">
              <button
                onClick={handleNewChat}
                className="w-full flex items-center gap-2 px-3 py-2.5 rounded-xl text-sm font-medium text-zinc-300 hover:bg-white/5 transition-colors border border-white/[0.06]"
              >
                <Plus size={16} strokeWidth={1.5} />
                New Chat
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-2 space-y-4">
              {Object.entries(grouped).map(([label, convs]) =>
                convs.length > 0 ? (
                  <div key={label}>
                    <p className="px-3 mb-1 text-[10px] font-medium text-zinc-600 uppercase tracking-wider">{label}</p>
                    {convs.map((c, i) => (
                      <button
                        key={c.id || i}
                        onClick={() => setActiveConvId(c.id)}
                        className={`w-full text-left px-3 py-2 rounded-lg text-sm truncate transition-colors ${activeConvId === c.id ? 'bg-white/5 text-zinc-200' : 'text-zinc-500 hover:text-zinc-300 hover:bg-white/[0.03]'}`}
                      >
                        {c.title || `Chat ${i + 1}`}
                      </button>
                    ))}
                  </div>
                ) : null
              )}
              {conversations.length === 0 && (
                <div className="px-3 py-8 text-center text-zinc-600 text-xs">
                  No conversations yet.<br />Start a new chat to begin.
                </div>
              )}
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* ── Main Chat Area ── */}
      <div className="flex-1 flex flex-col h-full min-w-0">
        {/* Header */}
        <div className="flex items-center gap-2 px-4 py-3 border-b border-white/[0.06]">
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-300 hover:bg-white/5 transition-colors hidden md:block">
            {sidebarOpen ? <PanelLeftClose size={18} strokeWidth={1.5} /> : <PanelLeft size={18} strokeWidth={1.5} />}
          </button>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-full gradient-cobalt flex items-center justify-center">
              <Bot size={12} className="text-white" />
            </div>
            <h1 className="text-sm font-heading font-bold text-zinc-200">
              {!identityComplete ? 'Onboarding — Tell Guild About Your Business' : 'Guild Orchestrator'}
            </h1>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center space-y-4 py-20">
              <div className="w-16 h-16 rounded-2xl gradient-cobalt flex items-center justify-center shadow-lg shadow-blue-500/20">
                <Sparkles size={28} className="text-white" />
              </div>
              <h2 className="text-xl font-heading font-bold text-zinc-200">
                {!identityComplete ? 'Welcome to Guild AI' : 'How can I help you grow today?'}
              </h2>
              <p className="text-sm text-zinc-500 max-w-md">
                {!identityComplete
                  ? "Let's get to know your business. Tell me about what you do, who your customers are, and what you're working toward."
                  : 'Ask me to create content, find leads, schedule campaigns, or build workflows. I\'ll coordinate the right agents for you.'}
              </p>
              <div className="flex flex-wrap gap-2 justify-center mt-4">
                {(!identityComplete
                  ? ["I run a candle business", "I'm a freelance designer", "I have an e-commerce store"]
                  : ["Create this week's content", "Show me my top leads", "Build a campaign for my new product"]
                ).map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => { setInput(suggestion); }}
                    className="px-3 py-1.5 rounded-full text-xs text-zinc-400 border border-white/[0.06] hover:border-indigo-500/30 hover:text-indigo-400 transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <React.Fragment key={i}>
              <MessageBubble message={msg} />
              {/* Show agent events after the last user message while thinking */}
              {msg.role === 'user' && i === messages.length - 1 && agentEvents.length > 0 && (
                <div className="space-y-2 py-1">
                  {agentEvents.slice(-3).map((evt, j) => (
                    <AgentEvent key={j} event={evt} />
                  ))}
                </div>
              )}
            </React.Fragment>
          ))}

          <AnimatePresence>
            {thinkingAgent && <ThinkingIndicator agent={thinkingAgent} />}
          </AnimatePresence>

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="px-4 py-3 border-t border-white/[0.06]">
          <div className="flex items-end gap-2 glass-panel rounded-xl px-3 py-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={!identityComplete ? "Tell me about your business..." : "Ask Guild anything..."}
              rows={1}
              className="flex-1 bg-transparent text-sm text-zinc-200 placeholder-zinc-600 resize-none outline-none max-h-32"
              style={{ minHeight: '36px' }}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || sending}
              className="p-2 rounded-lg bg-indigo-500 text-white hover:bg-indigo-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors flex-shrink-0"
            >
              <Send size={16} strokeWidth={1.5} />
            </button>
          </div>
          <p className="text-[10px] text-zinc-700 text-center mt-1.5">
            Guild may make mistakes. Verify important information.
          </p>
        </div>
      </div>
    </div>
  );
}
