import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { agentActivityService } from '../../services/AgentActivityService';

export const AgentActivityTheater = ({ selectedWorkflowName, selectedWorkflow }) => {
    const containerRef = useRef(null);
    const [viewport, setViewport] = useState({ width: 0, height: 0 });
    const [agents, setAgents] = useState([]);
    const [activeTasks, setActiveTasks] = useState([]);

    const LANE_POSITIONS = {
        research: { x: 16, y: 25 },
        marketing: { x: 50, y: 20 },
        sales: { x: 84, y: 30 },
        operations: { x: 25, y: 75 },
        content: { x: 75, y: 75 },
        support: { x: 50, y: 75 },
        orchestrator: { x: 50, y: 50 },
        evaluator: { x: 80, y: 50 }
    };

    const inferType = (name) => {
        const n = name.toLowerCase();
        if (n.includes('orchestrator')) return 'orchestrator';
        if (n.includes('evaluator') || n.includes('compliance')) return 'evaluator';
        if (n.includes('research')) return 'research';
        if (n.includes('marketing') || n.includes('email')) return 'marketing';
        if (n.includes('sales')) return 'sales';
        if (n.includes('support') || n.includes('ops') || n.includes('operation')) return 'support';
        if (n.includes('content') || n.includes('writer') || n.includes('seo')) return 'content';
        return 'research';
    };

    const getAgentColor = (type, status) => {
        const baseColors = {
            orchestrator: '#4F46E5',
            content: '#EC4899',
            evaluator: '#10B981',
            growth: '#6366F1',
            research: '#3B82F6',
            marketing: '#10B981',
            sales: '#F59E0B',
            support: '#8B5CF6',
        };
        const statusModifier = {
            idle: 0.3,
            working: 0.8,
            collaborating: 1.0,
            completed: 0.6
        };
        return {
            color: baseColors[type] || '#6B7280',
            auraOpacity: statusModifier[status] ?? 0.8
        };
    };

    const getAgentIcon = (type) => {
        const icons = {
            orchestrator: '👑',
            content: '✍️',
            evaluator: '⚖️',
            growth: '📈',
            research: '🔍',
            marketing: '🎯',
            sales: '💼',
            support: '🎧'
        };
        return icons[type] || '🤖';
    };

    const [paused, setPaused] = useState(new Set());

    // Subscribe to live events
    useEffect(() => {
        const unsubscribe = agentActivityService.subscribe((events) => {
            if (events.length === 0) return;

            setAgents(currentAgents => {
                const updatedAgents = [...currentAgents];

                events.forEach(evt => {
                    let agent = updatedAgents.find(a => a.id === evt.agentId);

                    if (!agent) {
                        const type = inferType(evt.agentId);
                        const center = LANE_POSITIONS[type] || { x: 50, y: 50 };
                        const jitter = (Math.random() - 0.5) * 10;
                        agent = {
                            id: evt.agentId,
                            name: evt.agentId,
                            type: type,
                            status: 'idle',
                            currentTask: evt.description,
                            position: { x: center.x + jitter, y: center.y + jitter },
                            progress: evt.progress || 0,
                            activityLog: []
                        };
                        updatedAgents.push(agent);
                    }

                    // Update agent state
                    agent.currentTask = evt.description;
                    agent.progress = evt.progress || agent.progress;

                    if (evt.type === 'error') agent.status = 'idle';
                    else if (evt.type === 'success') agent.status = 'completed';
                    else if (evt.type === 'thinking') agent.status = 'working';
                    else agent.status = 'working';

                    // Add to log
                    const logEntry = {
                        id: evt.id,
                        text: evt.description,
                        how: evt.how,
                        why: evt.why,
                        status: evt.type === 'success' ? 'done' : (evt.type === 'error' ? 'failed' : 'running'),
                        ts: evt.timestamp
                    };

                    if (!agent.activityLog.find(l => l.id === evt.id)) {
                        agent.activityLog = [logEntry, ...agent.activityLog].slice(0, 10);
                    }

                    // Handle Handoffs for visualization
                    if (evt.type === 'delegation' && evt.data?.target_agent) {
                        const targetId = evt.data.target_agent;
                        if (!activeTasks.find(t => t.id === `handoff-${evt.id}`)) {
                            setActiveTasks(prev => ([
                                ...prev.slice(-4),
                                { id: `handoff-${evt.id}`, from: evt.agentId, to: targetId, type: 'delegation', progress: 0 }
                            ]));
                        }
                    }
                });

                return updatedAgents;
            });
        });

        return unsubscribe;
    }, []);

    const [selected, setSelected] = useState(null);
    const [showWorkflowDetails, setShowWorkflowDetails] = useState(false);

    const estimateWorkflowCost = () => {
        const activeCount = agents.filter(a => a.status === 'working' || a.status === 'collaborating').length;
        const baseCredits = activeCount * 5 + activeTasks.length * 2;
        const estimatedCost = baseCredits * 0.1;
        return { baseCredits, estimatedCost };
    };

    useEffect(() => {
        if (!containerRef.current) return;
        const el = containerRef.current;
        const update = () => setViewport({ width: el.clientWidth, height: el.clientHeight });
        update();
        const ro = new ResizeObserver(update);
        ro.observe(el);
        return () => { try { ro.disconnect(); } catch { } };
    }, []);

    // Rebuild scene from selected workflow (agents, lanes, and handoffs)
    useEffect(() => {
        if (!selectedWorkflow) return;
        const wfAgents = (selectedWorkflow.agents || selectedWorkflow.agents_involved || []).map((a) => String(a));
        if (!wfAgents.length) return;
        const laneCenter = {
            research: { x: 16, y: 25 },
            marketing: { x: 50, y: 20 },
            sales: { x: 84, y: 30 },
            operations: { x: 25, y: 75 },
            content: { x: 75, y: 75 },
            support: { x: 50, y: 75 }
        };
        const inferType = (name) => {
            const n = name.toLowerCase();
            if (n.includes('research')) return 'research';
            if (n.includes('marketing') || n.includes('email')) return 'marketing';
            if (n.includes('sales')) return 'sales';
            if (n.includes('support') || n.includes('ops') || n.includes('operation')) return 'support';
            if (n.includes('content') || n.includes('writer') || n.includes('seo')) return 'content';
            return 'research';
        };
        const builtAgents = wfAgents.map((n, idx) => {
            const type = inferType(n);
            const center = laneCenter[type] || { x: 50, y: 50 };
            const jitterX = ((idx % 3) - 1) * 6; // -6,0,6
            const jitterY = Math.floor(idx / 3) * 6;
            return {
                id: `${type}-${idx}`,
                name: n,
                type,
                status: 'working',
                currentTask: 'Executing workflow step',
                position: { x: Math.max(5, Math.min(95, center.x + jitterX)), y: Math.max(10, Math.min(90, center.y + jitterY)) },
                progress: Math.random() * 0.6 + 0.3
            };
        });
        setAgents(builtAgents);

        const steps = Array.isArray(selectedWorkflow.actions) ? selectedWorkflow.actions : [];
        const edges = [];
        for (let i = 0; i < steps.length - 1; i++) {
            const fromName = String(steps[i].agent || '');
            const toName = String(steps[i + 1].agent || '');
            const from = builtAgents.find(a => a.name === fromName)?.id;
            const to = builtAgents.find(a => a.name === toName)?.id;
            if (from && to && from !== to) {
                edges.push({ id: `wf-${i}`, from, to, type: 'data', progress: 0.5 });
            }
        }
        setActiveTasks(edges.length ? edges : []);
    }, [selectedWorkflow]);

    return (
        <div ref={containerRef} className="relative w-full h-96 bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-inner">
            {selectedWorkflowName && (
                <div className="absolute top-4 left-4 z-20 px-3 py-1 text-[10px] font-black rounded-lg bg-[#1a6fff] text-white shadow-lg uppercase tracking-widest">{selectedWorkflowName}</div>
            )}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-slate-50 via-white to-slate-100 opacity-60" />

            <div className="absolute inset-6">
                <div className="absolute left-0 top-0 w-1/3 h-1/2 bg-indigo-50/30 rounded-3xl border border-indigo-100/50 border-dashed">
                    <div className="p-4 text-[10px] font-black text-indigo-400 uppercase tracking-widest">Strategy & Planning</div>
                </div>
                <div className="absolute right-0 top-0 w-1/3 h-1/2 bg-emerald-50/30 rounded-3xl border border-emerald-100/50 border-dashed">
                    <div className="p-4 text-[10px] font-black text-emerald-400 uppercase tracking-widest">Quality Control</div>
                </div>
                <div className="absolute left-1/4 bottom-0 w-1/2 h-1/3 bg-pink-50/30 rounded-3xl border border-pink-100/50 border-dashed">
                    <div className="p-4 text-[10px] font-black text-pink-400 uppercase tracking-widest">Content Execution Zone</div>
                </div>
            </div>

            {agents.map((agent) => {
                const { color, auraOpacity } = getAgentColor(agent.type, agent.status);
                return (
                    <motion.div
                        key={agent.id}
                        className="absolute cursor-pointer group z-10"
                        style={{ left: `${agent.position.x}%`, top: `${agent.position.y}%` }}
                        animate={{ scale: agent.status === 'working' ? [1, 1.1, 1] : 1 }}
                        transition={{ duration: 2, repeat: agent.status === 'working' ? Infinity : 0 }}
                        whileHover={{ scale: 1.2 }}
                        onClick={() => setSelected(agent.id)}
                    >
                        <motion.div
                            className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold shadow-lg relative"
                            style={{ backgroundColor: color }}
                        >
                            {/* Soft aura reflecting status; stays under avatar to occlude lines */}
                            <div
                                className="absolute rounded-full -inset-1"
                                style={{ backgroundColor: color, opacity: auraOpacity * 0.25, filter: 'blur(6px)', zIndex: -1 }}
                            />
                            <span className="text-lg">{getAgentIcon(agent.type)}</span>
                            {agent.status === 'working' && (
                                <motion.div
                                    className="absolute inset-0 rounded-full border-2 border-white"
                                    animate={{ rotate: 360 }}
                                    transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                                />
                            )}
                            {agent.progress > 0 && (
                                <svg className="absolute inset-0 w-full h-full -rotate-90">
                                    <circle
                                        cx="50%"
                                        cy="50%"
                                        r="20"
                                        fill="none"
                                        stroke="white"
                                        strokeWidth="2"
                                        strokeDasharray={`${agent.progress * 125.6} 125.6`}
                                        className="transition-all duration-500"
                                    />
                                </svg>
                            )}
                        </motion.div>
                        <motion.div
                            className="absolute left-1/2 transform -translate-x-1/2 bg-white rounded-lg shadow-lg p-2 min-w-max z-10 opacity-0 group-hover:opacity-100"
                            style={{ top: '3.5rem' }}
                            initial={false}
                            animate={{}}
                        >
                            <div className="text-xs font-medium text-gray-800">{agent.name}</div>
                            <div className="text-xs text-gray-600 italic mb-1">{agent.currentTask}</div>
                            {agent.activityLog[0]?.why && (
                                <div className="text-[10px] bg-blue-50 text-blue-700 p-1 rounded border border-blue-100 mb-1">
                                    <strong>Goal:</strong> {agent.activityLog[0].why}
                                </div>
                            )}
                            <div className="text-[10px] text-zinc-500">{Math.round(agent.progress * 100)}% complete</div>
                        </motion.div>
                    </motion.div>
                );
            })}

            {/* Collaboration lines between agents */}
            <svg className="absolute inset-0 pointer-events-none z-0" style={{ width: '100%', height: '100%' }}>
                {activeTasks.map((task) => {
                    const fromAgent = agents.find(a => a.id === task.from);
                    const toAgent = agents.find(a => a.id === task.to);
                    if (!fromAgent || !toAgent) return null;
                    const fromX = (fromAgent.position.x / 100) * viewport.width;
                    const fromY = (fromAgent.position.y / 100) * viewport.height;
                    const toX = (toAgent.position.x / 100) * viewport.width;
                    const toY = (toAgent.position.y / 100) * viewport.height;
                    return (
                        <line
                            key={`line-${task.id}`}
                            x1={fromX}
                            y1={fromY}
                            x2={toX}
                            y2={toY}
                            stroke="rgba(59, 130, 246, 0.35)"
                            strokeWidth="2"
                            strokeDasharray="4,4"
                        />
                    );
                })}
            </svg>

            {activeTasks.map((task) => {
                const fromAgent = agents.find(a => a.id === task.from);
                const toAgent = agents.find(a => a.id === task.to);
                if (!fromAgent || !toAgent) return null;
                return (
                    <motion.div
                        key={task.id}
                        className="absolute w-2 h-2 rounded-full bg-yellow-400 shadow-lg"
                        initial={{ left: ((fromAgent.position.x / 100) * viewport.width), top: ((fromAgent.position.y / 100) * viewport.height) }}
                        animate={{ left: ((toAgent.position.x / 100) * viewport.width), top: ((toAgent.position.y / 100) * viewport.height) }}
                        transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
                    />
                );
            })}

            <div className="absolute bottom-4 right-4 flex space-x-2 z-20">
                <button className="px-3 py-1 bg-white rounded-lg shadow text-xs font-medium hover:bg-gray-50">Pause</button>
                <button onClick={() => setShowWorkflowDetails(true)} className="px-3 py-1 bg-[#1a6fff] text-white rounded-lg shadow text-xs font-medium hover:bg-[#4d8fff]">Details</button>
            </div>

            {selected && (
                <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl shadow-xl w-full max-w-4xl p-6 relative max-h-[85vh] overflow-y-auto">
                        <button className="absolute top-3 right-3 text-zinc-500 hover:text-gray-600" onClick={() => setSelected(null)}>×</button>
                        {(() => {
                            const a = agents.find(x => x.id === selected);
                            if (!a) return null;
                            return (
                                <div className="space-y-4">
                                    <div className="flex items-start justify-between">
                                        <div>
                                            <h3 className="text-xl font-semibold text-gray-900">{a.name}</h3>
                                            <p className="text-sm text-zinc-500 capitalize">{a.type} • {a.status}</p>
                                        </div>
                                        <button
                                            onClick={() => {
                                                setPaused(prev => {
                                                    const next = new Set(prev);
                                                    if (next.has(a.id)) next.delete(a.id); else next.add(a.id);
                                                    return next;
                                                });
                                            }}
                                            className={`px-3 py-1.5 text-sm rounded-md border ${paused.has(a.id) ? 'bg-yellow-100 text-yellow-800' : 'bg-white'}`}
                                        >
                                            {paused.has(a.id) ? 'Resume Agent' : 'Pause Agent'}
                                        </button>
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {/* Left column: details */}
                                        <div className="space-y-4">
                                            <div className="bg-gray-50 rounded-lg p-3 text-sm">
                                                <div className="flex items-center justify-between mb-1"><span className="text-gray-600">Current Task</span><span className="font-medium">{Math.round(a.progress * 100)}%</span></div>
                                                <div className="text-gray-800">{a.currentTask}</div>
                                                <div className="mt-2 w-full bg-gray-200 rounded-full h-2"><div className="bg-blue-600 h-2 rounded-full" style={{ width: `${a.progress * 100}%` }} /></div>
                                            </div>
                                            <div className="grid grid-cols-2 gap-3 text-sm">
                                                <div className="bg-gray-50 rounded-lg p-3">
                                                    <div className="font-medium text-gray-800 mb-1">Completed Tasks</div>
                                                    <ul className="list-disc list-inside text-gray-600 space-y-1">
                                                        <li>Finished prior milestone</li>
                                                        <li>Synced with teammate</li>
                                                        <li>Queued deliverable</li>
                                                    </ul>
                                                </div>
                                                <div className="bg-gray-50 rounded-lg p-3">
                                                    <div className="font-medium text-gray-800 mb-1">Upcoming Todos</div>
                                                    <ul className="list-disc list-inside text-gray-600 space-y-1">
                                                        <li>Prepare handoff</li>
                                                        <li>Validate output</li>
                                                        <li>Notify owner</li>
                                                    </ul>
                                                </div>
                                            </div>
                                            <div className="flex items-center justify-end gap-2">
                                                {/* Quick task dropdown */}
                                                <div className="relative">
                                                    <details className="relative">
                                                        <summary className="px-3 py-1.5 text-sm rounded-md border cursor-pointer select-none">Quick Tasks</summary>
                                                        <div className="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg border p-3 z-10">
                                                            <div className="text-xs text-zinc-500 mb-2">Select tasks for {a.name}</div>
                                                            <div className="space-y-2 text-sm">
                                                                <label className="flex items-center gap-2"><input type="checkbox" /> Generate brief</label>
                                                                <label className="flex items-center gap-2"><input type="checkbox" /> Draft email</label>
                                                                <label className="flex items-center gap-2"><input type="checkbox" /> Create report</label>
                                                            </div>
                                                            <div className="mt-3">
                                                                <textarea placeholder="Additional instructions..." className="w-full p-2 border rounded-md text-sm"></textarea>
                                                            </div>
                                                            <div className="mt-3 flex justify-end gap-2">
                                                                <button className="px-3 py-1 text-sm border rounded-md" onClick={(e) => { e.preventDefault(); e.currentTarget.closest('details')?.removeAttribute('open'); }}>Cancel</button>
                                                                <button className="px-3 py-1 text-sm bg-[#1a6fff] text-white rounded-md" onClick={(e) => { e.preventDefault(); alert('Tasks assigned'); e.currentTarget.closest('details')?.removeAttribute('open'); }}>Assign</button>
                                                            </div>
                                                        </div>
                                                    </details>
                                                </div>
                                                <button className="px-3 py-1.5 text-sm rounded-md bg-[#1a6fff] text-white">Open Chat</button>
                                            </div>
                                        </div>
                                        {/* Right column: Live activity feed */}
                                        <div className="space-y-4">
                                            <div className="bg-gray-50 rounded-lg p-3 text-sm">
                                                <div className="font-medium text-gray-800 mb-2">Live Activity</div>
                                                <ul className="divide-y border rounded max-h-[50vh] overflow-y-auto">
                                                    {(a.activityLog || []).slice().reverse().map(item => (
                                                        <li key={item.id} className="p-3">
                                                            <div className="flex items-center justify-between mb-1">
                                                                <div className="font-medium text-gray-900">{item.text}</div>
                                                                <span className={`text-[10px] px-2 py-0.5 rounded-full ${item.status === 'done' ? 'bg-green-100 text-green-700' : item.status === 'running' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'}`}>{item.status}</span>
                                                            </div>
                                                            <div className="grid grid-cols-2 gap-2 mt-2">
                                                                {item.why && (
                                                                    <div className="bg-indigo-50/50 p-2 rounded border border-indigo-100/50">
                                                                        <div className="text-[9px] font-bold text-indigo-400 uppercase tracking-tighter">Strategic Why</div>
                                                                        <div className="text-[11px] text-indigo-900">{item.why}</div>
                                                                    </div>
                                                                )}
                                                                {item.how && (
                                                                    <div className="bg-white/[0.03]/50 p-2 rounded border border-slate-100/50">
                                                                        <div className="text-[9px] font-bold text-zinc-600 uppercase tracking-tighter">Technical How</div>
                                                                        <div className="text-[11px] text-slate-900">{item.how}</div>
                                                                    </div>
                                                                )}
                                                            </div>
                                                            <div className="text-[9px] text-zinc-500 mt-2">{new Date(item.ts).toLocaleTimeString()}</div>
                                                        </li>
                                                    ))}
                                                    {(a.activityLog || []).length === 0 && (
                                                        <li className="p-2 text-zinc-500 text-sm">No activity yet</li>
                                                    )}
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            );
                        })()}
                    </div>
                </div>
            )}

            {showWorkflowDetails && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-xl shadow-2xl w-full max-w-3xl p-6 relative">
                        <button className="absolute top-3 right-3 text-zinc-500 hover:text-gray-600" onClick={() => setShowWorkflowDetails(false)}>×</button>
                        <div className="space-y-4">
                            <div className="flex items-start justify-between">
                                <div>
                                    <h3 className="text-xl font-semibold text-gray-900">Workflow Overview</h3>
                                    <p className="text-sm text-zinc-500">Live orchestration of agents and handoffs</p>
                                </div>
                                {(() => {
                                    const { baseCredits, estimatedCost } = estimateWorkflowCost(); return (
                                        <div className="text-right">
                                            <div className="text-xs text-zinc-500">Estimated Credits</div>
                                            <div className="text-lg font-semibold text-blue-600">{baseCredits}</div>
                                            <div className="text-xs text-zinc-500 mt-1">Est. Cost</div>
                                            <div className="text-lg font-semibold text-green-600">${estimatedCost.toFixed(2)}</div>
                                        </div>
                                    );
                                })()}
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <div className="font-medium text-gray-800 mb-2">Current Flow</div>
                                    <ul className="text-sm text-gray-700 space-y-1">
                                        {activeTasks.slice(-6).map(t => {
                                            const from = agents.find(a => a.id === t.from)?.name || t.from;
                                            const to = agents.find(a => a.id === t.to)?.name || t.to;
                                            return <li key={`sum-${t.id}`}>{from} → {to} ({t.type})</li>;
                                        })}
                                        {activeTasks.length === 0 && <li>No active handoffs detected</li>}
                                    </ul>
                                </div>
                                <div className="bg-gray-50 rounded-lg p-4">
                                    <div className="font-medium text-gray-800 mb-2">Agent Status</div>
                                    <ul className="text-sm text-gray-700 space-y-1">
                                        {agents.map(a => (
                                            <li key={`status-${a.id}`} className="flex items-center justify-between">
                                                <span>{a.name}</span>
                                                <span className="text-zinc-500 capitalize">{a.status}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
