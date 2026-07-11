import os

old_path = "/tmp/old_onboarding.jsx"
new_path = "/Users/arnovanzyl/Dropbox/Mac (2)/Documents/GitHub/Guild-AI-New/services/web/src/components/onboarding/OnboardingFlow.jsx"

with open(old_path, "r") as f:
    old_content = f.read()

# Replace 'const OnboardingFlow = () => {' with 'const QuickForm = ({ forceNext }) => {'
# But QuickForm needs useAuth, navigate, etc. The original OnboardingFlow uses its own state.
# We can just rename OnboardingFlow to QuickForm and remove 'export default OnboardingFlow;'
new_quickform = old_content.replace("const OnboardingFlow = () => {", "const QuickForm = ({ onToggle }) => {")
new_quickform = new_quickform.replace("export default OnboardingFlow;", "")

# We need to inject the new Induction component at the bottom of the file
induction_code = """

// --- THE INDUCTION (Phase 3 Conversational Flow) ---

import { Send, MessageSquare, ArrowRight, CheckCircle, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const TheInduction = () => {
    const { setIdentityComplete } = useAuth();
    const navigate = useNavigate();
    const [useQuickForm, setUseQuickForm] = useState(false);
    
    const [history, setHistory] = useState([
        { role: 'assistant', content: "Hi, I'm Guild. Before I can build your marketing engine, I want to actually understand your business — this is a conversation, not a form. First things first: what's your name, and does your business have a website?" }
    ]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    
    const [statusData, setStatusData] = useState(null);
    const [finaleMode, setFinaleMode] = useState(false);
    const [finaleLoading, setFinaleLoading] = useState(false);
    const [finalePost, setFinalePost] = useState(null);
    
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [history, isTyping]);

    const pollStatus = async () => {
        try {
            const data = await api.onboarding.status();
            setStatusData(data);
        } catch (err) {
            console.error("Status poll failed", err);
        }
    };

    useEffect(() => {
        pollStatus();
        const interval = setInterval(pollStatus, 5000);
        return () => clearInterval(interval);
    }, []);

    const sendMessage = async (textOverride) => {
        const text = textOverride || input.trim();
        if (!text) return;
        
        const newHistory = [...history, { role: 'user', content: text }];
        setHistory(newHistory);
        setInput('');
        setIsTyping(true);

        try {
            const response = await api.onboarding.chat(text, newHistory);
            
            // The response might be just text or have coach_mode boolean etc.
            // But api.onboarding.chat returns OnboardingResponse
            const replyMsg = response.message || response.reply || response;
            const isCoach = response.coach_mode || false;
            
            const assistMsg = { role: 'assistant', content: typeof replyMsg === 'string' ? replyMsg : replyMsg.message || "Okay.", coach_mode: isCoach };
            setHistory([...newHistory, assistMsg]);
            
            if (response.onboarding_complete) {
                setFinaleMode(true);
            }
            pollStatus(); // Immediate poll on reply
        } catch (err) {
            setHistory([...newHistory, { role: 'assistant', content: "Sorry, I had trouble understanding that." }]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleFinale = async () => {
        setFinaleLoading(true);
        try {
            const res = await api.onboarding.finale();
            if (res.skipped) {
                setIdentityComplete(true);
                navigate('/chat');
            } else {
                setFinalePost(res);
            }
        } catch (err) {
            console.error("Finale failed", err);
            setIdentityComplete(true);
            navigate('/chat');
        } finally {
            setFinaleLoading(false);
        }
    };

    const finishOnboarding = () => {
        setIdentityComplete(true);
        navigate('/chat');
    };

    if (useQuickForm) {
        return (
            <div className="min-h-screen bg-slate-50 flex flex-col items-center pt-10">
                <div className="w-full max-w-4xl px-4">
                    <button onClick={() => setUseQuickForm(false)} className="text-sm text-indigo-500 mb-4 hover:underline">
                        &larr; Back to Conversation
                    </button>
                    <QuickForm />
                </div>
            </div>
        );
    }

    if (finaleMode) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
                <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="max-w-2xl w-full bg-white rounded-[2rem] p-10 shadow-xl text-center">
                    {!finaleLoading && !finalePost ? (
                        <div className="space-y-6">
                            <Sparkles className="w-16 h-16 text-indigo-500 mx-auto" />
                            <h2 className="text-3xl font-black text-slate-900">One last thing...</h2>
                            <p className="text-slate-600 text-lg">Want to see what I can already do with everything you've just told me?</p>
                            <button onClick={handleFinale} className="px-8 py-4 bg-indigo-600 text-white rounded-2xl font-black uppercase tracking-widest text-sm shadow-lg shadow-indigo-500/30 hover:bg-indigo-700 transition-all">
                                Show me
                            </button>
                        </div>
                    ) : finaleLoading ? (
                        <div className="space-y-6 py-12">
                            <Loader2 className="w-12 h-12 text-indigo-500 mx-auto animate-spin" />
                            <p className="text-slate-600 text-lg font-medium animate-pulse">Writing something in your voice...</p>
                        </div>
                    ) : (
                        <div className="space-y-8 text-left">
                            <div className="text-center space-y-2 mb-8">
                                <h2 className="text-2xl font-black text-slate-900">This is what working together looks like.</h2>
                                <p className="text-slate-500">This is already in your Content Queue.</p>
                            </div>
                            
                            <div className="p-6 bg-slate-50 border border-slate-200 rounded-2xl shadow-inner">
                                <div className="flex justify-between items-start mb-4">
                                    <h3 className="font-bold text-lg text-slate-900">{finalePost.title || "Sample Post"}</h3>
                                    {finalePost.judge_score && (
                                        <span className="px-3 py-1 bg-emerald-100 text-emerald-700 text-xs font-bold uppercase tracking-widest rounded-full">
                                            Score: {finalePost.judge_score}/100
                                        </span>
                                    )}
                                </div>
                                <div className="prose prose-sm text-slate-700">
                                    <ReactMarkdown>{finalePost.body || finalePost.content || ""}</ReactMarkdown>
                                </div>
                            </div>

                            <div className="text-center">
                                <button onClick={finishOnboarding} className="px-10 py-4 bg-slate-900 text-white rounded-2xl font-black uppercase tracking-widest text-sm shadow-xl hover:scale-105 transition-all">
                                    Enter Guild
                                </button>
                            </div>
                        </div>
                    )}
                </motion.div>
            </div>
        );
    }

    // Main layout
    return (
        <div className="min-h-screen bg-white flex flex-col md:flex-row overflow-hidden">
            
            {/* LEFT: Conversation Stage */}
            <div className="flex-1 flex flex-col h-screen max-w-3xl mx-auto border-r border-slate-100 relative shadow-2xl z-10 bg-white">
                <div className="p-6 border-b border-slate-100 flex items-center gap-3">
                    <div className="w-10 h-10 bg-indigo-100 rounded-xl flex items-center justify-center">
                        <Sparkles className="text-indigo-600" size={20} />
                    </div>
                    <div>
                        <h1 className="font-black text-slate-900">The Induction</h1>
                        <p className="text-xs text-slate-500 font-medium uppercase tracking-widest">Brand alignment in progress</p>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                    {history.map((msg, i) => (
                        <motion.div key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} 
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-[85%] rounded-2xl p-4 ${msg.role === 'user' ? 'bg-slate-900 text-white rounded-br-none' : 'bg-slate-50 text-slate-800 rounded-bl-none border border-slate-200'} ${msg.coach_mode ? 'border-amber-300 bg-amber-50/50' : ''}`}>
                                {msg.coach_mode && (
                                    <div className="flex items-center gap-1 mb-2 text-[10px] uppercase tracking-widest font-bold text-amber-600">
                                        <Sparkles size={10} /> Coaching
                                    </div>
                                )}
                                <div className="prose prose-sm leading-relaxed prose-p:my-1">
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                    {isTyping && (
                        <div className="flex justify-start">
                            <div className="bg-slate-50 border border-slate-200 rounded-2xl rounded-bl-none p-4 flex gap-1">
                                <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" />
                                <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce delay-75" />
                                <span className="w-2 h-2 bg-slate-300 rounded-full animate-bounce delay-150" />
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <div className="p-4 border-t border-slate-100 bg-white">
                    <div className="flex gap-2 mb-2">
                        <input 
                            type="text" 
                            value={input} 
                            onChange={e => setInput(e.target.value)}
                            onKeyDown={e => e.key === 'Enter' && sendMessage()}
                            placeholder="Type your response..."
                            className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-indigo-500 transition-all text-slate-900"
                            disabled={isTyping}
                        />
                        <button onClick={() => sendMessage()} disabled={isTyping || !input.trim()} className="bg-indigo-600 text-white p-3 rounded-xl hover:bg-indigo-700 transition-colors disabled:opacity-50">
                            <Send size={20} />
                        </button>
                    </div>
                    
                    <div className="flex justify-between items-center px-1">
                        <button onClick={() => sendMessage("I'm not sure")} disabled={isTyping} className="text-xs font-bold text-slate-500 hover:text-indigo-600 transition-colors px-2 py-1 rounded-md hover:bg-indigo-50">
                            I'm not sure — help me
                        </button>
                        <button onClick={() => setUseQuickForm(true)} className="text-xs text-slate-400 hover:text-slate-600 underline">
                            Prefer a quick form instead?
                        </button>
                    </div>
                </div>
            </div>

            {/* RIGHT: Brand Profile Card */}
            <div className="hidden md:flex flex-col w-[340px] bg-slate-50 border-l border-slate-200 h-screen overflow-y-auto p-6">
                <div className="mb-6 text-center">
                    <div className="relative w-24 h-24 mx-auto mb-3">
                        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="45" fill="none" stroke="#e2e8f0" strokeWidth="8" />
                            <motion.circle 
                                cx="50" cy="50" r="45" fill="none" stroke="#4f46e5" strokeWidth="8"
                                strokeDasharray="283"
                                animate={{ strokeDashoffset: 283 - (283 * (statusData?.completion_percentage || 0)) }}
                                transition={{ duration: 1 }}
                            />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center flex-col">
                            <span className="font-black text-xl text-slate-900">{Math.round((statusData?.completion_percentage || 0) * 100)}%</span>
                        </div>
                    </div>
                    <h3 className="font-bold text-slate-900">Brand Profile</h3>
                    <p className="text-xs text-slate-500">Building live...</p>
                </div>

                <div className="space-y-4">
                    <ProfileSection 
                        title="Business Core" 
                        items={[
                            { label: 'Name', value: statusData?.identity_data?.business_name, field: 'business_name' },
                            { label: 'Website', value: statusData?.identity_data?.website_url, field: 'website_url' },
                            { label: 'Niche', value: statusData?.identity_data?.niche, field: 'niche' }
                        ]} 
                        ledger={statusData?.knowledge_ledger} 
                    />
                    
                    <ProfileSection 
                        title="Ideal Customer" 
                        items={[
                            { label: 'Audience', value: statusData?.identity_data?.target_audience, field: 'target_audience' },
                            { label: 'Problem', value: statusData?.identity_data?.audience_problem, field: 'audience_problem' }
                        ]} 
                        ledger={statusData?.knowledge_ledger} 
                    />

                    <ProfileSection 
                        title="Voice & Tone" 
                        items={[
                            { label: 'Tone', value: statusData?.identity_data?.brand_voice_tone, field: 'brand_voice_tone' },
                            { label: 'Personality', value: statusData?.identity_data?.brand_personality, field: 'brand_personality' }
                        ]} 
                        ledger={statusData?.knowledge_ledger} 
                    />

                    {statusData?.brand_style_guide && (
                        <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
                            <h4 className="text-xs font-black uppercase tracking-widest text-slate-500 mb-2">Visual Style</h4>
                            <div className="flex flex-wrap gap-2">
                                {/* Parse hex codes from style guide */}
                                {(statusData.brand_style_guide.match(/#[0-9A-Fa-f]{6}/g) || []).slice(0, 5).map((hex, i) => (
                                    <div key={i} className="w-6 h-6 rounded-md shadow-sm border border-slate-200" style={{ backgroundColor: hex }} title={hex} />
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
            
        </div>
    );
};

const ProfileSection = ({ title, items, ledger = {} }) => {
    return (
        <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
            <h4 className="text-xs font-black uppercase tracking-widest text-slate-500 mb-3">{title}</h4>
            <div className="space-y-3">
                {items.map((item, idx) => {
                    const statusObj = ledger[item.field] || {};
                    const status = statusObj.status;
                    const isFilled = !!item.value;

                    return (
                        <div key={idx} className="relative">
                            <div className="text-[10px] uppercase font-bold text-slate-400 mb-0.5">{item.label}</div>
                            {isFilled ? (
                                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-sm font-medium text-slate-800 line-clamp-2">
                                    {item.value}
                                </motion.div>
                            ) : (
                                <div className="text-sm text-slate-300 italic">Not yet discussed</div>
                            )}
                            
                            {status === 'flagged' && (
                                <div className="mt-1 inline-block px-2 py-0.5 bg-amber-100 text-amber-700 text-[9px] font-bold uppercase rounded-sm">
                                    Exploring Later
                                </div>
                            )}
                            {status === 'coached' && (
                                <div className="absolute right-0 top-1 text-indigo-400" title="Coached">
                                    <Sparkles size={12} />
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Object.assign(TheInduction, { QuickForm });

"""

# Let's fix the duplicate imports from induction_code and QuickForm.
# Actually, since induction_code is appended to QuickForm, QuickForm already has imports at the top.
# We should remove the React/Framer imports from induction_code and make sure we don't duplicate them.
# The `import ReactMarkdown from 'react-markdown';` can be prepended at the top.

final_code = "import ReactMarkdown from 'react-markdown';\n" + new_quickform + induction_code

with open(new_path, "w") as f:
    f.write(final_code)
print("File updated successfully.")
