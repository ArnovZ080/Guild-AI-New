/**
 * Guild-AI — Settings Page (Unified)
 *
 * 6 tabs: Business Profile | Integrations | Subscription | Knowledge Base | Preferences | Admin
 */
import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import {
  User, Link2, CreditCard, BookOpen, Sliders, Shield,
  Loader2, Check, Upload, Trash2, ExternalLink, Sun, Moon,
  Bell, BellOff, ToggleLeft, ToggleRight,
} from 'lucide-react';
import { api } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../ThemeProvider';
import { toast } from 'react-toastify';

/* ─── Tab config ─── */
const TABS = [
  { key: 'profile', label: 'Business Profile', icon: User },
  { key: 'integrations', label: 'Integrations', icon: Link2 },
  { key: 'subscription', label: 'Subscription', icon: CreditCard },
  { key: 'knowledge', label: 'Knowledge Base', icon: BookOpen },
  { key: 'preferences', label: 'Preferences', icon: Sliders },
  { key: 'admin', label: 'Admin', icon: Shield },
];

/* ── Business Profile Tab ── */
function ProfileTab() {
  const [identity, setIdentity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const data = await api.identity.get();
        setIdentity(data);
      } catch { setIdentity({}); }
      setLoading(false);
    })();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.identity.update(identity);
      toast.success('Identity saved!');
    } catch (err) { toast.error(err.message); }
    setSaving(false);
  };

  if (loading) return <Loader2 size={20} className="animate-spin text-indigo-400 mx-auto my-12" />;

  const fields = [
    { key: 'business_name', label: 'Business Name' },
    { key: 'industry', label: 'Industry' },
    { key: 'target_audience', label: 'Target Audience' },
    { key: 'brand_voice', label: 'Brand Voice' },
    { key: 'unique_value', label: 'Unique Value Proposition' },
    { key: 'goals', label: 'Business Goals' },
  ];

  const completion = identity?.completion_percentage || 0;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <h3 className="text-sm font-heading font-bold text-zinc-300">Business Identity</h3>
        <span className={`text-xs font-medium px-2 py-0.5 rounded ${completion >= 80 ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>
          {Math.round(completion)}% complete
        </span>
      </div>

      <div className="w-full h-1.5 rounded-full bg-white/5 overflow-hidden">
        <div className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-emerald-500 transition-all" style={{ width: `${completion}%` }} />
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        {fields.map(({ key, label }) => (
          <div key={key}>
            <label className="text-xs text-zinc-500 mb-1 block">{label}</label>
            <input
              value={identity?.[key] || ''}
              onChange={(e) => setIdentity({ ...identity, [key]: e.target.value })}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/[0.06] text-sm text-zinc-200 placeholder-zinc-600 outline-none focus:border-indigo-500/30"
            />
          </div>
        ))}
      </div>

      <button
        onClick={handleSave}
        disabled={saving}
        className="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-500 text-white text-sm font-medium hover:bg-indigo-600 disabled:opacity-40 transition-colors"
      >
        {saving ? <Loader2 size={14} className="animate-spin" /> : <Check size={14} />}
        Save Changes
      </button>
    </div>
  );
}

/* ── Integrations Tab ── */
function IntegrationsTab() {
  const [connectors, setConnectors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const data = await api.integrations.list();
        setConnectors(data?.integrations || data || []);
      } catch { /* ok */ }
      setLoading(false);
    })();
  }, []);

  if (loading) return <Loader2 size={20} className="animate-spin text-indigo-400 mx-auto my-12" />;

  return (
    <div className="space-y-3">
      {connectors.length === 0 ? (
        <div className="glass-panel rounded-xl p-8 text-center text-sm text-zinc-500">
          No integrations available yet.
        </div>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {connectors.map((c, i) => (
            <div key={c.platform || i} className="glass-panel rounded-xl p-4 flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 text-xs font-bold">
                {(c.platform || 'INT')[0].toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-zinc-200 capitalize">{c.platform || c.name}</p>
                <p className="text-xs text-zinc-500">{c.connected ? 'Connected' : 'Not connected'}</p>
              </div>
              <button className={`text-xs px-2.5 py-1 rounded-lg ${c.connected ? 'bg-red-500/10 text-red-400' : 'bg-emerald-500/10 text-emerald-400'} transition-colors`}>
                {c.connected ? 'Disconnect' : 'Connect'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

/* ── Subscription Tab ── */
function SubscriptionTab() {
  const [sub, setSub] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const data = await api.subscription.status();
        setSub(data);
      } catch { /* ok */ }
      setLoading(false);
    })();
  }, []);

  if (loading) return <Loader2 size={20} className="animate-spin text-indigo-400 mx-auto my-12" />;

  const plans = [
    { name: 'starter', price: 49, features: ['50 content pieces/mo', '5 video clips', 'Email support'] },
    { name: 'growth', price: 149, features: ['Unlimited content', '20 video clips', 'Priority support', 'CRM + Nurture'], popular: true },
    { name: 'scale', price: 299, features: ['Everything in Growth', 'Unlimited video', 'Dedicated agent team', 'Custom workflows'] },
  ];

  return (
    <div className="space-y-4">
      <p className="text-sm text-zinc-400">
        Current plan: <span className="font-medium text-zinc-200 capitalize">{sub?.plan || sub?.tier || 'Free'}</span>
      </p>
      <div className="grid gap-3 md:grid-cols-3">
        {plans.map((plan) => (
          <div key={plan.name} className={`glass-panel rounded-xl p-5 space-y-3 ${plan.popular ? 'border-indigo-500/30' : ''}`}>
            {plan.popular && <span className="text-[10px] font-medium text-indigo-400 bg-indigo-500/15 px-2 py-0.5 rounded-full">Most Popular</span>}
            <h4 className="text-sm font-heading font-bold text-zinc-200 capitalize">{plan.name}</h4>
            <p className="text-2xl font-bold text-zinc-100">${plan.price}<span className="text-xs text-zinc-500">/mo</span></p>
            <ul className="space-y-1">
              {plan.features.map((f) => (
                <li key={f} className="flex items-center gap-1.5 text-xs text-zinc-400">
                  <Check size={10} className="text-emerald-400" /> {f}
                </li>
              ))}
            </ul>
            <button className={`w-full py-2 rounded-lg text-sm font-medium transition-colors ${plan.popular ? 'bg-indigo-500 text-white hover:bg-indigo-600' : 'bg-white/5 text-zinc-300 hover:bg-white/10'}`}>
              {sub?.plan === plan.name ? 'Current Plan' : 'Upgrade'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ── Knowledge Base Tab ── */
function KnowledgeTab() {
  const [dragging, setDragging] = useState(false);
  const [documents, setDocuments] = useState([]);

  const handleDrop = async (e) => {
    e.preventDefault();
    setDragging(false);
    const files = Array.from(e.dataTransfer?.files || []);
    for (const file of files) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        await api.identity.uploadDocument(formData);
        setDocuments((prev) => [...prev, { name: file.name, size: file.size, uploaded: new Date().toISOString() }]);
        toast.success(`${file.name} uploaded!`);
      } catch (err) { toast.error(err.message); }
    }
  };

  return (
    <div className="space-y-4">
      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${dragging ? 'border-indigo-500/50 bg-indigo-500/5' : 'border-white/[0.06]'}`}
      >
        <Upload size={28} className="mx-auto text-zinc-600 mb-2" strokeWidth={1.5} />
        <p className="text-sm text-zinc-400">Drag & drop documents here</p>
        <p className="text-xs text-zinc-600 mt-1">PDF, TXT, DOCX, CSV — up to 10MB</p>
        <label className="mt-3 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-white/5 text-sm text-zinc-300 hover:bg-white/10 cursor-pointer transition-colors">
          <Upload size={14} /> Browse files
          <input type="file" className="hidden" multiple onChange={(e) => handleDrop({ preventDefault: () => {}, dataTransfer: { files: e.target.files } })} />
        </label>
      </div>

      {/* Document list */}
      {documents.length > 0 && (
        <div className="glass-panel rounded-xl divide-y divide-white/[0.03]">
          {documents.map((doc, i) => (
            <div key={i} className="flex items-center gap-3 px-4 py-3">
              <BookOpen size={14} className="text-zinc-500" strokeWidth={1.5} />
              <span className="flex-1 text-sm text-zinc-300 truncate">{doc.name}</span>
              <span className="text-xs text-zinc-600">{(doc.size / 1024).toFixed(0)} KB</span>
              <button className="p-1 text-zinc-600 hover:text-red-400 transition-colors">
                <Trash2 size={14} strokeWidth={1.5} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

/* ── Preferences Tab ── */
function PreferencesTab() {
  const { theme, setTheme } = useTheme();
  const [notifications, setNotifications] = useState(true);
  const [autoApprove, setAutoApprove] = useState(false);

  return (
    <div className="space-y-4">
      <div className="glass-panel rounded-xl p-4 flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-zinc-200">Theme</p>
          <p className="text-xs text-zinc-500">Choose your preferred color scheme</p>
        </div>
        <div className="flex items-center gap-1 p-1 rounded-xl bg-white/[0.03] border border-white/[0.06]">
          {['light', 'system', 'dark'].map((t) => (
            <button
              key={t}
              onClick={() => setTheme(t)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors capitalize ${theme === t ? 'bg-white/[0.08] text-zinc-200' : 'text-zinc-500'}`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <div className="glass-panel rounded-xl p-4 flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-zinc-200">Notifications</p>
          <p className="text-xs text-zinc-500">Receive in-app notifications for agent activity</p>
        </div>
        <button onClick={() => setNotifications(!notifications)} className="text-zinc-400">
          {notifications ? <ToggleRight size={24} className="text-indigo-400" /> : <ToggleLeft size={24} />}
        </button>
      </div>

      <div className="glass-panel rounded-xl p-4 flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-zinc-200">Auto-approve low-risk content</p>
          <p className="text-xs text-zinc-500">Content scoring above 90% will be auto-approved</p>
        </div>
        <button onClick={() => setAutoApprove(!autoApprove)} className="text-zinc-400">
          {autoApprove ? <ToggleRight size={24} className="text-emerald-400" /> : <ToggleLeft size={24} />}
        </button>
      </div>
    </div>
  );
}

/* ── Admin Tab ── */
function AdminTab() {
  return (
    <div className="glass-panel rounded-xl p-8 text-center space-y-2">
      <Shield size={28} className="mx-auto text-zinc-600" strokeWidth={1.5} />
      <p className="text-sm text-zinc-500">Admin features coming soon.</p>
      <p className="text-xs text-zinc-600">Waitlist management, beta access, and user administration.</p>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Main Settings Page
   ═══════════════════════════════════════════ */
export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile');

  const tabContent = {
    profile: <ProfileTab />,
    integrations: <IntegrationsTab />,
    subscription: <SubscriptionTab />,
    knowledge: <KnowledgeTab />,
    preferences: <PreferencesTab />,
    admin: <AdminTab />,
  };

  return (
    <div className="p-4 md:p-6 max-w-5xl mx-auto">
      <h1 className="text-lg font-heading font-bold text-zinc-200 mb-4">Settings</h1>

      <div className="flex flex-col md:flex-row gap-4">
        {/* Tab Nav */}
        <nav className="flex md:flex-col gap-1 overflow-x-auto md:overflow-visible md:w-48 flex-shrink-0">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${activeTab === tab.key ? 'bg-white/[0.08] text-zinc-200' : 'text-zinc-500 hover:text-zinc-300 hover:bg-white/[0.03]'}`}
            >
              <tab.icon size={16} strokeWidth={1.5} />
              {tab.label}
            </button>
          ))}
        </nav>

        {/* Tab Content */}
        <div className="flex-1 min-w-0">
          {tabContent[activeTab]}
        </div>
      </div>
    </div>
  );
}
