import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Send, User, Bot, Sparkles, ArrowRight, CheckCircle,
    Settings, Loader2, Building, Heart, Target, Database, Upload, Link, X
} from 'lucide-react';
import { agentAPI } from '../../services/api';

const STEPS = [
    { id: 'core', title: 'The Core', icon: Building, description: 'Defining your business identity' },
    { id: 'brand', title: 'The Soul', icon: Heart, description: 'Establishing your brand voice' },
    { id: 'icp', title: 'The Target', icon: Target, description: 'Identifying your ideal client' },
    { id: 'sources', title: 'The Archive', icon: Database, description: 'Connecting your documents' }
];

const OnboardingFlow = () => {
    const [currentStep, setCurrentStep] = useState(0);
    const [isSaving, setIsSaving] = useState(false);
    const [identity, setIdentity] = useState({
        business_name: '',
        niche: '',
        core_objectives: [],
        brand: {
            voice: '',
            tone: '',
            vocabulary: [],
            dos: [],
            donts: []
        },
        icp: {
            ideal_client_description: '',
            demographics: {},
            psychographics: [],
            pain_points: [],
            buying_triggers: []
        },
        knowledge_base: []
    });

    const [currentInput, setCurrentInput] = useState('');
    const [files, setFiles] = useState([]);

    const handleNext = async () => {
        if (currentStep < STEPS.length - 1) {
            setCurrentStep(currentStep + 1);
        } else {
            await finalizeOnboarding();
        }
    };

    const handleBack = () => {
        if (currentStep > 0) setCurrentStep(currentStep - 1);
    };

    const finalizeOnboarding = async () => {
        setIsSaving(true);
        try {
            await fetch('/api/identity', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(identity)
            });
            // Redirect or show success
            window.location.href = '/';
        } catch (error) {
            console.error("Failed to save identity", error);
        } finally {
            setIsSaving(false);
        }
    };

    const handleFileUpload = async (e) => {
        const uploadedFiles = Array.from(e.target.files);
        setFiles(prev => [...prev, ...uploadedFiles]);

        // In a real system, we'd upload each to /api/identity/document
        for (const file of uploadedFiles) {
            const formData = new FormData();
            formData.append('file', file);
            try {
                const response = await fetch('/api/identity/document', {
                    method: 'POST',
                    body: formData
                });
                const source = await response.json();
                setIdentity(prev => ({
                    ...prev,
                    knowledge_base: [...prev.knowledge_base, source]
                }));
            } catch (error) {
                console.error("Upload failed", error);
            }
        }
    };

    return (
        <div className="flex flex-col h-screen bg-white/[0.03] p-8">
            <div className="max-w-5xl mx-auto w-full flex flex-col h-full bg-white rounded-[2rem] shadow-2xl border border-slate-200 overflow-hidden">

                {/* Stepper Header */}
                <div className="bg-slate-900 p-10 text-white">
                    <div className="flex justify-between items-center mb-10">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-indigo-500 rounded-2xl shadow-lg shadow-indigo-500/30">
                                <Sparkles size={28} strokeWidth={1.5} />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold tracking-tight">Business Induction</h1>
                                <p className="text-zinc-600 text-sm">Phase 4: Persistent Context Alignment</p>
                            </div>
                        </div>
                        <div className="text-right">
                            <span className="text-3xl font-black text-indigo-400">0{currentStep + 1}</span>
                            <span className="text-zinc-400 text-sm ml-2">/ 04</span>
                        </div>
                    </div>

                    <div className="flex gap-8">
                        {STEPS.map((step, idx) => (
                            <div key={step.id} className={`flex-1 group cursor-pointer ${idx > currentStep ? 'opacity-30' : ''}`}>
                                <div className={`h-1 rounded-full mb-3 transition-all ${idx <= currentStep ? 'bg-indigo-500' : 'bg-slate-700'}`} />
                                <div className="flex items-center gap-3">
                                    <step.icon size={16} className={idx === currentStep ? 'text-indigo-400' : 'text-zinc-400'} />
                                    <span className={`text-xs font-black uppercase tracking-widest ${idx === currentStep ? 'text-white' : 'text-zinc-400'}`}>
                                        {step.title}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Content Area */}
                <div className="flex-1 overflow-y-auto p-12 bg-white/[0.03]/50">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={STEPS[currentStep].id}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="max-w-2xl mx-auto"
                        >
                            <div className="mb-10 text-center">
                                <h2 className="text-3xl font-bold text-slate-900 mb-3">{STEPS[currentStep].description}</h2>
                                <p className="text-zinc-400">Provide these details to train your Orchestrator on your specific business DNA.</p>
                            </div>

                            {/* Step Components */}
                            {currentStep === 0 && (
                                <div className="space-y-6">
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-zinc-600 uppercase tracking-widest ml-1">Company Legal Name</label>
                                        <input
                                            type="text"
                                            value={identity.business_name}
                                            onChange={(e) => setIdentity({ ...identity, business_name: e.target.value })}
                                            className="w-full glass-panel p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                                            placeholder="e.g. Acme Innovations"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-zinc-600 uppercase tracking-widest ml-1">Business Niche & Mission</label>
                                        <textarea
                                            value={identity.niche}
                                            onChange={(e) => setIdentity({ ...identity, niche: e.target.value })}
                                            className="w-full glass-panel p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all h-32"
                                            placeholder="What exactly do you do and what is your unique value proposition?"
                                        />
                                    </div>
                                </div>
                            )}

                            {currentStep === 1 && (
                                <div className="space-y-6">
                                    <div className="grid grid-cols-2 gap-6">
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-zinc-600 uppercase tracking-widest ml-1">Brand Voice</label>
                                            <input
                                                type="text"
                                                value={identity.brand.voice}
                                                onChange={(e) => setIdentity({ ...identity, brand: { ...identity.brand, voice: e.target.value } })}
                                                className="w-full glass-panel p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                                                placeholder="e.g. Authoritative"
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-zinc-600 uppercase tracking-widest ml-1">Content Tone</label>
                                            <input
                                                type="text"
                                                value={identity.brand.tone}
                                                onChange={(e) => setIdentity({ ...identity, brand: { ...identity.brand, tone: e.target.value } })}
                                                className="w-full glass-panel p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                                                placeholder="e.g. Humorous"
                                            />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-zinc-600 uppercase tracking-widest ml-1">Vocabulary (Keywords)</label>
                                        <input
                                            type="text"
                                            className="w-full glass-panel p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                                            placeholder="Comma separated terms your brand loves..."
                                            onKeyDown={(e) => {
                                                if (e.key === 'Enter') {
                                                    const val = e.target.value.trim();
                                                    if (val) setIdentity({ ...identity, brand: { ...identity.brand, vocabulary: [...identity.brand.vocabulary, val] } });
                                                    e.target.value = '';
                                                }
                                            }}
                                        />
                                        <div className="flex flex-wrap gap-2 mt-2">
                                            {identity.brand.vocabulary.map((v, i) => (
                                                <span key={i} className="px-3 py-1 bg-indigo-50 text-[#1a6fff] rounded-lg text-xs font-bold border border-indigo-100">{v}</span>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {currentStep === 2 && (
                                <div className="space-y-6">
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-zinc-600 uppercase tracking-widest ml-1">Ideal Client Profile</label>
                                        <textarea
                                            value={identity.icp.ideal_client_description}
                                            onChange={(e) => setIdentity({ ...identity, icp: { ...identity.icp, ideal_client_description: e.target.value } })}
                                            className="w-full glass-panel p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none h-48"
                                            placeholder="Describe your perfect customer in detail. Who are they? What do they value?"
                                        />
                                    </div>
                                </div>
                            )}

                            {currentStep === 3 && (
                                <div className="space-y-8">
                                    <div className="border-2 border-dashed border-slate-200 rounded-[2rem] p-12 text-center hover:border-indigo-400 transition-all cursor-pointer relative group">
                                        <input
                                            type="file"
                                            multiple
                                            onChange={handleFileUpload}
                                            className="absolute inset-0 opacity-0 cursor-pointer"
                                        />
                                        <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-all">
                                            <Upload className="text-zinc-600 group-hover:text-indigo-500" strokeWidth={1.5} />
                                        </div>
                                        <h3 className="text-xl font-bold text-slate-900 mb-2">Upload Business Intelligence</h3>
                                        <p className="text-zinc-400">Brand guidelines, product catalogs, or internal strategy docs.</p>
                                    </div>

                                    {files.length > 0 && (
                                        <div className="space-y-3">
                                            {files.map((f, i) => (
                                                <div key={i} className="bg-white p-4 rounded-2xl border border-slate-200 flex items-center justify-between">
                                                    <div className="flex items-center gap-3">
                                                        <Database size={18} className="text-indigo-400" strokeWidth={1.5} />
                                                        <span className="text-sm font-bold text-zinc-400">{f.name}</span>
                                                    </div>
                                                    <CheckCircle size={18} className="text-emerald-500" strokeWidth={1.5} />
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}

                        </motion.div>
                    </AnimatePresence>
                </div>

                {/* Footer Controls */}
                <div className="p-10 border-t border-slate-100 bg-white flex justify-between items-center">
                    <button
                        onClick={handleBack}
                        disabled={currentStep === 0}
                        className="px-8 py-4 text-zinc-600 font-black uppercase tracking-widest text-xs hover:text-slate-900 disabled:opacity-30 transition-all"
                    >
                        Back
                    </button>
                    <button
                        onClick={handleNext}
                        className="px-12 py-4 bg-[#1a6fff] text-white rounded-2xl font-black uppercase tracking-widest text-xs shadow-xl shadow-indigo-600/30 hover:bg-[#4d8fff] transition-all flex items-center gap-3 group"
                    >
                        {currentStep === STEPS.length - 1 ? (isSaving ? 'Finalizing DNA...' : 'Finish Induction') : 'Continue Journey'}
                        <ArrowRight size={14} className="group-hover:translate-x-1 transition-all" strokeWidth={1.5} />
                    </button>
                </div>

            </div>
        </div>
    );
};

export default OnboardingFlow;
