/**
 * Guild-AI — Comprehensive API Client
 * Covers all Phase 1 + Phase 2 backend endpoints.
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001';

/* ─── Token getter (set by AuthContext on mount) ─── */
let _getToken = () => Promise.resolve(null);
export function setTokenGetter(fn) {
  _getToken = fn;
}

/* ─── Authenticated fetch helper ─── */
async function authFetch(url, options = {}) {
  const token = await _getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };
  // Don't set Content-Type for FormData (browser sets boundary automatically)
  if (options.body instanceof FormData) {
    delete headers['Content-Type'];
  }
  const res = await fetch(`${API_BASE}${url}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `API ${res.status}: ${res.statusText}`);
  }
  return res.json();
}

/* ─── Public (no-auth) fetch ─── */
async function publicFetch(url) {
  const res = await fetch(`${API_BASE}${url}`);
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

/* ═══════════════════════════════════════════════
   API Namespace
   ═══════════════════════════════════════════════ */

export const api = {
  // ── Auth ──
  auth: {
    register: (data) =>
      authFetch('/api/auth/register', { method: 'POST', body: JSON.stringify(data) }),
    verify: () =>
      authFetch('/api/auth/verify', { method: 'POST' }),
    me: () =>
      authFetch('/api/auth/me'),
  },

  // ── Onboarding ──
  onboarding: {
    chat: (message) =>
      authFetch('/api/onboarding/chat', { method: 'POST', body: JSON.stringify({ message }) }),
    status: () =>
      authFetch('/api/onboarding/status'),
  },

  // ── Content Pipeline ──
  content: {
    generate: (params) =>
      authFetch('/api/content/generate', { method: 'POST', body: JSON.stringify(params) }),
    queue: () =>
      authFetch('/api/content/queue'),
    approve: (id) =>
      authFetch(`/api/content/${id}/approve`, { method: 'POST' }),
    reject: (id, feedback) =>
      authFetch(`/api/content/${id}/reject`, { method: 'POST', body: JSON.stringify({ feedback }) }),
    edit: (id, edits) =>
      authFetch(`/api/content/${id}/edit`, { method: 'PUT', body: JSON.stringify(edits) }),
    bulkApprove: (ids) =>
      authFetch('/api/content/bulk-approve', { method: 'POST', body: JSON.stringify({ content_ids: ids }) }),
    published: () =>
      authFetch('/api/content/published'),
    performance: () =>
      authFetch('/api/content/performance'),
    regenerate: (id, feedback) =>
      authFetch(`/api/content/${id}/regenerate`, { method: 'POST', body: JSON.stringify({ feedback }) }),
  },

  // ── CRM ──
  crm: {
    contacts: (filters = {}) =>
      authFetch(`/api/crm/contacts?${new URLSearchParams(filters)}`),
    contact: (id) =>
      authFetch(`/api/crm/contacts/${id}`),
    createContact: (data) =>
      authFetch('/api/crm/contacts', { method: 'POST', body: JSON.stringify(data) }),
    updateContact: (id, data) =>
      authFetch(`/api/crm/contacts/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    pipeline: () =>
      authFetch('/api/crm/pipeline'),
    moveStage: (id, stage) =>
      authFetch(`/api/crm/contacts/${id}/stage`, { method: 'POST', body: JSON.stringify({ stage }) }),
    newLeads: () =>
      authFetch('/api/crm/leads/new'),
    captureEngagement: (data) =>
      authFetch('/api/crm/capture/engagement', { method: 'POST', body: JSON.stringify(data) }),
  },

  // ── Calendar ──
  calendar: {
    events: (start, end) =>
      authFetch(`/api/calendar/events?start=${start}&end=${end}`),
    addEvent: (data) =>
      authFetch('/api/calendar/events', { method: 'POST', body: JSON.stringify(data) }),
    dailyBrief: () =>
      authFetch('/api/calendar/daily-brief'),
    sync: () =>
      authFetch('/api/calendar/sync', { method: 'POST' }),
    suggestTime: (params) =>
      authFetch('/api/calendar/suggest-time', { method: 'POST', body: JSON.stringify(params) }),
  },

  // ── Goals ──
  goals: {
    create: (data) =>
      authFetch('/api/goals/', { method: 'POST', body: JSON.stringify(data) }),
    list: () =>
      authFetch('/api/goals/'),
    get: (id) =>
      authFetch(`/api/goals/${id}`),
    trackProgress: (id) =>
      authFetch(`/api/goals/${id}/progress`, { method: 'POST' }),
    recordMilestone: (id, data) =>
      authFetch(`/api/goals/${id}/milestones`, { method: 'POST', body: JSON.stringify(data) }),
    repeat: (id, data) =>
      authFetch(`/api/goals/${id}/repeat`, { method: 'POST', body: JSON.stringify(data) }),
  },

  // ── Agents ──
  agents: {
    list: () =>
      authFetch('/api/v1/agents/'),
    run: (name, input, context = {}) =>
      authFetch(`/api/v1/agents/${name}/run`, {
        method: 'POST',
        body: JSON.stringify({ input_data: input, context }),
      }),
    events: () =>
      authFetch('/api/v1/agents/events'),
  },

  // ── Identity ──
  identity: {
    get: () =>
      authFetch('/api/v1/identity/'),
    update: (data) =>
      authFetch('/api/v1/identity/', { method: 'POST', body: JSON.stringify(data) }),
    uploadDocument: (formData) =>
      authFetch('/api/v1/identity/document', { method: 'POST', body: formData }),
  },

  // ── Integrations ──
  integrations: {
    list: () =>
      authFetch('/api/v1/integrations/'),
    connect: (platform, config) =>
      authFetch('/api/v1/integrations/connect', { method: 'POST', body: JSON.stringify({ platform, config }) }),
    disconnect: (platform) =>
      authFetch(`/api/v1/integrations/${platform}`, { method: 'DELETE' }),
    test: (platform) =>
      authFetch(`/api/v1/integrations/test/${platform}`, { method: 'POST' }),
  },

  // ── Subscription ──
  subscription: {
    initialize: (plan) =>
      authFetch('/api/subscription/initialize', { method: 'POST', body: JSON.stringify({ plan }) }),
    status: () =>
      authFetch('/api/subscription/status'),
  },

  // ── Workflows ──
  workflows: {
    list: () =>
      authFetch('/api/v1/workflows/'),
    execute: (templateName, params = {}) =>
      authFetch('/api/v1/workflows/execute', {
        method: 'POST',
        body: JSON.stringify({ template_name: templateName, params }),
      }),
    approve: (workflowId, stepName) =>
      authFetch(`/api/v1/workflows/${workflowId}/approve`, {
        method: 'POST',
        body: JSON.stringify({ step_name: stepName, approved: true }),
      }),
  },

  // ── Dashboard ──
  dashboard: {
    snapshot: () =>
      authFetch('/api/v1/dashboard/snapshot'),
  },

  // ── Health ──
  health: () => publicFetch('/health'),
};

/* Backwards-compat exports for existing code */
export const agentAPI = {
  listAgents: () => api.agents.list(),
  runAgent: (name, input, ctx) => api.agents.run(name, input, ctx),
};

export const healthAPI = {
  checkHealth: () => api.health(),
};
