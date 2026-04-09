/**
 * Guild-AI - Agent Activity Theater
 *
 * Real-time visibility into agent operations.
 * Card grid + activity feed + pending approvals.
 * Connected via WebSocket for live updates.
 */
import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Activity, Bot, Zap, Clock, CheckCircle2, XCircle, ChevronDown,
  ChevronUp, Info, Loader2, AlertCircle, HelpCircle,
} from 'lucide-react';
import { guildWS } from '../../services/websocket';
import { api } from '../../services/api';
import { toast } from 'react-toastify';

/* ─── Status config ─── */
const statusConfig = {
  active: { color: 'text-emerald-400', bg: 'bg-emerald-500/15', pulse: 'animate-pulse', label: 'Active' },
  thinking: { color: 'text-amber-400', bg: 'bg-amber-500/15', pulse: 'animate-pulse', label: 'Thinking' },
  idle: { color: 'text-zinc-400', bg: 'bg-zinc-500/10', pulse: '', label: 'Idle' },
  failed: { color: 'text-red-400', bg: 'bg-red-500/15', pulse: '', label: 'Failed' },
  complete: { color: 'text-blue-400', bg: 'bg-blue-500/15', pulse: '', label: 'Complete' },
};

/* ─── Agent Card ─── */
function AgentCard({ agent }) {
  const [expanded, setExpanded] = useState(false);
  const status = statusConfig[agent.status] || statusConfig.idle;

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`glass-panel rounded-xl p-4 space-y-2 ${agent.status === 'active' ? 'ai-active-glow' : ''}`}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <div className={`w-8 h-8 rounded-lg ${status.bg} flex items-center justify-center ${status.pulse}`}>
            <Bot size={16} className={status.color} strokeWidth={1.5} />
          </div>
          <div>
            <h4 className="text-sm font-medium text-zinc-200">{agent.name || agent.agent_id}</h4>
            <span className={`text-xs font-medium ${status.color}`}>{status.label}</span>
          </div>
        </div>
        {agent.progress != null && (
          <span className="text-xs text-zinc-400">{Math.round(agent.progress * 100)}%</span>
        )}
      </div>

      {agent.description && <p className="text-xs text-zinc-400">{agent.description}</p>}

      {agent.progress != null && (
        <div className="w-full h-1 rounded-full bg-white/5 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${agent.progress * 100}%` }}
            className="h-full rounded-full bg-indigo-500"
          />
        </div>
      )}

      {/* Why/How */}
      {(agent.why || agent.how) && (
        <div className="space-y-1 text-xs">
          {agent.why && (
            <div className="flex items-start gap-1.5 text-zinc-400">
              <HelpCircle size={12} className="text-amber-500 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
              <span><strong className="text-zinc-400">Why:</strong> {agent.why}</span>
            </div>
          )}
          {agent.how && (
            <div className="flex items-start gap-1.5 text-zinc-400">
              <Info size={12} className="text-blue-400 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
              <span><strong className="text-zinc-400">How:</strong> {agent.how}</span>
            </div>
          )}
        </div>
      )}

      {/* Expandable Log */}
      <button onClick={() => setExpanded(!expanded)} className="flex items-center gap-1 text-xs text-zinc-600 hover:text-zinc-400 transition-colors">
        {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
        {expanded ? 'Hide log' : 'Show log'}
      </button>
      <AnimatePresence>
        {expanded && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
            <pre className="text-xs text-zinc-600 bg-white/[0.02] rounded-lg p-2 max-h-32 overflow-y-auto whitespace-pre-wrap">
              {agent.process_log || agent.log || 'No log data available.'}
            </pre>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

/* ─── Activity Feed Item ─── */
function FeedItem({ event }) {
  const time = event.timestamp ? new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
  return (
    <div className="flex gap-2 text-xs py-1.5 border-b border-white/[0.03] last:border-0">
      <span className="text-zinc-600 w-12 flex-shrink-0">{time}</span>
      <div className="flex-1 min-w-0">
        <span className="text-indigo-400 font-medium">{event.agent_id || event.agent || 'System'}</span>
        <span className="text-zinc-600 mx-1">→</span>
        <span className="text-zinc-400">{event.description || event.event_type || 'event'}</span>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Main Theater
   ═══════════════════════════════════════════ */
export default function AgentActivityTheater() {
  const [agents, setAgents] = useState([]);
  const [feed, setFeed] = useState([]);
  const [loading, setLoading] = useState(true);

  /* ── Load historical events ── */
  useEffect(() => {
    (async () => {
      try {
        const data = await api.agents.events();
        if (Array.isArray(data)) setFeed(data.slice(-50));
      } catch { /* ok */ }
      try {
        const data = await api.agents.list();
        if (data?.agents) {
          setAgents(data.agents.map((a) => ({ ...a, status: 'idle', name: a.name || a.agent_name })));
        }
      } catch { /* ok */ }
      setLoading(false);
    })();
  }, []);

  /* ── WebSocket subscription ── */
  useEffect(() => {
    const unsub = guildWS.on('*', (data) => {
      // Update feed
      setFeed((prev) => [...prev.slice(-100), { ...data, timestamp: data.timestamp || new Date().toISOString() }]);
      // Update agent card
      if (data.agent_id) {
        setAgents((prev) => {
          const idx = prev.findIndex((a) => a.agent_id === data.agent_id || a.name === data.agent_id);
          if (idx >= 0) {
            const updated = [...prev];
            updated[idx] = { ...updated[idx], ...data, status: data.event_type === 'complete' ? 'complete' : 'active' };
            return updated;
          }
          return [...prev, { agent_id: data.agent_id, name: data.agent_id, status: 'active', ...data }];
        });
      }
    });
    return unsub;
  }, []);

  const activeCount = agents.filter((a) => a.status === 'active' || a.status === 'thinking').length;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 size={24} className="animate-spin text-indigo-400" />
      </div>
    );
  }

  return (
    <div className="flex flex-col lg:flex-row h-full">
      {/* ── Main View (agent cards) ── */}
      <div className="flex-1 p-4 md:p-6 overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <h1 className="text-lg font-heading font-bold text-zinc-200">Agent Theater</h1>
            <div className="flex items-center gap-1.5 text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-zinc-400">{activeCount} active</span>
            </div>
          </div>
        </div>

        {agents.length === 0 ? (
          <div className="glass-panel rounded-xl p-12 text-center space-y-3">
            <Activity size={32} className="mx-auto text-zinc-600" strokeWidth={1.5} />
            <p className="text-sm text-zinc-400">No agent activity yet.</p>
            <p className="text-xs text-zinc-600">Start a conversation or run a workflow to see agents in action.</p>
          </div>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
            {agents.map((agent, i) => (
              <AgentCard key={agent.agent_id || agent.name || i} agent={agent} />
            ))}
          </div>
        )}
      </div>

      {/* ── Activity Feed (right panel) ── */}
      <aside className="w-full lg:w-80 border-t lg:border-t-0 lg:border-l border-white/[0.06] flex flex-col bg-surface-base/50">
        <div className="px-4 py-3 border-b border-white/[0.06] flex items-center gap-2">
          <Zap size={14} className="text-amber-400" strokeWidth={1.5} />
          <h2 className="text-sm font-medium text-zinc-300">Activity Feed</h2>
          <span className="ml-auto text-xs text-zinc-600">{feed.length} events</span>
        </div>
        <div className="flex-1 overflow-y-auto px-3 py-2">
          {feed.length === 0 ? (
            <p className="text-xs text-zinc-600 text-center py-8">Waiting for events...</p>
          ) : (
            feed.slice().reverse().map((evt, i) => <FeedItem key={i} event={evt} />)
          )}
        </div>
      </aside>
    </div>
  );
}
