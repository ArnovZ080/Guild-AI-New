class AgentActivityService {
    constructor() {
        this.subscribers = [];
        this.events = [];
        this.isRunning = false;
        this.lastEventId = null;
        this.pollInterval = 2000; // 2 seconds
    }

    subscribe(callback) {
        this.subscribers.push(callback);
        // Immediately provide current events
        callback(this.events);

        // Start polling if not already running
        if (!this.isRunning) {
            this.startPolling();
        }

        return () => {
            this.subscribers = this.subscribers.filter(sub => sub !== callback);
            if (this.subscribers.length === 0) {
                this.stopPolling();
            }
        };
    }

    async startPolling() {
        if (this.isRunning) return;
        this.isRunning = true;

        while (this.isRunning) {
            try {
                const url = new URL('/api/v1/agents/events', window.location.origin);
                if (this.lastEventId) {
                    url.searchParams.append('since_id', this.lastEventId);
                }

                const response = await fetch(url);
                if (response.ok) {
                    const newEvents = await response.json();
                    if (newEvents && newEvents.length > 0) {
                        this.lastEventId = newEvents[newEvents.length - 1].id;

                        const mappedEvents = newEvents.map(evt => ({
                            id: evt.id,
                            agentId: evt.agent_id,
                            type: this.mapEventType(evt.event_type),
                            description: evt.description,
                            how: evt.how,
                            why: evt.why,
                            timestamp: evt.timestamp,
                            data: evt.data,
                            progress: evt.progress,
                            workflowName: evt.workflow_name
                        }));

                        this.events = [...this.events, ...mappedEvents].slice(-100);
                        this.notifySubscribers();
                    }
                }
            } catch (error) {
                console.error("AgentActivityService: Polling error", error);
            }
            await new Promise(resolve => setTimeout(resolve, this.pollInterval));
        }
    }

    stopPolling() {
        this.isRunning = false;
    }

    mapEventType(backendType) {
        const typeMap = {
            'started': 'info',
            'thinking': 'thinking',
            'step_completed': 'success',
            'completed': 'success',
            'failed': 'error',
            'handoff': 'delegation',
            'approval_request': 'warning'
        };
        return typeMap[backendType] || 'info';
    }

    notifySubscribers() {
        this.subscribers.forEach(callback => callback(this.events));
    }

    async getRecentActivity(userId, limit = 20) {
        return { success: true, events: this.events.slice(-limit) };
    }
}

export const agentActivityService = new AgentActivityService();
