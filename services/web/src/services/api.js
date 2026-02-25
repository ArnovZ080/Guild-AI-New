const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001';

export const agentAPI = {
    /**
     * List all available agents
     */
    listAgents: async () => {
        try {
            const response = await fetch(`${API_BASE}/agents/`);
            if (!response.ok) {
                throw new Error(`Failed to fetch agents: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error listing agents:', error);
            throw error;
        }
    },

    /**
     * Run an agent with input data
     */
    runAgent: async (agentName, inputData, context = {}) => {
        try {
            const response = await fetch(`${API_BASE}/agents/${agentName}/run`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    input_data: inputData,
                    context: context
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `Agent execution failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`Error running agent ${agentName}:`, error);
            throw error;
        }
    }
};

export const healthAPI = {
    /**
     * Check API health
     */
    checkHealth: async () => {
        try {
            const response = await fetch(`${API_BASE}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'error', error: error.message };
        }
    }
};
