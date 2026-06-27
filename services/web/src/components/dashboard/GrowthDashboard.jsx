/**
 * Guild-AI - Growth Dashboard
 *
 * Replaces ExecutiveDashboard.
 * Shows: stat cards, "What's Working" insights, goals & milestones, recent leads.
 * All data from API - no mock/hardcoded values.
 */
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import {
  TrendingUp, Users, FileText, DollarSign, Target, Plus,
  Loader2, ArrowUpRight, ArrowDownRight, RefreshCw, Sparkles, Trophy,
} from 'lucide-react';
import { api } from '../../services/api';
import { toast } from 'react-toastify';

/* ─── Count-up hook ─── */
function useCountUp(target, duration = 900) {
  const [count, setCount] = useState(0);
  const ref = useRef(null);
  const inView = useInView(ref, { once: true });

  useEffect(() => {
    if (!inView || !target) return;
    const num = parseFloat(String(target).replace(/[^0-9.]/g, '')) || 0;
    const prefix = String(target).match(/^[^0-9]*/)?.[0] || '';
    const suffix = String(target).match(/[^0-9.]*$/)?.[0] || '';
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - p, 3); // ease-out cubic
      setCount({ val: Math.round(ease * num), prefix, suffix });
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, [inView, target, duration]);

  return { ref, count };
}

/* ─── Mini sparkline ─── */
function Sparkline({ data = [], color = '#5E6AD2' }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true });
  const W = 64, H = 24;
  if (!data.length) return null;
  const min = Math.min(...data), max = Math.max(...data);
  const range = max - min || 1;
  const pts = data.map((v, i) => [
    (i / (data.length - 1)) * W,
    H - ((v - min) / range) * (H - 4) - 2,
  ]);
  const d = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
  const totalLen = pts.reduce((acc, p, i) => {
    if (i === 0) return 0;
    const prev = pts[i - 1];
    return acc + Math.hypot(p[0] - prev[0], p[1] - prev[1]);
  }, 0);

  return (
    <svg ref={ref} width={W} height={H} viewBox={`0 0 ${W} ${H}`} fill="none">
      <motion.path
        d={d}
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        initial={{ pathLength: 0, opacity: 0 }}
        animate={inView ? { pathLength: 1, opacity: 1 } : {}}
        transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      />
    </svg>
  );
}

/* ─── Stat Card ─── */
function StatCard({ icon: Icon, label, value, change, color, glowColor, sparkData }) {
  const isPositive = change >= 0;
  const { ref, count } = useCountUp(value);
  const displayVal = count
    ? `${count.prefix}${count.val}${count.suffix}`
    : value;

  return (
    <motion.div
      ref={ref}
      whileHover={{ y: -4, transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] } }}
      className="glass-panel rounded-xl p-4 space-y-2 cursor-default relative overflow-hidden"
      style={{
        boxShadow: glowColor ? `0 0 0 1px ${glowColor}` : undefined,
        transition: 'box-shadow 0.3s ease, transform 0.25s cubic-bezier(0.16,1,0.3,1)',
      }}
      onMouseEnter={e => { if (glowColor) e.currentTarget.style.boxShadow = `0 4px 24px ${glowColor}, 0 0 0 1px ${glowColor}`; }}
      onMouseLeave={e => { if (glowColor) e.currentTarget.style.boxShadow = `0 0 0 1px ${glowColor}`; }}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs text-zinc-500">{label}</span>
        <div className="flex items-center gap-2">
          {sparkData && <Sparkline data={sparkData} color={glowColor?.replace(/[^,]+\)$/, '0.8)')} />}
          <div className={`w-8 h-8 rounded-lg ${color} flex items-center justify-center`}>
            <Icon size={16} strokeWidth={1.5} />
          </div>
        </div>
      </div>
      <p className="text-2xl font-bold text-zinc-200 tabular-nums">{displayVal}</p>
      {change != null && (
        <div className={`flex items-center gap-1 text-xs ${isPositive ? 'text-emerald-400' : 'text-red-400'}`}>
          {isPositive ? <ArrowUpRight size={12} /> : <ArrowDownRight size={12} />}
          {Math.abs(change)}%
        </div>
      )}
    </motion.div>
  );
}

/* ─── Goal Card ─── */
function GoalCard({ goal, onRepeat }) {
  const pct = goal.progress || 0;
  const currentVal = goal.current_value || Math.round(pct * (goal.target_value || 100));
  const targetVal = goal.target_value || 100;

  return (
    <div className="glass-panel rounded-xl p-4 space-y-3">
      <div className="flex items-start gap-2">
        <Target size={16} className="text-indigo-400 flex-shrink-0 mt-0.5" strokeWidth={1.5} />
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-medium text-zinc-200 truncate">{goal.title || goal.description}</h4>
          <p className="text-xs text-zinc-400">{currentVal.toLocaleString()} / {targetVal.toLocaleString()}</p>
        </div>
        <span className="text-xs font-medium text-zinc-400">{Math.round(pct * 100)}%</span>
      </div>
      <div className="w-full h-2 rounded-full bg-white/5 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct * 100}%` }}
          transition={{ duration: 0.8 }}
          className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-emerald-500"
        />
      </div>
      {pct >= 1 && (
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1 text-xs text-emerald-400">
            <Trophy size={12} strokeWidth={1.5} /> Milestone reached!
          </div>
          <button onClick={() => onRepeat(goal)} className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors">
            Set new target →
          </button>
        </div>
      )}
    </div>
  );
}

/* ─── Lead Row ─── */
function LeadRow({ lead }) {
  const score = lead.icp_score || lead.health_score || 0;
  return (
    <div className="flex items-center gap-3 py-2 border-b border-white/[0.03] last:border-0">
      <div className="w-8 h-8 rounded-full bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center text-indigo-400 text-xs font-bold flex-shrink-0">
        {(lead.name || lead.email || '?')[0].toUpperCase()}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm text-zinc-300 truncate">{lead.name || lead.email}</p>
        <p className="text-xs text-zinc-600">{lead.source || 'Unknown source'}</p>
      </div>
      <span className={`text-xs font-medium px-2 py-0.5 rounded ${score >= 80 ? 'bg-emerald-500/15 text-emerald-400' : score >= 60 ? 'bg-amber-500/15 text-amber-400' : 'bg-zinc-500/10 text-zinc-400'}`}>
        ICP {score}%
      </span>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Main Growth Dashboard
   ═══════════════════════════════════════════ */
export default function GrowthDashboard() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ content: 0, leads: 0, pipeline: 0, revenue: 0, funnels: 0, funnelSubmissions: 0 });
  const [goals, setGoals] = useState([]);
  const [leads, setLeads] = useState([]);
  const [funnels, setFunnels] = useState([]);
  const [insights, setInsights] = useState('');
  const [showAddGoal, setShowAddGoal] = useState(false);
  const [newGoal, setNewGoal] = useState('');

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [perf, goalData, leadData, pipe, funnelData] = await Promise.allSettled([
        api.content.performance(),
        api.goals.list(),
        api.crm.newLeads(),
        api.crm.pipeline(),
        api.funnels.list()
      ]);
      if (perf.status === 'fulfilled') {
        const p = perf.value;
        setStats((prev) => ({
          ...prev,
          content: p.total_published || p.count || 0,
        }));
        setInsights(p.insights || '');
      }
      if (goalData.status === 'fulfilled') {
        setGoals(goalData.value?.goals || goalData.value || []);
      }
      if (leadData.status === 'fulfilled') {
        setLeads(leadData.value?.leads || leadData.value || []);
        setStats((prev) => ({
          ...prev,
          leads: (leadData.value?.leads || leadData.value || []).length,
        }));
      }
      if (pipe.status === 'fulfilled') {
        const pipeData = pipe.value;
        setStats((prev) => ({
          ...prev,
          pipeline: pipeData?.stages?.length || pipeData?.active || 0,
          revenue: pipeData?.total_value || 0,
        }));
      }
      if (funnelData.status === 'fulfilled') {
        const funs = funnelData.value || [];
        setFunnels(funs);
        setStats((prev) => ({
          ...prev,
          funnels: funs.length,
          funnelSubmissions: funs.reduce((acc, f) => acc + (f.submissions || 0), 0)
        }));
      }
    } catch { /* ok */ }
    setLoading(false);
  }, []);

  useEffect(() => { loadData(); }, [loadData]);

  const handleAddGoal = async () => {
    if (!newGoal.trim()) return;
    try {
      await api.goals.create({ title: newGoal, target_value: 100 });
      setNewGoal('');
      setShowAddGoal(false);
      toast.success('Goal created!');
      loadData();
    } catch (err) { toast.error(err.message); }
  };

  const handleRepeatGoal = async (goal) => {
    try {
      await api.goals.repeat(goal.id, { new_target: (goal.target_value || 100) * 1.5 });
      toast.success('New target set!');
      loadData();
    } catch (err) { toast.error(err.message); }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Loader2 size={24} className="animate-spin text-indigo-400" />
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-heading font-bold text-zinc-200">Growth Dashboard</h1>
        <button onClick={loadData} className="p-2 rounded-lg text-zinc-400 hover:text-zinc-300 hover:bg-white/5 transition-colors">
          <RefreshCw size={16} strokeWidth={1.5} />
        </button>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <StatCard icon={FileText} label="Content Published" value={stats.content}
          color="bg-indigo-500/10 border border-indigo-400/40 text-indigo-400"
          glowColor="rgba(94,106,210,0.25)" />
        <StatCard icon={Users} label="Funnel Submissions" value={stats.funnelSubmissions}
          color="bg-emerald-500/10 border border-emerald-400/40 text-emerald-400"
          glowColor="rgba(34,197,94,0.2)" />
        <StatCard icon={TrendingUp} label="Active Funnels" value={stats.funnels}
          color="bg-amber-500/10 border border-amber-400/40 text-amber-400"
          glowColor="rgba(245,158,11,0.2)" />
        <StatCard icon={DollarSign} label="Revenue Influenced" value={`$${(stats.revenue / 1000).toFixed(1)}k`}
          color="bg-indigo-500/10 border border-indigo-400/40 text-indigo-400"
          glowColor="rgba(94,106,210,0.2)" />
      </div>

      {/* What's Working */}
      <div className="glass-panel rounded-xl p-5 space-y-2">
        <div className="flex items-center gap-2 text-sm font-medium text-zinc-300">
          <Sparkles size={14} className="text-amber-400" strokeWidth={1.5} />
          What's Working
        </div>
        <p className="text-sm text-zinc-400 leading-relaxed">
          {insights || 'Start publishing content and generating leads to see AI-powered insights about what\'s working for your business.'}
        </p>
        {insights && <p className="text-xs text-zinc-600 italic">- ContentIntelligenceAgent</p>}
      </div>

      {/* Goals & Milestones */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-heading font-bold text-zinc-300">Goals & Milestones</h2>
          <button onClick={() => setShowAddGoal(!showAddGoal)} className="flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 transition-colors">
            <Plus size={14} strokeWidth={1.5} /> Add Goal
          </button>
        </div>

        {showAddGoal && (
          <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} className="glass-panel rounded-xl p-4 flex gap-2">
            <input
              value={newGoal}
              onChange={(e) => setNewGoal(e.target.value)}
              placeholder="e.g. Grow Instagram to 5,000 followers"
              className="flex-1 px-3 py-2 rounded-lg bg-white/5 border border-white/[0.06] text-sm text-zinc-200 placeholder-zinc-600 outline-none focus:border-indigo-500/30"
              onKeyDown={(e) => e.key === 'Enter' && handleAddGoal()}
            />
            <button onClick={handleAddGoal} className="px-4 py-2 rounded-lg bg-indigo-500 text-white text-sm font-medium hover:bg-indigo-600 transition-colors">
              Create
            </button>
          </motion.div>
        )}

        {goals.length === 0 ? (
          <div className="glass-panel rounded-xl p-8 text-center space-y-2">
            <Target size={28} className="mx-auto text-zinc-600" strokeWidth={1.5} />
            <p className="text-sm text-zinc-400">No goals set yet.</p>
            <button onClick={() => setShowAddGoal(true)} className="text-xs text-indigo-400 hover:text-indigo-300">Create your first goal →</button>
          </div>
        ) : (
          <div className="grid gap-3 md:grid-cols-2">
            {goals.map((goal, i) => (
              <GoalCard key={goal.id || i} goal={goal} onRepeat={handleRepeatGoal} />
            ))}
          </div>
        )}
      </div>

      {/* Recent Leads */}
      <div className="space-y-3">
        <h2 className="text-sm font-heading font-bold text-zinc-300">Recent Leads</h2>
        {leads.length === 0 ? (
          <div className="glass-panel rounded-xl p-8 text-center space-y-2">
            <Users size={28} className="mx-auto text-zinc-600" strokeWidth={1.5} />
            <p className="text-sm text-zinc-400">No leads captured yet.</p>
            <p className="text-xs text-zinc-600">Leads will appear here as your content captures engagement.</p>
          </div>
        ) : (
          <div className="glass-panel rounded-xl p-3">
            {leads.slice(0, 10).map((lead, i) => (
              <LeadRow key={lead.id || i} lead={lead} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
