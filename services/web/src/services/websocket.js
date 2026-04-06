/**
 * Guild-AI — WebSocket Client
 *
 * Manages a single WebSocket connection to the backend.
 * Dispatches typed events to registered listeners.
 * Supports auto-reconnect with exponential backoff.
 */

const WS_BASE = import.meta.env.VITE_WS_URL || 'ws://localhost:8001';
const MAX_RECONNECT_DELAY = 30_000;

class GuildWebSocket {
  constructor() {
    this.ws = null;
    this.listeners = new Map();
    this._userId = null;
    this._reconnectTimer = null;
    this._reconnectDelay = 1000;
    this._intentionalClose = false;
  }

  /** Connect to the Guild WebSocket for the given user */
  connect(userId) {
    if (this.ws?.readyState === WebSocket.OPEN) return;
    this._userId = userId;
    this._intentionalClose = false;

    try {
      this.ws = new WebSocket(`${WS_BASE}/ws/${userId}`);
    } catch {
      this._scheduleReconnect();
      return;
    }

    this.ws.onopen = () => {
      this._reconnectDelay = 1000; // reset on success
      this._dispatch('_connected', { userId });
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this._dispatch(data.type || data.event_type || '_message', data);
        this._dispatch('*', data); // wildcard
      } catch {
        /* non-JSON payload, ignore */
      }
    };

    this.ws.onclose = () => {
      this._dispatch('_disconnected', {});
      if (!this._intentionalClose) this._scheduleReconnect();
    };

    this.ws.onerror = () => {
      /* onclose will fire after onerror */
    };
  }

  /** Register a listener. Returns an unsubscribe function. */
  on(eventType, callback) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, new Set());
    }
    this.listeners.get(eventType).add(callback);
    return () => this.listeners.get(eventType)?.delete(callback);
  }

  /** Disconnect and stop reconnecting */
  disconnect() {
    this._intentionalClose = true;
    clearTimeout(this._reconnectTimer);
    this.ws?.close();
    this.ws = null;
  }

  /* ── private ── */

  _dispatch(type, data) {
    this.listeners.get(type)?.forEach((cb) => {
      try { cb(data); } catch (e) { console.error('WS listener error:', e); }
    });
  }

  _scheduleReconnect() {
    clearTimeout(this._reconnectTimer);
    this._reconnectTimer = setTimeout(() => {
      if (this._userId) this.connect(this._userId);
    }, this._reconnectDelay);
    this._reconnectDelay = Math.min(this._reconnectDelay * 2, MAX_RECONNECT_DELAY);
  }
}

export const guildWS = new GuildWebSocket();
