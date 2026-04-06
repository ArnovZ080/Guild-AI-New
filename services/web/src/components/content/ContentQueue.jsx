/**
 * Guild-AI — Content Queue + Calendar (Unified View)
 *
 * 3 tabs: Queue | Calendar | Published
 * Queue: Content cards with Judge scores, approve/reject/edit, bulk approve
 * Calendar: Scheduled content + events timeline
 * Published: Performance metrics grid
 */
import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FileText, Calendar as CalendarIcon, BarChart3, Plus, Check, X, Edit3, Eye,
  Instagram, Mail, PenTool, Video, Image, Loader2, ChevronLeft, ChevronRight,
  RefreshCw, CheckCheck, Clock, Sparkles,
} from 'lucide-react';
import { api } from '../../services/api';
import { toast } from 'react-toastify';
import { format, startOfWeek, addDays, addWeeks, subWeeks, isSameDay } from 'date-fns';

/* ─── Content Type Icons ─── */
const typeIcons = {
  social: Instagram,
  email: Mail,
  blog: PenTool,
  video: Video,
  image: Image,
  default: FileText,
};

function getTypeIcon(type) {
  const Icon = typeIcons[type] || typeIcons.default;
  return <Icon size={16} strokeWidth={1.5} />;
}

/* ─── Score Badge ─── */
function ScoreBadge({ label, pass }) {
  return (
    <span className={`inline-flex items-center gap-1 text-[10px] font-medium px-1.5 py-0.5 rounded ${pass ? 'bg-emerald-500/15 text-emerald-400' : 'bg-amber-500/15 text-amber-400'}`}>
      {pass ? <Check size={10} /> : <X size={10} />} {label}
    </span>
  );
}

/* ─── Content Card ─── */
function ContentCard({ item, onApprove, onReject, onEdit, selected, onToggleSelect }) {
  const [expanded, setExpanded] = useState(false);
  const score = item.quality_score || item.score || 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel rounded-xl overflow-hidden"
    >
      <div className="p-4 space-y-3">
        {/* Header */}
        <div className="flex items-start gap-3">
          <label className="flex items-center mt-0.5">
            <input
              type="checkbox"
              checked={selected}
              onChange={onToggleSelect}
              className="w-4 h-4 rounded border-white/10 bg-white/5 text-indigo-500 focus:ring-0"
            />
          </label>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <span className="flex items-center gap-1 text-xs text-zinc-500">
                {getTypeIcon(item.content_type || item.type)}
                {item.platform || 'General'}
              </span>
              <span className={`text-xs font-medium px-1.5 py-0.5 rounded ${score >= 90 ? 'bg-emerald-500/15 text-emerald-400' : score >= 70 ? 'bg-amber-500/15 text-amber-400' : 'bg-red-500/15 text-red-400'}`}>
                {score}%
              </span>
            </div>
            <h3 className="text-sm font-medium text-zinc-200 truncate">{item.title || 'Untitled Content'}</h3>
          </div>
        </div>

        {/* Scores */}
        <div className="flex flex-wrap gap-1.5">
          <ScoreBadge label="Brand" pass={item.brand_check !== false} />
          <ScoreBadge label="ICP" pass={item.icp_check !== false} />
          {item.seo_check != null && <ScoreBadge label="SEO" pass={item.seo_check} />}
        </div>

        {/* Schedule */}
        {item.scheduled_at && (
          <div className="flex items-center gap-1.5 text-xs text-zinc-500">
            <Clock size={12} strokeWidth={1.5} />
            {format(new Date(item.scheduled_at), 'EEE, MMM d · h:mm a')}
          </div>
        )}

        {/* Preview */}
        <AnimatePresence>
          {expanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden"
            >
              <div className="pt-2 border-t border-white/[0.06]">
                <p className="text-xs text-zinc-400 whitespace-pre-wrap">{item.body || item.content || 'No content preview available.'}</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Actions */}
        <div className="flex items-center gap-2 pt-1">
          <button onClick={() => setExpanded(!expanded)} className="flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors">
            <Eye size={12} strokeWidth={1.5} /> {expanded ? 'Collapse' : 'Preview'}
          </button>
          <button onClick={() => onEdit(item)} className="flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors">
            <Edit3 size={12} strokeWidth={1.5} /> Edit
          </button>
          <div className="flex-1" />
          <button onClick={() => onReject(item)} className="flex items-center gap-1 text-xs px-2.5 py-1.5 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-colors">
            <X size={12} strokeWidth={1.5} /> Reject
          </button>
          <button onClick={() => onApprove(item)} className="flex items-center gap-1 text-xs px-2.5 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 transition-colors">
            <Check size={12} strokeWidth={1.5} /> Approve
          </button>
        </div>
      </div>
    </motion.div>
  );
}

/* ─── Generate Modal ─── */
function GenerateModal({ open, onClose }) {
  const [topic, setTopic] = useState('');
  const [contentType, setContentType] = useState('social');
  const [platform, setPlatform] = useState('linkedin');
  const [generating, setGenerating] = useState(false);

  const handleGenerate = async () => {
    if (!topic.trim()) return;
    setGenerating(true);
    try {
      await api.content.generate({ topic, content_type: contentType, platform });
      toast.success('Content generation started!');
      onClose();
    } catch (err) {
      toast.error(err.message);
    } finally {
      setGenerating(false);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="glass-panel rounded-2xl p-6 w-full max-w-md space-y-4"
      >
        <h2 className="text-lg font-heading font-bold text-zinc-200">Generate Content</h2>

        <div className="space-y-3">
          <div>
            <label className="text-xs text-zinc-500 mb-1 block">Topic or brief</label>
            <textarea
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. 5 benefits of soy candles for self-care routines"
              rows={3}
              className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/[0.06] text-sm text-zinc-200 placeholder-zinc-600 outline-none focus:border-indigo-500/30"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-zinc-500 mb-1 block">Type</label>
              <select value={contentType} onChange={(e) => setContentType(e.target.value)} className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/[0.06] text-sm text-zinc-300 outline-none">
                <option value="social">Social Post</option>
                <option value="blog">Blog Article</option>
                <option value="email">Email</option>
                <option value="video">Video Script</option>
                <option value="image">Image</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-zinc-500 mb-1 block">Platform</label>
              <select value={platform} onChange={(e) => setPlatform(e.target.value)} className="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/[0.06] text-sm text-zinc-300 outline-none">
                <option value="linkedin">LinkedIn</option>
                <option value="instagram">Instagram</option>
                <option value="twitter">X (Twitter)</option>
                <option value="facebook">Facebook</option>
                <option value="email">Email</option>
                <option value="blog">Blog</option>
              </select>
            </div>
          </div>

          {/* Quick options */}
          <div className="flex flex-wrap gap-2">
            {["Generate this week's content", "Create a promotional post", "Write a newsletter"].map((q) => (
              <button key={q} onClick={() => setTopic(q)} className="text-[10px] px-2 py-1 rounded-full border border-white/[0.06] text-zinc-500 hover:text-indigo-400 hover:border-indigo-500/30 transition-colors">
                {q}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-2 pt-2">
          <button onClick={onClose} className="flex-1 px-4 py-2 rounded-lg text-sm text-zinc-400 hover:bg-white/5 transition-colors">Cancel</button>
          <button onClick={handleGenerate} disabled={!topic.trim() || generating} className="flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-500 text-white text-sm font-medium hover:bg-indigo-600 disabled:opacity-40 transition-colors">
            {generating ? <Loader2 size={14} className="animate-spin" /> : <Sparkles size={14} />}
            Generate
          </button>
        </div>
      </motion.div>
    </div>
  );
}

/* ─── Week Calendar ─── */
function WeekCalendar({ events }) {
  const [weekStart, setWeekStart] = useState(startOfWeek(new Date(), { weekStartsOn: 1 }));
  const days = Array.from({ length: 7 }, (_, i) => addDays(weekStart, i));

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <button onClick={() => setWeekStart(subWeeks(weekStart, 1))} className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-300 hover:bg-white/5 transition-colors">
          <ChevronLeft size={16} strokeWidth={1.5} />
        </button>
        <h3 className="text-sm font-medium text-zinc-300">{format(weekStart, 'MMM d')} – {format(addDays(weekStart, 6), 'MMM d, yyyy')}</h3>
        <button onClick={() => setWeekStart(addWeeks(weekStart, 1))} className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-300 hover:bg-white/5 transition-colors">
          <ChevronRight size={16} strokeWidth={1.5} />
        </button>
      </div>

      <div className="grid grid-cols-7 gap-1">
        {days.map((day) => {
          const isToday = isSameDay(day, new Date());
          const dayEvents = (events || []).filter((e) => isSameDay(new Date(e.scheduled_at || e.start), day));
          return (
            <div key={day.toISOString()} className={`glass-panel rounded-xl p-2 min-h-[120px] ${isToday ? 'border-indigo-500/30' : ''}`}>
              <p className={`text-xs font-medium mb-1 ${isToday ? 'text-indigo-400' : 'text-zinc-500'}`}>
                {format(day, 'EEE d')}
              </p>
              <div className="space-y-1">
                {dayEvents.map((evt, i) => (
                  <div key={i} className="text-[10px] px-1.5 py-1 rounded bg-indigo-500/10 text-indigo-300 truncate">
                    {evt.title || evt.content_type || 'Event'}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Main Content Queue
   ═══════════════════════════════════════════ */
export default function ContentQueue() {
  const [activeTab, setActiveTab] = useState('queue');
  const [queue, setQueue] = useState([]);
  const [published, setPublished] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(new Set());
  const [showGenerate, setShowGenerate] = useState(false);

  /* ── Fetch data ── */
  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [q, p] = await Promise.allSettled([api.content.queue(), api.content.published()]);
      setQueue(q.status === 'fulfilled' ? (q.value?.items || q.value || []) : []);
      setPublished(p.status === 'fulfilled' ? (p.value?.items || p.value || []) : []);
    } catch { /* empty */ }
    setLoading(false);
  }, []);

  useEffect(() => { loadData(); }, [loadData]);

  /* ── Actions ── */
  const handleApprove = async (item) => {
    try {
      await api.content.approve(item.id);
      setQueue((prev) => prev.filter((c) => c.id !== item.id));
      toast.success('Content approved!');
    } catch (err) { toast.error(err.message); }
  };

  const handleReject = async (item) => {
    try {
      await api.content.reject(item.id, 'Rejected by user');
      setQueue((prev) => prev.filter((c) => c.id !== item.id));
      toast.info('Content rejected');
    } catch (err) { toast.error(err.message); }
  };

  const handleBulkApprove = async () => {
    try {
      await api.content.bulkApprove([...selected]);
      setQueue((prev) => prev.filter((c) => !selected.has(c.id)));
      setSelected(new Set());
      toast.success(`${selected.size} items approved!`);
    } catch (err) { toast.error(err.message); }
  };

  const tabs = [
    { key: 'queue', label: 'Queue', icon: FileText, count: queue.length },
    { key: 'calendar', label: 'Calendar', icon: CalendarIcon },
    { key: 'published', label: 'Published', icon: BarChart3, count: published.length },
  ];

  return (
    <div className="p-4 md:p-6 max-w-6xl mx-auto space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1 p-1 rounded-xl bg-white/[0.02] border border-white/[0.06]">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${activeTab === tab.key ? 'bg-white/[0.08] text-zinc-200' : 'text-zinc-500 hover:text-zinc-300'}`}
            >
              <tab.icon size={14} strokeWidth={1.5} />
              {tab.label}
              {tab.count != null && tab.count > 0 && (
                <span className="min-w-[18px] h-[18px] flex items-center justify-center text-[10px] font-bold rounded-full bg-indigo-500/20 text-indigo-400">{tab.count}</span>
              )}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <button onClick={loadData} className="p-2 rounded-lg text-zinc-500 hover:text-zinc-300 hover:bg-white/5 transition-colors">
            <RefreshCw size={16} strokeWidth={1.5} />
          </button>
          <button onClick={() => setShowGenerate(true)} className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-indigo-500 text-white text-sm font-medium hover:bg-indigo-600 transition-colors">
            <Plus size={14} strokeWidth={1.5} /> Generate
          </button>
        </div>
      </div>

      {/* Bulk actions */}
      {activeTab === 'queue' && selected.size > 0 && (
        <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} className="flex items-center gap-3 glass-panel rounded-xl px-4 py-2">
          <span className="text-xs text-zinc-400">{selected.size} selected</span>
          <button onClick={handleBulkApprove} className="flex items-center gap-1 text-xs px-3 py-1.5 rounded-lg bg-emerald-500/15 text-emerald-400 hover:bg-emerald-500/25 transition-colors">
            <CheckCheck size={12} strokeWidth={1.5} /> Approve All
          </button>
          <button onClick={() => setSelected(new Set())} className="text-xs text-zinc-500 hover:text-zinc-300">Clear</button>
        </motion.div>
      )}

      {/* Tab Content */}
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 size={24} className="animate-spin text-indigo-400" />
        </div>
      ) : (
        <>
          {activeTab === 'queue' && (
            <div className="space-y-3">
              {queue.length === 0 ? (
                <div className="glass-panel rounded-xl p-12 text-center space-y-3">
                  <FileText size={32} className="mx-auto text-zinc-600" strokeWidth={1.5} />
                  <p className="text-sm text-zinc-500">No content in your queue yet.</p>
                  <button onClick={() => setShowGenerate(true)} className="text-sm text-indigo-400 hover:text-indigo-300 transition-colors">
                    Generate your first content →
                  </button>
                </div>
              ) : (
                queue.map((item) => (
                  <ContentCard
                    key={item.id}
                    item={item}
                    onApprove={handleApprove}
                    onReject={handleReject}
                    onEdit={() => {}}
                    selected={selected.has(item.id)}
                    onToggleSelect={() => {
                      const next = new Set(selected);
                      next.has(item.id) ? next.delete(item.id) : next.add(item.id);
                      setSelected(next);
                    }}
                  />
                ))
              )}
            </div>
          )}

          {activeTab === 'calendar' && <WeekCalendar events={[...queue, ...events]} />}

          {activeTab === 'published' && (
            <div className="space-y-3">
              {published.length === 0 ? (
                <div className="glass-panel rounded-xl p-12 text-center space-y-3">
                  <BarChart3 size={32} className="mx-auto text-zinc-600" strokeWidth={1.5} />
                  <p className="text-sm text-zinc-500">No published content yet.</p>
                  <p className="text-xs text-zinc-600">Approve content from the Queue to see it here.</p>
                </div>
              ) : (
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {published.map((item) => (
                    <div key={item.id} className="glass-panel rounded-xl p-4 space-y-2">
                      <div className="flex items-center gap-2 text-xs text-zinc-500">
                        {getTypeIcon(item.content_type || item.type)}
                        {item.platform || 'General'}
                      </div>
                      <h4 className="text-sm font-medium text-zinc-300 truncate">{item.title}</h4>
                      <div className="flex gap-3 text-xs text-zinc-500">
                        {item.engagement && <span>👍 {item.engagement}</span>}
                        {item.reach && <span>👁 {item.reach}</span>}
                        {item.clicks && <span>🔗 {item.clicks}</span>}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </>
      )}

      <GenerateModal open={showGenerate} onClose={() => { setShowGenerate(false); loadData(); }} />
    </div>
  );
}
