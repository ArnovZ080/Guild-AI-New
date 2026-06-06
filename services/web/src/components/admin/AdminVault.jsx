import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Database, UploadCloud, Search, Trash2, Power, FileText, X } from 'lucide-react';
import { toast } from 'react-toastify';
import { api } from '../../services/api';

export default function AdminVault() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showUpload, setShowUpload] = useState(false);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const res = await api.admin.vault.list({ search });
      setDocuments(res);
    } catch (err) {
      toast.error('Failed to load global knowledge');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [search]);

  const handleToggle = async (id) => {
    try {
      await api.admin.vault.toggle(id);
      fetchDocuments();
      toast.success('Document status updated');
    } catch (err) {
      toast.error('Failed to toggle document');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Permanently delete this knowledge from the global vault?')) return;
    try {
      await api.admin.vault.delete(id);
      fetchDocuments();
      toast.success('Document deleted');
    } catch (err) {
      toast.error('Failed to delete document');
    }
  };

  return (
    <div className="flex flex-col h-full bg-surface-base">
      <header className="px-8 py-6 border-b border-white/[0.06] flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400">
            <Database size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold text-zinc-100">Global Knowledge Vault</h1>
            <p className="text-sm text-zinc-400">Manage foundational intelligence injected into all agents.</p>
          </div>
        </div>
        <button
          onClick={() => setShowUpload(true)}
          className="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg flex items-center gap-2 font-medium transition-colors"
        >
          <UploadCloud size={18} />
          Upload Knowledge
        </button>
      </header>

      <div className="flex-1 overflow-auto p-8">
        <div className="max-w-5xl mx-auto space-y-6">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500" size={18} />
            <input
              type="text"
              placeholder="Search global knowledge..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-surface-raised border border-white/[0.06] rounded-xl pl-12 pr-4 py-3 text-zinc-100 placeholder-zinc-500 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 outline-none transition-all"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {loading ? (
              <div className="col-span-full text-center py-12 text-zinc-500">Loading...</div>
            ) : documents.length === 0 ? (
              <div className="col-span-full text-center py-12 text-zinc-500 bg-surface-raised/50 rounded-xl border border-white/[0.02]">
                No global knowledge found.
              </div>
            ) : (
              documents.map((doc) => (
                <div key={doc.id} className="bg-surface-raised border border-white/[0.06] rounded-xl p-5 hover:border-white/[0.12] transition-colors group relative overflow-hidden">
                  <div className={`absolute top-0 left-0 w-full h-1 ${doc.is_active ? 'bg-emerald-500' : 'bg-zinc-600'}`} />
                  <div className="flex justify-between items-start mb-4">
                    <div className="p-2 bg-white/5 rounded-lg text-zinc-400">
                      <FileText size={20} />
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleToggle(doc.id)}
                        className={`p-1.5 rounded-md transition-colors ${doc.is_active ? 'text-emerald-400 hover:bg-emerald-400/10' : 'text-zinc-500 hover:bg-white/5'}`}
                        title={doc.is_active ? 'Deactivate' : 'Activate'}
                      >
                        <Power size={16} />
                      </button>
                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="p-1.5 rounded-md text-red-400 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-400/10"
                        title="Delete"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                  <h3 className="font-semibold text-zinc-100 mb-1 truncate" title={doc.title}>{doc.title}</h3>
                  <p className="text-xs text-zinc-500 mb-4">{doc.category} • {doc.chunk_count} chunks</p>
                  {doc.description && <p className="text-sm text-zinc-400 line-clamp-2">{doc.description}</p>}
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      <AnimatePresence>
        {showUpload && <UploadModal onClose={() => setShowUpload(false)} onComplete={fetchDocuments} />}
      </AnimatePresence>
    </div>
  );
}

function UploadModal({ onClose, onComplete }) {
  const [form, setForm] = useState({ title: '', category: 'Marketing', content: '', description: '' });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title || !form.content) {
      toast.error('Title and content are required');
      return;
    }
    
    setIsSubmitting(true);
    try {
      await api.admin.vault.upload({
        title: form.title,
        filename: form.title,
        content: form.content,
        category: form.category,
        description: form.description,
      });
      toast.success('Knowledge ingested and embedded globally');
      onComplete();
      onClose();
    } catch (err) {
      toast.error(err.message || 'Failed to upload knowledge');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    if (!file.name.endsWith('.txt') && !file.name.endsWith('.md')) {
      toast.error('Only .txt and .md files are supported for now');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      setForm(f => ({
        ...f,
        title: file.name,
        content: event.target.result
      }));
    };
    reader.readAsText(file);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />
      
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        className="relative w-full max-w-2xl bg-surface-raised border border-white/[0.08] rounded-2xl shadow-2xl flex flex-col max-h-[90vh]"
      >
        <div className="p-6 border-b border-white/[0.06] flex justify-between items-center">
          <h2 className="text-xl font-bold text-zinc-100">Upload Knowledge</h2>
          <button onClick={onClose} className="p-2 text-zinc-400 hover:text-white rounded-lg hover:bg-white/5">
            <X size={20} />
          </button>
        </div>

        <div className="p-6 overflow-y-auto">
          <form id="upload-form" onSubmit={handleSubmit} className="space-y-5">
            
            <div className="p-6 border border-dashed border-white/[0.12] rounded-xl text-center bg-white/[0.02] hover:bg-white/[0.04] transition-colors cursor-pointer relative">
              <input 
                type="file" 
                accept=".txt,.md" 
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <UploadCloud className="mx-auto text-zinc-500 mb-2" size={32} />
              <p className="text-zinc-300 font-medium">Click or drag a .txt or .md file to upload</p>
              <p className="text-xs text-zinc-500 mt-1">File contents will be pasted below</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-zinc-300">Title</label>
                <input
                  type="text"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  className="w-full bg-black/20 border border-white/[0.06] rounded-xl px-4 py-2.5 text-zinc-100 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 outline-none"
                  placeholder="E.g., High Converting Emails"
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-zinc-300">Category</label>
                <select
                  value={form.category}
                  onChange={(e) => setForm({ ...form, category: e.target.value })}
                  className="w-full bg-black/20 border border-white/[0.06] rounded-xl px-4 py-2.5 text-zinc-100 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 outline-none"
                >
                  <option>Marketing</option>
                  <option>Sales</option>
                  <option>Copywriting</option>
                  <option>Strategy</option>
                  <option>Advertising</option>
                </select>
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-sm font-medium text-zinc-300">Raw Content</label>
              <textarea
                value={form.content}
                onChange={(e) => setForm({ ...form, content: e.target.value })}
                rows={6}
                className="w-full bg-black/20 border border-white/[0.06] rounded-xl px-4 py-3 text-zinc-100 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 outline-none font-mono text-sm"
                placeholder="Paste raw text or markdown here..."
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-sm font-medium text-zinc-300">Description (Optional)</label>
              <input
                type="text"
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                className="w-full bg-black/20 border border-white/[0.06] rounded-xl px-4 py-2.5 text-zinc-100 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/50 outline-none"
              />
            </div>
          </form>
        </div>

        <div className="p-6 border-t border-white/[0.06] flex justify-end gap-3 bg-surface-base rounded-b-2xl">
          <button
            type="button"
            onClick={onClose}
            className="px-5 py-2.5 rounded-lg text-zinc-400 hover:text-zinc-200 font-medium transition-colors"
          >
            Cancel
          </button>
          <button
            form="upload-form"
            type="submit"
            disabled={isSubmitting}
            className="px-6 py-2.5 bg-indigo-500 hover:bg-indigo-600 disabled:opacity-50 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
          >
            {isSubmitting && <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />}
            Ingest Knowledge
          </button>
        </div>
      </motion.div>
    </div>
  );
}
