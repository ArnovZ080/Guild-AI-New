
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Activity,
    Bot,
    CheckCircle,
    AlertTriangle,
    Eye,
    Zap,
    Database,
    Filter,
    Search,
    RefreshCw,
    Bell,
    BellOff,
    Minimize2,
    Download
} from 'lucide-react';
import { agentActivityService } from '../../services/AgentActivityService.js';

const AgentActivityFeed = ({ userId, isCompact = false, maxEvents = 20 }) => {
    const [events, setEvents] = useState([]);
    const [filteredEvents, setFilteredEvents] = useState([]);
    const [filter, setFilter] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [isLive, setIsLive] = useState(true);
    const [isExpanded, setIsExpanded] = useState(!isCompact);
    const [selectedEvent, setSelectedEvent] = useState(null);

    // Subscribe to real-time updates
    useEffect(() => {
        setIsLoading(true);
        const unsubscribe = agentActivityService.subscribe((newEvents) => {
            setEvents(newEvents);
            setIsLoading(false);
        });
        return unsubscribe;
    }, [userId, isLive]);

    // Filter events
    useEffect(() => {
        let filtered = events;

        if (filter !== 'all') {
            filtered = filtered.filter(event =>
                event.event_type.includes(filter) ||
                (filter === 'important' && (event.event_type.includes('failed') || event.event_type.includes('approval')))
            );
        }

        if (searchTerm) {
            filtered = filtered.filter(event =>
                event.event_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
                JSON.stringify(event.data).toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        setFilteredEvents(filtered);
    }, [events, filter, searchTerm]);

    const getEventIcon = (eventType) => {
        if (eventType.includes('workflow')) return <Zap className="w-4 h-4" strokeWidth={1.5} />;
        if (eventType.includes('step')) return <Activity className="w-4 h-4" strokeWidth={1.5} />;
        if (eventType.includes('completed')) return <CheckCircle className="w-4 h-4" strokeWidth={1.5} />;
        if (eventType.includes('failed')) return <AlertTriangle className="w-4 h-4" strokeWidth={1.5} />;
        if (eventType.includes('approval')) return <Eye className="w-4 h-4" strokeWidth={1.5} />;
        if (eventType.includes('data')) return <Database className="w-4 h-4" strokeWidth={1.5} />;
        return <Bot className="w-4 h-4" strokeWidth={1.5} />;
    };

    const getEventColor = (eventType) => {
        if (eventType.includes('completed')) return 'text-green-600 bg-green-100';
        if (eventType.includes('failed')) return 'text-red-600 bg-red-100';
        if (eventType.includes('running') || eventType.includes('started')) return 'text-blue-600 bg-blue-100';
        if (eventType.includes('approval')) return 'text-yellow-600 bg-yellow-100';
        return 'text-gray-600 bg-gray-100';
    };

    const formatTimestamp = (timestamp) => {
        if (!timestamp) return 'Unknown';
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        return date.toLocaleDateString();
    };

    if (isCompact && !isExpanded) {
        return (
            <div className="fixed bottom-4 right-4 z-50">
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setIsExpanded(true)}
                    className="flex items-center space-x-2 px-4 py-3 bg-[#1a6fff] text-white rounded-full shadow-lg hover:bg-[#4d8fff]"
                >
                    <Activity className="w-5 h-5" strokeWidth={1.5} />
                    <span className="font-medium">Agent Activity</span>
                    {events.length > 0 && (
                        <span className="px-2 py-0.5 bg-white text-blue-600 rounded-full text-xs font-bold">
                            {events.length}
                        </span>
                    )}
                </motion.button>
            </div>
        );
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={`bg-white rounded-lg shadow-lg ${isCompact ? 'fixed bottom-4 right-4 z-50 w-96 max-h-[600px]' : 'w-full'}`}
        >
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
                <div className="flex items-center space-x-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                        <Activity className="w-5 h-5 text-blue-600" strokeWidth={1.5} />
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold text-gray-900">Agent Activity Feed</h3>
                        <p className="text-sm text-gray-600">Real-time autonomous operations</p>
                    </div>
                </div>
                <div className="flex items-center space-x-2">
                    <button onClick={() => setIsLive(!isLive)} className={`p-2 rounded-lg transition-colors ${isLive ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'}`}>
                        {isLive ? <Bell className="w-4 h-4" strokeWidth={1.5} /> : <BellOff className="w-4 h-4" strokeWidth={1.5} />}
                    </button>
                    <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                        <Download className="w-4 h-4 text-gray-600" strokeWidth={1.5} />
                    </button>
                    {isCompact && (
                        <button onClick={() => setIsExpanded(false)} className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                            <Minimize2 className="w-4 h-4 text-gray-600" strokeWidth={1.5} />
                        </button>
                    )}
                </div>
            </div>

            <div className="p-4 border-b border-gray-200 space-y-3">
                <div className="flex items-center space-x-3">
                    <Filter className="w-4 h-4 text-zinc-500" strokeWidth={1.5} />
                    <select
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                        <option value="all">All Events</option>
                        <option value="workflow">Workflows</option>
                        <option value="step">Steps</option>
                        <option value="completed">Completed</option>
                        <option value="failed">Failed</option>
                        <option value="approval">Approvals</option>
                    </select>
                    <input
                        type="text"
                        placeholder="Search..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm"
                    />
                </div>
            </div>

            <div className={`overflow-y-auto ${isCompact ? 'max-h-96' : 'max-h-[600px]'} p-4`}>
                {isLoading ? (
                    <div className="flex items-center justify-center py-12">
                        <RefreshCw className="w-6 h-6 text-blue-600 animate-spin" strokeWidth={1.5} />
                    </div>
                ) : filteredEvents.length === 0 ? (
                    <div className="text-center py-12 text-zinc-500">No activity yet</div>
                ) : (
                    <div className="space-y-3">
                        <AnimatePresence>
                            {filteredEvents.map((event, index) => (
                                <motion.div
                                    key={`${event.id}`}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: 20 }}
                                    className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                                    onClick={() => setSelectedEvent(selectedEvent?.id === event.id ? null : event)}
                                >
                                    <div className="flex items-start justify-between">
                                        <div className="flex items-start space-x-3 flex-1">
                                            <div className={`p-2 rounded-lg ${getEventColor(event.event_type)}`}>
                                                {getEventIcon(event.event_type)}
                                            </div>
                                            <div>
                                                <h4 className="font-medium text-gray-900 text-sm">
                                                    {event.event_type.replace(/_/g, ' ').toUpperCase()}
                                                </h4>
                                                <p className="text-xs text-gray-600 mt-1">{event.workflow_name || 'System'}</p>
                                            </div>
                                        </div>
                                        <span className="text-xs text-zinc-500">{formatTimestamp(event.timestamp)}</span>
                                    </div>
                                    {selectedEvent?.id === event.id && (
                                        <motion.div
                                            initial={{ height: 0 }}
                                            animate={{ height: 'auto' }}
                                            className="mt-2 pt-2 border-t text-xs text-gray-600"
                                        >
                                            <pre className="whitespace-pre-wrap">{JSON.stringify(event.data, null, 2)}</pre>
                                        </motion.div>
                                    )}
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default AgentActivityFeed;
