import React, { useState, useCallback } from 'react';
import ReactFlow, {
    addEdge,
    Background,
    Controls,
    useNodesState,
    useEdgesState,
    MarkerType
} from 'reactflow';
import 'reactflow/dist/style.css';
import { motion } from 'framer-motion';
import {
    Settings, Save, Play, Plus, Trash2,
    CheckCircle, AlertCircle, MoreVertical,
    MousePointer, Layout, FileText, Share2
} from 'lucide-react';

const initialNodes = [
    {
        id: '1',
        type: 'input',
        data: { label: 'Start Trigger' },
        position: { x: 250, y: 50 },
        style: { background: '#F0F9FF', border: '1px solid #BAE6FD', color: '#0369A1', fontWeight: 'bold' }
    },
    {
        id: '2',
        data: { label: 'Research Agent' },
        position: { x: 100, y: 150 },
        style: { background: '#F0FDFA', border: '1px solid #99F6E4', color: '#0F766E' }
    },
    {
        id: '3',
        data: { label: 'Content Agent' },
        position: { x: 400, y: 150 },
        style: { background: '#FFF7ED', border: '1px solid #FFEDD5', color: '#C2410C' }
    },
];

const initialEdges = [
    { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: '#94A3B8' } },
    { id: 'e1-3', source: '1', target: '3', animated: true, style: { stroke: '#94A3B8' } },
];

const WorkflowBuilder = () => {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
    const [selectedNode, setSelectedNode] = useState(null);

    const onConnect = useCallback((params) => setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: '#94A3B8' } }, eds)), [setEdges]);

    const onNodeClick = (event, node) => {
        setSelectedNode(node);
    };

    const addNode = () => {
        const id = `${nodes.length + 1}`;
        const newNode = {
            id,
            data: { label: `New Node ${id}` },
            position: { x: Math.random() * 400, y: Math.random() * 400 },
            style: { background: '#fff', border: '1px solid #ddd', padding: '10px', borderRadius: '5px' }
        };
        setNodes((nds) => nds.concat(newNode));
    };

    return (
        <div className="h-full flex flex-col bg-slate-50 relative">
            <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between shadow-sm z-10 relative">
                <div>
                    <h1 className="text-xl font-bold text-gray-900">Workflow Builder</h1>
                    <p className="text-xs text-gray-500">Design autonomous agent processes</p>
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={addNode}
                        className="flex items-center gap-2 px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-sm hover:bg-gray-50 text-gray-700 font-medium"
                    >
                        <Plus size={16} /> Add Node
                    </button>
                    <button className="flex items-center gap-2 px-3 py-1.5 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700 font-medium shadow-sm">
                        <Save size={16} /> Save Workflow
                    </button>
                    <button className="flex items-center gap-2 px-3 py-1.5 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700 font-medium shadow-sm">
                        <Play size={16} /> Run
                    </button>
                </div>
            </div>

            <div className="flex-1 relative flex">
                {/* Canvas */}
                <div className="flex-1 h-[calc(100vh-140px)] bg-slate-50">
                    <ReactFlow
                        nodes={nodes}
                        edges={edges}
                        onNodesChange={onNodesChange}
                        onEdgesChange={onEdgesChange}
                        onConnect={onConnect}
                        onNodeClick={onNodeClick}
                        fitView
                    >
                        <Background color="#cbd5e1" gap={16} />
                        <Controls />
                    </ReactFlow>
                </div>

                {/* Properties Panel */}
                {selectedNode && (
                    <motion.div
                        initial={{ x: 300, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        exit={{ x: 300, opacity: 0 }}
                        className="w-80 bg-white border-l border-gray-200 p-4 shadow-xl z-20 absolute right-0 top-0 bottom-0 overflow-y-auto"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="font-bold text-gray-900">Properties</h3>
                            <button onClick={() => setSelectedNode(null)} className="text-gray-400 hover:text-gray-600"><Trash2 size={16} /></button>
                        </div>

                        <div className="space-y-4">
                            <div>
                                <label className="block text-xs font-medium text-gray-500 uppercase mb-1">Label</label>
                                <input
                                    type="text"
                                    value={selectedNode.data.label}
                                    onChange={(e) => {
                                        const label = e.target.value;
                                        setNodes((nds) => nds.map((n) => {
                                            if (n.id === selectedNode.id) {
                                                n.data = { ...n.data, label };
                                            }
                                            return n;
                                        }));
                                    }}
                                    className="w-full border border-gray-300 rounded px-2 py-1 text-sm"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-medium text-gray-500 uppercase mb-1">Type</label>
                                <select className="w-full border border-gray-300 rounded px-2 py-1 text-sm bg-white">
                                    <option>Agent Task</option>
                                    <option>API Trigger</option>
                                    <option>Wait Condition</option>
                                    <option>Human Approval</option>
                                </select>
                            </div>

                            <div className="p-3 bg-blue-50 border border-blue-100 rounded text-xs text-blue-700">
                                Configure advanced settings for this node in the execution layer.
                            </div>
                        </div>
                    </motion.div>
                )}
            </div>
        </div>
    );
};

export default WorkflowBuilder;
