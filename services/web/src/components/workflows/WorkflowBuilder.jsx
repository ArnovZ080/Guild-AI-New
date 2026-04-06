/**
 * Guild-AI — Workflow Builder (3 Modes)
 *
 * Tab 1: Pre-built Templates — card grid with launch
 * Tab 2: AI Builder — natural language → DAG preview → execute
 * Tab 3: Custom Builder — ReactFlow canvas
 */
import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactFlow, { Background, Controls, MiniMap } from 'reactflow';
import 'reactflow/dist/style.css';
import {
  Layout, Sparkles, GitBranch, Play, Loader2, Send,
  ChevronRight, Clock, Zap, Plus,
} from 'lucide-react';
import { api } from '../../services/api';
import { toast } from 'react-toastify';

/* ─── Known Templates ─── */
const TEMPLATES = [
  { name: 'weekly_content_pipeline', title: 'Weekly Content Pipeline', desc: 'Generate, review, and schedule a full week of content.', steps: ['ContentAgent', 'JudgeAgent', 'CalendarAgent'], cost: '~2,500 tokens' },
  { name: 'lead_capture_qualification', title: 'Lead Capture & Qualification', desc: 'Capture new leads, score ICP fit, and begin nurture.', steps: ['CRMAgent', 'PersonalizationAgent'], cost: '~1,200 tokens' },
  { name: 'product_launch_campaign', title: 'Product Launch Campaign', desc: 'Full multi-channel launch campaign with content + ads.', steps: ['ContentAgent', 'DistributionAgent', 'AnalyticsAgent'], cost: '~4,000 tokens' },
  { name: 'monthly_growth_review', title: 'Monthly Growth Review', desc: 'Analyze performance, identify trends, and recommend actions.', steps: ['AnalyticsAgent', 'ContentIntelligenceAgent'], cost: '~3,000 tokens' },
  { name: 'customer_onboarding', title: 'Customer Onboarding', desc: 'Welcome sequence for new customers.', steps: ['NurtureAgent', 'CRMAgent'], cost: '~1,500 tokens' },
  { name: 'customer_retention', title: 'Customer Retention', desc: 'Re-engage at-risk customers with tailored outreach.', steps: ['CRMAgent', 'NurtureAgent', 'ContentAgent'], cost: '~2,000 tokens' },
  { name: 'competitive_intel', title: 'Competitive Intelligence', desc: 'Research competitors and surface opportunities.', steps: ['ResearchAgent', 'AnalyticsAgent'], cost: '~2,500 tokens' },
];

/* ─── Template Card ─── */
function TemplateCard({ template, onLaunch }) {
  const [launching, setLaunching] = useState(false);

  const handleLaunch = async () => {
    setLaunching(true);
    try {
      await api.workflows.execute(template.name);
      toast.success(`${template.title} started!`);
    } catch (err) {
      toast.error(err.message);
    }
    setLaunching(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel rounded-xl p-5 space-y-3 hover:border-indigo-500/20 transition-colors"
    >
      <h3 className="text-sm font-heading font-bold text-zinc-200">{template.title}</h3>
      <p className="text-xs text-zinc-400">{template.desc}</p>

      <div className="flex flex-wrap gap-1">
        {template.steps.map((step, i) => (
          <span key={i} className="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400">
            {step}
            {i < template.steps.length - 1 && <ChevronRight size={8} />}
          </span>
        ))}
      </div>

      <div className="flex items-center justify-between pt-1">
        <span className="flex items-center gap-1 text-[10px] text-zinc-600">
          <Clock size={10} strokeWidth={1.5} /> {template.cost}
        </span>
        <button
          onClick={handleLaunch}
          disabled={launching}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-500 text-white text-xs font-medium hover:bg-indigo-600 disabled:opacity-40 transition-colors"
        >
          {launching ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />}
          Launch
        </button>
      </div>
    </motion.div>
  );
}

/* ─── AI Builder ─── */
function AIBuilder() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [dag, setDag] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    try {
      const result = await api.agents.run('OrchestratorAgent', { goal: prompt, require_preflight: true });
      setDag(result);
      toast.success('Workflow plan generated!');
    } catch (err) {
      toast.error(err.message);
    }
    setLoading(false);
  };

  const handleExecute = async () => {
    if (!dag) return;
    try {
      await api.workflows.execute('custom_ai', { plan: dag });
      toast.success('Workflow started!');
      setDag(null);
      setPrompt('');
    } catch (err) {
      toast.error(err.message);
    }
  };

  return (
    <div className="space-y-4">
      <div className="glass-panel rounded-xl p-6 space-y-4">
        <h3 className="text-sm font-heading font-bold text-zinc-300">Describe your workflow</h3>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g. Every Monday, generate 5 social posts, have the Judge review them, schedule for the week, and email me a summary"
          rows={4}
          className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/[0.06] text-sm text-zinc-200 placeholder-zinc-600 outline-none focus:border-indigo-500/30 resize-none"
        />
        <button
          onClick={handleGenerate}
          disabled={!prompt.trim() || loading}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-500 text-white text-sm font-medium hover:bg-indigo-600 disabled:opacity-40 transition-colors"
        >
          {loading ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />}
          Generate Plan
        </button>
      </div>

      {/* DAG Preview */}
      {dag && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="glass-panel rounded-xl p-6 space-y-4">
          <h3 className="text-sm font-heading font-bold text-zinc-300">Generated Workflow Plan</h3>
          <pre className="text-xs text-zinc-400 bg-white/[0.02] rounded-lg p-4 max-h-64 overflow-y-auto whitespace-pre-wrap">
            {typeof dag === 'string' ? dag : JSON.stringify(dag, null, 2)}
          </pre>
          <div className="flex gap-2">
            <button onClick={() => setDag(null)} className="px-4 py-2 rounded-lg text-sm text-zinc-400 hover:bg-white/5 transition-colors">
              Discard
            </button>
            <button onClick={handleExecute} className="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 text-white text-sm font-medium hover:bg-emerald-600 transition-colors">
              <Play size={14} /> Execute Workflow
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}

/* ─── Custom Builder (ReactFlow) ─── */
function CustomBuilder() {
  const [nodes, setNodes] = useState([
    { id: '1', type: 'default', data: { label: 'Start' }, position: { x: 100, y: 100 }, style: { background: '#1e1b4b', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)', borderRadius: '12px', fontSize: '12px' } },
    { id: '2', type: 'default', data: { label: 'ContentAgent' }, position: { x: 300, y: 100 }, style: { background: '#1e1b4b', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)', borderRadius: '12px', fontSize: '12px' } },
    { id: '3', type: 'default', data: { label: 'JudgeAgent' }, position: { x: 500, y: 100 }, style: { background: '#1e1b4b', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.3)', borderRadius: '12px', fontSize: '12px' } },
  ]);
  const [edges, setEdges] = useState([
    { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#6366f1' } },
    { id: 'e2-3', source: '2', target: '3', animated: true, style: { stroke: '#6366f1' } },
  ]);

  return (
    <div className="glass-panel rounded-xl overflow-hidden" style={{ height: '500px' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={(changes) => {}}
        onEdgesChange={(changes) => {}}
        fitView
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#1e1b4b" gap={24} size={1} />
        <Controls className="!bg-zinc-900 !border-white/10 !rounded-xl" />
        <MiniMap
          nodeColor="#6366f1"
          maskColor="rgba(0,0,0,0.8)"
          className="!bg-zinc-900 !border-white/10 !rounded-xl"
        />
      </ReactFlow>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Main Workflow Builder
   ═══════════════════════════════════════════ */
export default function WorkflowBuilder() {
  const [activeTab, setActiveTab] = useState('templates');

  const tabs = [
    { key: 'templates', label: 'Pre-built Templates', icon: Layout },
    { key: 'ai', label: 'AI Builder', icon: Sparkles },
    { key: 'custom', label: 'Custom Builder', icon: GitBranch },
  ];

  return (
    <div className="p-4 md:p-6 max-w-6xl mx-auto space-y-4">
      <h1 className="text-lg font-heading font-bold text-zinc-200">Workflow Builder</h1>

      {/* Tabs */}
      <div className="flex items-center gap-1 p-1 rounded-xl bg-white/[0.02] border border-white/[0.06] w-fit">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${activeTab === tab.key ? 'bg-white/[0.08] text-zinc-200' : 'text-zinc-500 hover:text-zinc-300'}`}
          >
            <tab.icon size={14} strokeWidth={1.5} />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'templates' && (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {TEMPLATES.map((t) => (
            <TemplateCard key={t.name} template={t} />
          ))}
        </div>
      )}

      {activeTab === 'ai' && <AIBuilder />}
      {activeTab === 'custom' && <CustomBuilder />}
    </div>
  );
}
