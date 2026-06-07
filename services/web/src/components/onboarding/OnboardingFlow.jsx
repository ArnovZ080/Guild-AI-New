import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Sparkles, ArrowRight, CheckCircle,
    Building, Heart, Target, Database, Upload, TrendingUp
} from 'lucide-react';
import { api } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const STEPS = [
    { id: 'core', title: 'The Core', icon: Building, description: 'Defining your business identity' },
    { id: 'audience', title: 'The Target', icon: Target, description: 'Identifying your ideal client' },
    { id: 'brand', title: 'The Soul', icon: Heart, description: 'Establishing your brand voice' },
    { id: 'goals', title: 'The Vision', icon: TrendingUp, description: 'Setting goals & preferences' },
    { id: 'sources', title: 'The Archive', icon: Database, description: 'Connecting your documents' }
];

const OnboardingFlow = () => {
    const { setIdentityComplete } = useAuth();
    const navigate = useNavigate();
    const [currentStep, setCurrentStep] = useState(0);
    const [isSaving, setIsSaving] = useState(false);
    const scrollContainerRef = useRef(null);

    useEffect(() => {
        if (scrollContainerRef.current) {
            scrollContainerRef.current.scrollTo(0, 0);
        }
    }, [currentStep]);
    
    const [identity, setIdentity] = useState({
        // Core
        user_name: '',
        business_name: '',
        niche: '',
        business_type: '',
        business_stage: '',
        
        // Audience
        audience_type: '',
        customer_avatar: '',
        audience_problem: '',
        audience_size: '',
        icp_description: '',
        
        // Brand
        brand_voice_tone: '',
        brand_personality: '',
        brand_colors: '',
        logo_status: '',
        brand_visual_style: '',
        brand_values: '',
        brand_story: '',
        brand_positioning: '',
        brand_differentiation: '',
        brand_consistency: '',
        
        // Goals & Preferences
        priority_3months: '',
        guild_support_focus: '',
        guild_working_style: '',
        vision_12months: '',
        biggest_challenge: '',
        data_storage: 'Secure cloud storage (recommended)',
        sensitive_data: 'Limited access with my approval',
        automation_level: 'Moderately autonomous - ask for important decisions',
        notification_preferences: 'Weekly reports',

        knowledge_base: []
    });

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
            await api.onboarding.update(identity);
            setIdentityComplete(true);
            navigate('/chat');
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

    const updateField = (field, value) => {
        setIdentity(prev => ({ ...prev, [field]: value }));
    };

    return (
        <div className="flex flex-col h-screen bg-slate-50 p-8">
            <div className="max-w-5xl mx-auto w-full flex flex-col h-full bg-white rounded-[2rem] shadow-xl border border-slate-200 overflow-hidden">

                {/* Stepper Header */}
                <div className="bg-white border-b border-slate-100 p-10 text-slate-900">
                    <div className="flex justify-between items-center mb-10">
                        <div className="flex items-center gap-4">
                            <div className="p-3 bg-indigo-500 rounded-2xl shadow-lg shadow-indigo-500/30">
                                <Sparkles size={28} className="text-white" strokeWidth={1.5} />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold tracking-tight">Business Induction</h1>
                                <p className="text-slate-500 text-sm">Phase 4: Persistent Context Alignment</p>
                            </div>
                        </div>
                        <div className="text-right">
                            <span className="text-3xl font-black text-indigo-500">0{currentStep + 1}</span>
                            <span className="text-slate-400 text-sm ml-2">/ 0{STEPS.length}</span>
                        </div>
                    </div>

                    <div className="flex gap-8">
                        {STEPS.map((step, idx) => (
                            <div key={step.id} className={`flex-1 group cursor-pointer ${idx > currentStep ? 'opacity-40' : ''}`}>
                                <div className={`h-1.5 rounded-full mb-3 transition-all ${idx <= currentStep ? 'bg-indigo-500' : 'bg-slate-200'}`} />
                                <div className="flex items-center gap-3">
                                    <step.icon size={16} className={idx === currentStep ? 'text-indigo-500' : 'text-slate-400'} />
                                    <span className={`text-xs font-black uppercase tracking-widest ${idx === currentStep ? 'text-slate-900' : 'text-slate-400'}`}>
                                        {step.title}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Content Area */}
                <div ref={scrollContainerRef} className="flex-1 overflow-y-auto p-12 bg-slate-50">
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
                                <p className="text-slate-500">Provide these details to train your Orchestrator on your specific business DNA.</p>
                            </div>

                            {/* Step 1: Core */}
                            {currentStep === 0 && (
                                <div className="space-y-6">
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Your Name</label>
                                        <input
                                            type="text"
                                            value={identity.user_name}
                                            onChange={(e) => updateField('user_name', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-slate-900 placeholder-slate-400 shadow-sm"
                                            placeholder="e.g. Jane Doe"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Company Legal Name</label>
                                        <input
                                            type="text"
                                            value={identity.business_name}
                                            onChange={(e) => updateField('business_name', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-slate-900 placeholder-slate-400 shadow-sm"
                                            placeholder="e.g. Acme Innovations"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">What type of business are you running?</label>
                                        <select
                                            value={identity.business_type}
                                            onChange={(e) => updateField('business_type', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-slate-900 shadow-sm appearance-none"
                                        >
                                            <option value="" disabled>Select business type...</option>
                                            <option value="Coaching / Consulting">Coaching / Consulting</option>
                                            <option value="E-commerce / Online Store">E-commerce / Online Store</option>
                                            <option value="SaaS / Digital Products">SaaS / Digital Products</option>
                                            <option value="Freelancing / Services">Freelancing / Services</option>
                                            <option value="Content Creation / Media">Content Creation / Media</option>
                                            <option value="Agency / Marketing">Agency / Marketing</option>
                                            <option value="Not sure yet">Not sure yet</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">What stage is your business at right now?</label>
                                        <select
                                            value={identity.business_stage}
                                            onChange={(e) => updateField('business_stage', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-slate-900 shadow-sm appearance-none"
                                        >
                                            <option value="" disabled>Select business stage...</option>
                                            <option value="Just getting started (pre-launch)">Just getting started (pre-launch)</option>
                                            <option value="Recently launched (0-6 months)">Recently launched (0-6 months)</option>
                                            <option value="Growing (6 months - 2 years)">Growing (6 months - 2 years)</option>
                                            <option value="Established (2+ years)">Established (2+ years)</option>
                                            <option value="Scaling up (hiring, expanding)">Scaling up (hiring, expanding)</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Tell us about your business in your own words</label>
                                        <textarea
                                            value={identity.niche}
                                            onChange={(e) => updateField('niche', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all h-32 text-slate-900 placeholder-slate-400 shadow-sm"
                                            placeholder="A quick overview of what you do, who you serve, and what makes you unique."
                                        />
                                    </div>
                                </div>
                            )}

                            {/* Step 2: Audience */}
                            {currentStep === 1 && (
                                <div className="space-y-6">
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Who benefits the most from what you offer?</label>
                                        <select
                                            value={identity.audience_type}
                                            onChange={(e) => updateField('audience_type', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-slate-900 shadow-sm appearance-none"
                                        >
                                            <option value="" disabled>Select audience type...</option>
                                            <option value="Individual consumers (B2C)">Individual consumers (B2C)</option>
                                            <option value="Small businesses (B2B)">Small businesses (B2B)</option>
                                            <option value="Enterprise companies">Enterprise companies</option>
                                            <option value="Non-profits / Organizations">Non-profits / Organizations</option>
                                            <option value="Other creators / Freelancers">Other creators / Freelancers</option>
                                            <option value="Not sure yet">Not sure yet</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Do you already have a customer avatar?</label>
                                        <select
                                            value={identity.customer_avatar}
                                            onChange={(e) => updateField('customer_avatar', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-slate-900 shadow-sm appearance-none"
                                        >
                                            <option value="" disabled>Select option...</option>
                                            <option value="Yes, I have a detailed avatar">Yes, I have a detailed avatar</option>
                                            <option value="I have a rough idea">I have a rough idea</option>
                                            <option value="No, but I know my audience generally">No, but I know my audience generally</option>
                                            <option value="Not sure what that is">Not sure what that is</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">How big is your current audience or customer base?</label>
                                        <select
                                            value={identity.audience_size}
                                            onChange={(e) => updateField('audience_size', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-slate-900 shadow-sm appearance-none"
                                        >
                                            <option value="" disabled>Select size...</option>
                                            <option value="Just starting (0-10 people)">Just starting (0-10 people)</option>
                                            <option value="Small but growing (10-100 people)">Small but growing (10-100 people)</option>
                                            <option value="Moderate (100-1,000 people)">Moderate (100-1,000 people)</option>
                                            <option value="Large (1,000+ people)">Large (1,000+ people)</option>
                                            <option value="Not sure / Don't track this">Not sure / Don't track this</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">What's the biggest problem your audience struggles with?</label>
                                        <textarea
                                            value={identity.audience_problem}
                                            onChange={(e) => updateField('audience_problem', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none h-24 text-slate-900 placeholder-slate-400 shadow-sm"
                                            placeholder="Think about the pain that keeps them up at night."
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Ideal Client Description (Optional)</label>
                                        <textarea
                                            value={identity.icp_description}
                                            onChange={(e) => updateField('icp_description', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none h-32 text-slate-900 placeholder-slate-400 shadow-sm"
                                            placeholder="Describe your perfect customer in detail. Who are they? What do they value?"
                                        />
                                    </div>
                                </div>
                            )}

                            {/* Step 3: Brand */}
                            {currentStep === 2 && (
                                <div className="space-y-6">
                                    <div className="grid grid-cols-2 gap-6">
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Brand Voice & Tone</label>
                                            <select
                                                value={identity.brand_voice_tone}
                                                onChange={(e) => updateField('brand_voice_tone', e.target.value)}
                                                className="w-full bg-white border border-slate-200 p-4 rounded-2xl text-base focus:ring-2 focus:ring-indigo-500 outline-none text-slate-900 shadow-sm appearance-none"
                                            >
                                                <option value="" disabled>Select...</option>
                                                <option value="Professional and authoritative">Professional and authoritative</option>
                                                <option value="Friendly and approachable">Friendly and approachable</option>
                                                <option value="Playful and creative">Playful and creative</option>
                                                <option value="Inspirational and motivational">Inspirational and motivational</option>
                                                <option value="Expert and educational">Expert and educational</option>
                                                <option value="Casual and conversational">Casual and conversational</option>
                                                <option value="Luxury and premium">Luxury and premium</option>
                                                <option value="I'm not sure yet">I'm not sure yet</option>
                                            </select>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Brand Personality</label>
                                            <select
                                                value={identity.brand_personality}
                                                onChange={(e) => updateField('brand_personality', e.target.value)}
                                                className="w-full bg-white border border-slate-200 p-4 rounded-2xl text-base focus:ring-2 focus:ring-indigo-500 outline-none text-slate-900 shadow-sm appearance-none"
                                            >
                                                <option value="" disabled>Select...</option>
                                                <option value="Trustworthy and reliable">Trustworthy and reliable</option>
                                                <option value="Innovative and cutting-edge">Innovative and cutting-edge</option>
                                                <option value="Caring and supportive">Caring and supportive</option>
                                                <option value="Bold and confident">Bold and confident</option>
                                                <option value="Wise and experienced">Wise and experienced</option>
                                                <option value="Fun and energetic">Fun and energetic</option>
                                                <option value="Authentic and genuine">Authentic and genuine</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-2 gap-6">
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Core Values</label>
                                            <select
                                                value={identity.brand_values}
                                                onChange={(e) => updateField('brand_values', e.target.value)}
                                                className="w-full bg-white border border-slate-200 p-4 rounded-2xl text-base focus:ring-2 focus:ring-indigo-500 outline-none text-slate-900 shadow-sm appearance-none"
                                            >
                                                <option value="" disabled>Select...</option>
                                                <option value="Quality and excellence">Quality and excellence</option>
                                                <option value="Innovation and progress">Innovation and progress</option>
                                                <option value="Customer service and care">Customer service and care</option>
                                                <option value="Transparency and honesty">Transparency and honesty</option>
                                                <option value="Community and connection">Community and connection</option>
                                                <option value="Growth and empowerment">Growth and empowerment</option>
                                            </select>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">Brand Positioning</label>
                                            <select
                                                value={identity.brand_positioning}
                                                onChange={(e) => updateField('brand_positioning', e.target.value)}
                                                className="w-full bg-white border border-slate-200 p-4 rounded-2xl text-base focus:ring-2 focus:ring-indigo-500 outline-none text-slate-900 shadow-sm appearance-none"
                                            >
                                                <option value="" disabled>Select...</option>
                                                <option value="Premium/high-end option">Premium/high-end option</option>
                                                <option value="Affordable and accessible">Affordable and accessible</option>
                                                <option value="Innovative and cutting-edge">Innovative and cutting-edge</option>
                                                <option value="Traditional and reliable">Traditional and reliable</option>
                                                <option value="Personal and relationship-focused">Personal and relationship-focused</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">What makes your brand unique or different?</label>
                                        <textarea
                                            value={identity.brand_differentiation}
                                            onChange={(e) => updateField('brand_differentiation', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none h-24 text-slate-900 placeholder-slate-400 shadow-sm"
                                            placeholder="Your competitive advantage - what sets you apart from others in your space."
                                        />
                                    </div>
                                </div>
                            )}

                            {/* Step 4: Goals */}
                            {currentStep === 3 && (
                                <div className="space-y-6">
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">What's your #1 priority for the next 3 months?</label>
                                        <select
                                            value={identity.priority_3months}
                                            onChange={(e) => updateField('priority_3months', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-slate-900 shadow-sm appearance-none"
                                        >
                                            <option value="" disabled>Select priority...</option>
                                            <option value="Get more clients / customers">Get more clients / customers</option>
                                            <option value="Grow my revenue">Grow my revenue</option>
                                            <option value="Build a brand and community">Build a brand and community</option>
                                            <option value="Launch a new product or service">Launch a new product or service</option>
                                            <option value="Get more organized and efficient">Get more organized and efficient</option>
                                            <option value="Improve my marketing">Improve my marketing</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">What kind of support do you want Guild to give you first?</label>
                                        <select
                                            value={identity.guild_support_focus}
                                            onChange={(e) => updateField('guild_support_focus', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-slate-900 shadow-sm appearance-none"
                                        >
                                            <option value="" disabled>Select focus...</option>
                                            <option value="Content creation and strategy">Content creation and strategy</option>
                                            <option value="Marketing and campaigns">Marketing and campaigns</option>
                                            <option value="Lead nurturing and automation">Lead nurturing and automation</option>
                                            <option value="Closing sales and pipeline management">Closing sales and pipeline management</option>
                                            <option value="A bit of everything">A bit of everything</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">What's your biggest challenge right now?</label>
                                        <textarea
                                            value={identity.biggest_challenge}
                                            onChange={(e) => updateField('biggest_challenge', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none h-24 text-slate-900 placeholder-slate-400 shadow-sm"
                                            placeholder="Be specific - the more we understand, the better we can help."
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-black text-slate-500 uppercase tracking-widest ml-1">When you think about success 12 months from now, what would make you say 'this was worth it'?</label>
                                        <textarea
                                            value={identity.vision_12months}
                                            onChange={(e) => updateField('vision_12months', e.target.value)}
                                            className="w-full bg-white border border-slate-200 p-5 rounded-2xl text-lg focus:ring-2 focus:ring-indigo-500 outline-none h-24 text-slate-900 placeholder-slate-400 shadow-sm"
                                            placeholder="Paint a picture of your future."
                                        />
                                    </div>
                                </div>
                            )}

                            {/* Step 5: Archive */}
                            {currentStep === 4 && (
                                <div className="space-y-8">
                                    <div className="border-2 border-dashed border-slate-300 bg-slate-50 rounded-[2rem] p-12 text-center hover:border-indigo-400 transition-all cursor-pointer relative group">
                                        <input
                                            type="file"
                                            multiple
                                            onChange={handleFileUpload}
                                            className="absolute inset-0 opacity-0 cursor-pointer z-10"
                                        />
                                        <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-all">
                                            <Upload className="text-slate-400 group-hover:text-indigo-500" strokeWidth={1.5} />
                                        </div>
                                        <h3 className="text-xl font-bold text-slate-900 mb-2">Upload Business Intelligence</h3>
                                        <p className="text-slate-500">Brand guidelines, product catalogs, or internal strategy docs.</p>
                                    </div>

                                    {files.length > 0 && (
                                        <div className="space-y-3">
                                            {files.map((f, i) => (
                                                <div key={i} className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
                                                    <div className="flex items-center gap-3">
                                                        <Database size={18} className="text-indigo-500" strokeWidth={1.5} />
                                                        <span className="text-sm font-bold text-slate-700">{f.name}</span>
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
                        className="px-8 py-4 text-slate-500 font-black uppercase tracking-widest text-xs hover:text-slate-900 disabled:opacity-30 transition-all"
                    >
                        Back
                    </button>
                    <button
                        onClick={handleNext}
                        className="px-12 py-4 bg-[#1a6fff] text-white rounded-2xl font-black uppercase tracking-widest text-xs shadow-lg shadow-[#1a6fff]/30 hover:bg-[#0055ff] transition-all flex items-center gap-3 group"
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
