/**
 * Guild-AI - Settings Page (Unified)
 *
 * 7 tabs: Business Profile | Integrations | Subscription | Knowledge Base | Media Library | Preferences | Admin
 */
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  User, Link2, CreditCard, BookOpen, Sliders, Shield, Image as ImageIcon,
  Loader2, Check, Upload, Trash2, ExternalLink, Search, X, Tag,
  Bell, BellOff, ToggleLeft, ToggleRight, Sparkles, Palette, Move,
} from 'lucide-react';
import ZARPrice from '../ui/ZARPrice';
import { api } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';

import { toast } from 'react-toastify';

/* ─── Tab config ─── */
const TABS = [
  { key: 'profile', label: 'Business Profile', icon: User },
  { key: 'integrations', label: 'Integrations', icon: Link2 },
  { key: 'subscription', label: 'Subscription', icon: CreditCard },
  { key: 'knowledge', label: 'Knowledge Base', icon: BookOpen },
  { key: 'media', label: 'Media Library', icon: ImageIcon },
  { key: 'preferences', label: 'Preferences', icon: Sliders },
  { key: 'admin', label: 'Admin', icon: Shield },
];

const CATEGORIES = ['All', 'Products', 'Team', 'Lifestyle', 'Logo & Branding', 'Other'];

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
            <label className="text-xs text-zinc-400 mb-1 block">{label}</label>
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
        <div className="glass-panel rounded-xl p-8 text-center text-sm text-zinc-400">
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
                <p className="text-xs text-zinc-400">{c.connected ? 'Connected' : 'Not connected'}</p>
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
            {plan.popular && <span className="text-xs font-medium text-indigo-400 bg-indigo-500/15 px-2 py-0.5 rounded-full">Most Popular</span>}
            <h4 className="text-sm font-heading font-bold text-zinc-200 capitalize">{plan.name}</h4>
            <p className="text-2xl font-bold text-zinc-100">${plan.price}<span className="text-xs text-zinc-400">/mo</span></p>
            <ZARPrice usd={plan.price} className="text-xs" />
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
        <p className="text-xs text-zinc-600 mt-1">PDF, TXT, DOCX, CSV - up to 10MB</p>
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
              <BookOpen size={14} className="text-zinc-400" strokeWidth={1.5} />
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

/* ── Media Library Tab ── */
function MediaLibraryTab() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [activeCategory, setActiveCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const fileInputRef = useRef(null);

  // Load assets
  const loadAssets = useCallback(async () => {
    try {
      const params = {};
      if (activeCategory !== 'All') {
        params.category = activeCategory.toLowerCase().replace('& branding', '').replace('logo ', 'logo').trim();
      }
      const data = await api.media.list(params);
      setAssets(data?.assets || []);
    } catch { /* ok */ }
    setLoading(false);
  }, [activeCategory]);

  useEffect(() => { loadAssets(); }, [loadAssets]);

  // Upload handler
  const handleUpload = async (files) => {
    if (!files || files.length === 0) return;
    setUploading(true);

    const formData = new FormData();
    Array.from(files).forEach((f) => formData.append('files', f));

    if (activeCategory !== 'All') {
      formData.append('category', activeCategory.toLowerCase());
    }

    try {
      const result = await api.media.upload(formData);
      const uploaded = result?.uploaded || [];
      const successes = uploaded.filter((u) => !u.error);
      const errors = uploaded.filter((u) => u.error);

      if (successes.length) toast.success(`${successes.length} file(s) uploaded!`);
      errors.forEach((e) => toast.error(`${e.filename}: ${e.error}`));

      await loadAssets();
    } catch (err) {
      toast.error(err.message);
    }
    setUploading(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleUpload(e.dataTransfer?.files);
  };

  // Search
  const handleSearch = async () => {
    if (!searchQuery.trim()) { setSearchResults(null); return; }
    try {
      const data = await api.media.search(searchQuery);
      setSearchResults(data?.results || []);
    } catch { setSearchResults([]); }
  };

  // Delete
  const handleDelete = async (id) => {
    try {
      await api.media.delete(id);
      toast.success('Asset deleted');
      setSelectedAsset(null);
      await loadAssets();
    } catch (err) { toast.error(err.message); }
  };

  // Update
  const handleUpdate = async (id, updates) => {
    try {
      await api.media.update(id, updates);
      toast.success('Asset updated');
      await loadAssets();
    } catch (err) { toast.error(err.message); }
  };

  const displayAssets = searchResults !== null ? searchResults : assets;

  return (
    <div className="space-y-4">
      {/* Upload area */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-6 text-center transition-all ${dragging ? 'border-indigo-500/50 bg-indigo-500/5 scale-[1.01]' : 'border-white/[0.06] hover:border-white/[0.12]'}`}
      >
        {uploading ? (
          <div className="flex flex-col items-center gap-2">
            <Loader2 size={28} className="animate-spin text-indigo-400" />
            <p className="text-sm text-zinc-400">Processing uploads...</p>
          </div>
        ) : (
          <>
            <div className="w-12 h-12 mx-auto mb-2 rounded-xl bg-gradient-to-br from-indigo-500/20 to-violet-500/20 flex items-center justify-center">
              <Upload size={22} className="text-indigo-400" strokeWidth={1.5} />
            </div>
            <p className="text-sm text-zinc-300 font-medium">Drop images & videos here</p>
            <p className="text-xs text-zinc-500 mt-1">JPEG, PNG, WebP, GIF, MP4 — up to 25MB each</p>
            <label className="mt-3 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-500/10 text-sm text-indigo-400 hover:bg-indigo-500/20 cursor-pointer transition-colors font-medium">
              <Upload size={14} /> Browse files
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                multiple
                accept="image/*,video/*"
                onChange={(e) => handleUpload(e.target.files)}
              />
            </label>
          </>
        )}
      </div>

      {/* Search bar */}
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
          <input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Search media... (e.g. 'candle on wooden table')"
            className="w-full pl-9 pr-3 py-2 rounded-lg bg-white/5 border border-white/[0.06] text-sm text-zinc-200 placeholder-zinc-600 outline-none focus:border-indigo-500/30"
          />
          {searchResults !== null && (
            <button
              onClick={() => { setSearchQuery(''); setSearchResults(null); }}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-zinc-500 hover:text-zinc-300"
            >
              <X size={12} />
            </button>
          )}
        </div>
        <button
          onClick={handleSearch}
          className="px-4 py-2 rounded-lg bg-indigo-500/10 text-indigo-400 text-sm font-medium hover:bg-indigo-500/20 transition-colors"
        >
          Search
        </button>
      </div>

      {/* Category filter */}
      <div className="flex gap-1.5 overflow-x-auto pb-1">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => { setActiveCategory(cat); setSearchResults(null); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
              activeCategory === cat
                ? 'bg-indigo-500/15 text-indigo-400 border border-indigo-500/20'
                : 'bg-white/5 text-zinc-400 border border-transparent hover:bg-white/[0.08]'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Asset grid */}
      {loading ? (
        <div className="flex justify-center py-12">
          <Loader2 size={20} className="animate-spin text-indigo-400" />
        </div>
      ) : displayAssets.length === 0 ? (
        <div className="glass-panel rounded-xl p-12 text-center">
          <ImageIcon size={32} className="mx-auto text-zinc-700 mb-3" strokeWidth={1.5} />
          <p className="text-sm text-zinc-400">
            {searchResults !== null ? 'No matching assets found' : 'No media uploaded yet'}
          </p>
          <p className="text-xs text-zinc-600 mt-1">Upload images and videos to build your brand library</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {displayAssets.map((asset) => (
            <motion.div
              key={asset.id}
              layoutId={asset.id}
              onClick={() => setSelectedAsset(asset)}
              className="glass-panel rounded-xl overflow-hidden cursor-pointer group hover:border-indigo-500/20 transition-colors"
            >
              {/* Thumbnail */}
              <div className="relative aspect-[4/3] bg-zinc-900/50 overflow-hidden">
                <img
                  src={asset.thumbnail_url || asset.storage_url}
                  alt={asset.ai_description || asset.filename}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  loading="lazy"
                />
                {/* Category badge */}
                {asset.category && (
                  <span className="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-black/60 backdrop-blur-sm text-xs text-zinc-300 capitalize">
                    {asset.category}
                  </span>
                )}
                {/* Score badge (search results) */}
                {asset.score !== undefined && (
                  <span className="absolute top-2 right-2 px-2 py-0.5 rounded-md bg-indigo-500/80 text-xs text-white font-medium">
                    {(asset.score * 100).toFixed(0)}%
                  </span>
                )}
                {/* Delete button */}
                <button
                  onClick={(e) => { e.stopPropagation(); handleDelete(asset.id); }}
                  className="absolute top-2 right-2 p-1.5 rounded-lg bg-black/50 text-zinc-400 opacity-0 group-hover:opacity-100 hover:text-red-400 hover:bg-red-500/20 transition-all"
                >
                  <Trash2 size={12} />
                </button>
              </div>

              {/* Info */}
              <div className="p-3 space-y-1">
                <p className="text-xs font-medium text-zinc-300 truncate">{asset.filename}</p>
                {asset.ai_description && (
                  <p className="text-xs text-zinc-500 line-clamp-2">{asset.ai_description}</p>
                )}
                {asset.ai_tags?.length > 0 && (
                  <div className="flex flex-wrap gap-1 pt-1">
                    {asset.ai_tags.slice(0, 3).map((tag) => (
                      <span key={tag} className="px-1.5 py-0.5 rounded bg-white/5 text-[10px] text-zinc-500">
                        {tag}
                      </span>
                    ))}
                    {asset.ai_tags.length > 3 && (
                      <span className="text-[10px] text-zinc-600">+{asset.ai_tags.length - 3}</span>
                    )}
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Asset Detail Modal */}
      <AnimatePresence>
        {selectedAsset && (
          <AssetDetailModal
            asset={selectedAsset}
            onClose={() => setSelectedAsset(null)}
            onDelete={handleDelete}
            onUpdate={handleUpdate}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

/* ── Asset Detail Modal ── */
function AssetDetailModal({ asset, onClose, onDelete, onUpdate }) {
  const [category, setCategory] = useState(asset.category || '');
  const [altText, setAltText] = useState(asset.alt_text || '');
  const [userTags, setUserTags] = useState(asset.user_tags || []);
  const [newTag, setNewTag] = useState('');

  const addTag = () => {
    if (newTag.trim() && !userTags.includes(newTag.trim())) {
      const updated = [...userTags, newTag.trim()];
      setUserTags(updated);
      setNewTag('');
      onUpdate(asset.id, { user_tags: updated });
    }
  };

  const removeTag = (tag) => {
    const updated = userTags.filter((t) => t !== tag);
    setUserTags(updated);
    onUpdate(asset.id, { user_tags: updated });
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
        className="glass-panel rounded-2xl max-w-3xl w-full max-h-[85vh] overflow-y-auto"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/[0.06]">
          <h3 className="text-sm font-heading font-bold text-zinc-200 truncate">{asset.filename}</h3>
          <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-white/5 text-zinc-400">
            <X size={16} />
          </button>
        </div>

        <div className="flex flex-col md:flex-row">
          {/* Image */}
          <div className="md:w-1/2 p-4">
            <img
              src={asset.storage_url}
              alt={asset.ai_description || asset.filename}
              className="w-full rounded-xl object-contain max-h-[400px] bg-zinc-900/50"
            />
            {/* Dominant colours */}
            {asset.ai_colors?.length > 0 && (
              <div className="flex items-center gap-2 mt-3">
                <Palette size={12} className="text-zinc-500" />
                <div className="flex gap-1.5">
                  {asset.ai_colors.map((color) => (
                    <div
                      key={color}
                      className="w-6 h-6 rounded-md border border-white/10 cursor-pointer"
                      style={{ backgroundColor: color }}
                      title={color}
                    />
                  ))}
                </div>
              </div>
            )}
            {/* Dimensions */}
            {asset.width && asset.height && (
              <p className="text-xs text-zinc-600 mt-2">
                {asset.width} × {asset.height} px · {asset.file_size ? `${(asset.file_size / 1024).toFixed(0)} KB` : ''}
              </p>
            )}
          </div>

          {/* Details */}
          <div className="md:w-1/2 p-4 space-y-4 border-t md:border-t-0 md:border-l border-white/[0.06]">
            {/* AI Description */}
            <div>
              <label className="text-xs text-zinc-400 mb-1 block">AI Description</label>
              <p className="text-sm text-zinc-300 bg-white/[0.03] rounded-lg p-3">
                {asset.ai_description || 'No description generated'}
              </p>
            </div>

            {/* Category */}
            <div>
              <label className="text-xs text-zinc-400 mb-1 block">Category</label>
              <select
                value={category}
                onChange={(e) => { setCategory(e.target.value); onUpdate(asset.id, { category: e.target.value }); }}
                className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/[0.06] text-sm text-zinc-200 outline-none"
              >
                <option value="">Uncategorized</option>
                <option value="products">Products</option>
                <option value="team">Team</option>
                <option value="lifestyle">Lifestyle</option>
                <option value="logo">Logo & Branding</option>
                <option value="other">Other</option>
              </select>
            </div>

            {/* Alt text */}
            <div>
              <label className="text-xs text-zinc-400 mb-1 block">Alt Text</label>
              <input
                value={altText}
                onChange={(e) => setAltText(e.target.value)}
                onBlur={() => onUpdate(asset.id, { alt_text: altText })}
                placeholder="Describe this image for accessibility"
                className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/[0.06] text-sm text-zinc-200 placeholder-zinc-600 outline-none focus:border-indigo-500/30"
              />
            </div>

            {/* AI Tags */}
            {asset.ai_tags?.length > 0 && (
              <div>
                <label className="text-xs text-zinc-400 mb-1 block">AI Tags</label>
                <div className="flex flex-wrap gap-1.5">
                  {asset.ai_tags.map((tag) => (
                    <span key={tag} className="px-2 py-1 rounded-md bg-indigo-500/10 text-xs text-indigo-400">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* User Tags */}
            <div>
              <label className="text-xs text-zinc-400 mb-1 block">Your Tags</label>
              <div className="flex flex-wrap gap-1.5 mb-2">
                {userTags.map((tag) => (
                  <span key={tag} className="px-2 py-1 rounded-md bg-emerald-500/10 text-xs text-emerald-400 flex items-center gap-1">
                    {tag}
                    <button onClick={() => removeTag(tag)} className="hover:text-red-400">
                      <X size={10} />
                    </button>
                  </span>
                ))}
              </div>
              <div className="flex gap-2">
                <input
                  value={newTag}
                  onChange={(e) => setNewTag(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && addTag()}
                  placeholder="Add tag..."
                  className="flex-1 px-3 py-1.5 rounded-lg bg-white/5 border border-white/[0.06] text-xs text-zinc-200 placeholder-zinc-600 outline-none"
                />
                <button onClick={addTag} className="px-3 py-1.5 rounded-lg bg-white/5 text-xs text-zinc-300 hover:bg-white/10">
                  Add
                </button>
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2 pt-2">
              <button
                className="flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-500/10 text-indigo-400 text-xs font-medium hover:bg-indigo-500/20 transition-colors"
              >
                <Sparkles size={12} /> Enhance
              </button>
              <button
                onClick={() => onDelete(asset.id)}
                className="flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-red-500/10 text-red-400 text-xs font-medium hover:bg-red-500/20 transition-colors"
              >
                <Trash2 size={12} /> Delete
              </button>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

/* ── Preferences Tab ── */
function PreferencesTab() {
  const [notifications, setNotifications] = useState(true);
  const [autoApprove, setAutoApprove] = useState(false);

  return (
    <div className="space-y-4">
      <div className="glass-panel rounded-xl p-4 flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-zinc-200">Notifications</p>
          <p className="text-xs text-zinc-400">Receive in-app notifications for agent activity</p>
        </div>
        <button onClick={() => setNotifications(!notifications)} className="text-zinc-400">
          {notifications ? <ToggleRight size={24} className="text-indigo-400" /> : <ToggleLeft size={24} />}
        </button>
      </div>

      <div className="glass-panel rounded-xl p-4 flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-zinc-200">Auto-approve low-risk content</p>
          <p className="text-xs text-zinc-400">Content scoring above 90% will be auto-approved</p>
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
      <p className="text-sm text-zinc-400">Admin features coming soon.</p>
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
    media: <MediaLibraryTab />,
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
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${activeTab === tab.key ? 'bg-white/[0.08] text-zinc-200' : 'text-zinc-400 hover:text-zinc-300 hover:bg-white/[0.03]'}`}
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
