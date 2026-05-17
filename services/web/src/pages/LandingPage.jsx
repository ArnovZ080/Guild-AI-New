import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import ZARPrice from '@/components/ui/ZARPrice'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Check, ArrowRight, Sparkles, Shield, TrendingUp, 
  Users, Zap, Brain, Target, Award, Calculator, 
  GitBranch, MessageSquare, Play, Layout, Rocket
} from 'lucide-react'
import { motion } from 'framer-motion'
import guildLogo from '@/assets/guild-logo.png'

function LandingPage() {
    const navigate = useNavigate();
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const growthSteps = [
        { title: 'LEARN', description: 'Tell Guild about your business in a natural conversation. It remembers your voice, your audience, your goals — and gets smarter every cycle.', icon: <Brain />, color: 'from-blue-600 to-indigo-600' },
        { title: 'CREATE', description: 'Blog posts, social content, reels, emails, and ad creatives — written and designed in your exact brand voice. Quality-checked before you see them.', icon: <Sparkles />, color: 'from-blue-600 to-indigo-600' },
        { title: 'PUBLISH', description: 'Your content goes live at the optimal time on every connected platform. Automatically. Every week. Without you scheduling a single post.', icon: <Layout />, color: 'from-blue-600 to-indigo-600' },
        { title: 'ATTRACT', description: 'People discover your business through content Guild creates — across social, search, and email. You show up consistently without lifting a finger.', icon: <Target />, color: 'from-blue-600 to-indigo-600' },
        { title: 'CAPTURE', description: 'When someone engages, Guild adds them to your CRM and scores how likely they are to buy. No lead falls through the cracks.', icon: <Users />, color: 'from-blue-600 to-indigo-600' },
        { title: 'NURTURE', description: 'Personalised follow-up sequences keep the conversation going until they are ready to buy. Written in your voice. Sent at the right moment.', icon: <MessageSquare />, color: 'from-blue-600 to-indigo-600' },
        { title: 'CONVERT', description: 'Guild tracks what content drives real sales and does more of it. Every cycle, the system gets smarter about your business and your buyers.', icon: <Rocket />, color: 'from-blue-600 to-indigo-600' },
    ];

    const plans = [
        {
            name: 'Starter',
            price: '$39',
            regularPrice: '$49',
            description: 'Start your growth engine. Content created, published, and on-brand — without the agency fee.',
            features: [
                'Personalised business onboarding',
                '50 content pieces per month',
                'Blog posts, social media & images',
                '3 connected platforms',
                'Quality checks on every piece',
                'Pre-built marketing templates'
            ],
            cta: 'Claim Founding Access',
            popular: false
        },
        {
            name: 'Growth',
            price: '$119',
            regularPrice: '$149',
            description: 'The full loop. Create, publish, capture leads, and nurture them to purchase — automatically.',
            features: [
                'Everything in Starter',
                '200 content pieces per month',
                '10 AI-generated videos',
                'Unlimited connected platforms',
                'Built-in CRM & lead capture',
                'Automated nurture sequences',
                'Facebook & Instagram ad designs'
            ],
            cta: 'Claim Founding Access',
            popular: true
        },
        {
            name: 'Scale',
            price: '$239',
            regularPrice: '$299',
            description: 'Run multiple brands or client accounts from one place. Agency power at a founder\'s price.',
            features: [
                'Everything in Growth',
                '500 content pieces per month',
                '30 AI-generated videos',
                'Custom workflow builder',
                'A/B testing on content & ads',
                'White-label for client brands',
                'Priority support'
            ],
            cta: 'Talk to Arno',
            popular: false
        }
    ];

    const handleSignup = (planName) => {
        navigate(`/signup?plan=${planName.toLowerCase()}`)
    }

    return (
        <div className="min-h-screen bg-transparent text-white selection:bg-indigo-500/30">
            {/* Nav */}
            <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'py-3 backdrop-blur-md bg-zinc-950/50 border-b border-white/5' : 'py-6'}`}>
                <div className="container mx-auto px-6 flex items-center justify-between max-w-7xl">
                    <div className="flex items-center gap-3">
                        <img src={guildLogo} alt="Guild" className="w-9 h-9 border border-white/10 rounded-lg shadow-2xl" />
                        <span className="text-xl font-bold tracking-tight font-heading">Guild <span className="text-indigo-400">AI</span></span>
                    </div>
                    <div className="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-400">
                        <Link to="/how-it-works" className="hover:text-white transition-colors">How It Works</Link>
                        <Link to="/features" className="hover:text-white transition-colors">Features</Link>
                        <Link to="/pricing" className="hover:text-white transition-colors">Pricing</Link>
                        <Link to="/about" className="hover:text-white transition-colors">About</Link>
                    </div>
                    <div className="flex items-center gap-4">
                        <Link to="/login" className="text-sm font-medium text-zinc-400 hover:text-white px-4 py-2">Login</Link>
                        <Button className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-6 shadow-xl shadow-indigo-500/20 border-t border-white/20" onClick={() => navigate('/waitlist')}>
                            Claim Founding Access
                        </Button>
                    </div>
                </div>
            </nav>

            {/* Hero */}
            <section className="pt-44 pb-24 px-6 relative overflow-hidden">
                <div className="container mx-auto max-w-6xl text-center relative z-10">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <Badge className="mb-6 bg-white/5 text-indigo-300 border border-white/10 px-4 py-1 flex items-center gap-2 w-fit mx-auto backdrop-blur-sm">
                            <Sparkles size={14} className="animate-pulse" />
                            Founding Member Access — 50 spots. First come, first locked.
                        </Badge>
                        <h1 className="text-6xl md:text-8xl font-bold font-heading leading-[1.1] tracking-tight mb-8">
                            Guild knows your business, <br />
                            <span className="text-gradient-cobalt">finds your customers,</span> <br />
                            and turns them into buyers.
                        </h1>
                        <p className="text-xl text-zinc-400 max-w-3xl mx-auto mb-3 leading-relaxed font-light font-bold">
                            You're paying for 6 different tools. And still doing all the work yourself.
                        </p>
                        <p className="text-xl text-zinc-400 max-w-3xl mx-auto mb-10 leading-relaxed font-light">
                            Guild replaces them with one system that creates your content, publishes it at the right time, captures every lead who engages, and nurtures them into customers — without you doing any of it manually.
                        </p>
                        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                            <Button size="lg" className="bg-white text-black hover:bg-zinc-200 rounded-full px-10 py-7 text-lg font-bold transition-all hover:scale-105 active:scale-95" onClick={() => navigate('/waitlist')}>
                                Claim Founding Access <ArrowRight className="ml-2 text-indigo-600" />
                            </Button>
                            <Button size="lg" variant="ghost" className="text-zinc-400 hover:text-indigo-400 rounded-full px-8 py-7 text-lg group">
                                <Play className="mr-2 fill-indigo-400/50 group-hover:fill-indigo-400 transition-all shadow-glow-sm" size={18} /> See How It Works
                            </Button>
                        </div>
                    </motion.div>
                </div>

                {/* Glass Mockup Preview / Theater */}
                <div className="container mx-auto max-w-6xl mt-20 relative px-4">
                    <div className="glass-panel p-2 rounded-2xl border border-white/10 shadow-3xl overflow-hidden aspect-video relative group">
                        <div className="w-full h-full bg-transparent rounded-xl relative overflow-hidden flex flex-col">
                           <div className="absolute top-4 left-4 flex gap-2 z-20">
                               <div className="w-2.5 h-2.5 rounded-full bg-white/20" />
                               <div className="w-2.5 h-2.5 rounded-full bg-white/10" />
                               <div className="w-2.5 h-2.5 rounded-full bg-white/5" />
                           </div>
                           
                           {/* Simulated Activity Feed */}
                           <div className="flex-1 p-8 pt-12 font-mono text-xs overflow-hidden">
                               <AgentSimulatedLogs />
                           </div>

                           <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20 group-hover:opacity-40 transition-opacity">
                               <div className="text-center">
                                   <div className="w-32 h-32 rounded-full border border-indigo-500/30 flex items-center justify-center mb-4 animate-pulse">
                                       <GitBranch className="text-indigo-400" size={48} />
                                   </div>
                               </div>
                           </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="py-24 px-6 border-y border-white/5 relative overflow-hidden">
                <div className="container mx-auto max-w-7xl relative z-10">
                    <div className="text-center mb-20">
                        <h2 className="text-4xl md:text-5xl font-bold font-heading mb-6 tracking-tight">The Only Platform That Closes the Full Loop</h2>
                        <p className="text-zinc-400 max-w-2xl mx-auto text-lg leading-relaxed">
                            Most tools help you create content and leave the rest to you. Guild creates it, publishes it, captures everyone who engages, and turns them into paying customers — as one connected system.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-7 gap-4">
                        {growthSteps.map((step, i) => (
                            <motion.div 
                                key={i}
                                whileHover={{ y: -5 }}
                                className="glass-panel p-6 rounded-2xl flex flex-col items-center text-center group cursor-default"
                            >
                                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${step.color} flex items-center justify-center text-white mb-6 shadow-lg shadow-indigo-500/10 group-hover:scale-110 transition-transform`}>
                                    {step.icon}
                                </div>
                                <h3 className="text-sm font-bold font-heading tracking-[0.2em] mb-3 text-zinc-100 uppercase">{step.title}</h3>
                                <p className="text-sm text-zinc-400 leading-relaxed font-light">{step.description}</p>
                            </motion.div>
                        ))}
                    </div>
                    
                    {/* Trust signal */}
                    <div className="mt-16 text-center">
                        <p className="text-sm font-bold uppercase tracking-[0.2em] text-indigo-400/70">Beta cohort now open — founding member spots filling fast</p>
                    </div>

                    <div className="mt-10 flex justify-center gap-8 items-center flex-wrap opacity-60 hover:opacity-100 transition-all duration-700">
                        <span className="text-xs font-bold uppercase tracking-[0.3em] text-indigo-500/50 block w-full text-center mb-8">Connects with the tools you already use</span>
                        <div className="px-8 py-2 border border-indigo-500/10 rounded-full text-zinc-400 font-heading hover:border-indigo-500/30 transition-colors">Instagram</div>
                        <div className="px-8 py-2 border border-indigo-500/10 rounded-full text-zinc-400 font-heading hover:border-indigo-500/30 transition-colors">LinkedIn</div>
                        <div className="px-8 py-2 border border-indigo-500/10 rounded-full text-zinc-400 font-heading hover:border-indigo-500/30 transition-colors">Facebook</div>
                        <div className="px-8 py-2 border border-indigo-500/10 rounded-full text-zinc-400 font-heading hover:border-indigo-500/30 transition-colors">Mailchimp</div>
                        <div className="px-8 py-2 border border-indigo-500/10 rounded-full text-zinc-400 font-heading hover:border-indigo-500/30 transition-colors">Shopify</div>
                        <div className="px-8 py-2 border border-indigo-500/10 rounded-full text-zinc-400 font-heading hover:border-indigo-500/30 transition-colors">Google Ads</div>
                    </div>
                </div>
            </section>

            {/* Differentiators */}
            <section className="py-32 px-6">
                <div className="container mx-auto max-w-6xl">
                    <div className="grid lg:grid-cols-2 gap-20 items-center">
                        <div className="relative">
                            <div className="absolute -inset-20 bg-indigo-500/5 blur-[100px] rounded-full" />
                            <h2 className="text-4xl md:text-5xl font-bold font-heading mb-8 relative">
                                What Makes <br /> <span className="text-indigo-400">Guild Different</span>
                            </h2>
                            <div className="space-y-8 relative">
                                <div className="flex gap-6">
                                    <div className="w-12 h-12 rounded-xl border border-white/10 glass-panel flex items-center justify-center shrink-0 text-indigo-400 shadow-glow-sm">
                                        <Shield size={22} strokeWidth={1.5} />
                                    </div>
                                    <div>
                                        <h4 className="text-xl font-bold mb-2 font-heading">Content That Checks Itself Before You See It</h4>
                                        <p className="text-base text-zinc-400 leading-relaxed font-light">Before any content reaches you, Guild has already checked it against your brand voice, your ideal customer profile, your SEO requirements, and your factual accuracy standards. You only review what's already worth approving. No generic AI output. No off-brand mistakes. No other platform does this.</p>
                                    </div>
                                </div>
                                <div className="flex gap-6">
                                    <div className="w-12 h-12 rounded-xl border border-white/10 glass-panel flex items-center justify-center shrink-0 text-indigo-400 shadow-glow-sm">
                                        <Layout size={22} strokeWidth={1.5} />
                                    </div>
                                    <div>
                                        <h4 className="text-xl font-bold mb-2 font-heading">Posts When Your Audience Is Actually Watching</h4>
                                        <p className="text-base text-zinc-400 leading-relaxed font-light">Guild learns when your followers are most active and schedules your content automatically. It syncs with your calendar so nothing clashes with your meetings or personal time. The longer you use it, the smarter the scheduling gets.</p>
                                    </div>
                                </div>
                                <div className="flex gap-6">
                                    <div className="w-12 h-12 rounded-xl border border-white/10 glass-panel flex items-center justify-center shrink-0 text-indigo-400 shadow-glow-sm">
                                        <Award size={22} strokeWidth={1.5} />
                                    </div>
                                    <div>
                                        <h4 className="text-xl font-bold mb-2 font-heading">Gets Smarter the Longer You Use It</h4>
                                        <p className="text-base text-zinc-400 leading-relaxed font-light">Content that performs well shapes the next campaign. Leads that convert refine who gets targeted next. Guild builds a deep understanding of your business over time — making it more valuable every month, and making switching feel pointless.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="glass-panel p-10 rounded-2xl relative border border-white/10">
                            <h3 className="text-2xl font-bold font-heading mb-8">The Math Is Simple</h3>
                            <div className="space-y-6 mb-10">
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-zinc-400 uppercase tracking-widest">Content creation (Jasper)</span>
                                    <span className="font-medium">$59/mo</span>
                                </div>
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-zinc-400 uppercase tracking-widest">Scheduling (Buffer)</span>
                                    <span className="font-medium">$30/mo</span>
                                </div>
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-zinc-400 uppercase tracking-widest">Email marketing (Mailchimp)</span>
                                    <span className="font-medium">$50/mo</span>
                                </div>
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-zinc-400 uppercase tracking-widest">CRM (HubSpot Starter)</span>
                                    <span className="font-medium">$50/mo</span>
                                </div>
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-zinc-400 uppercase tracking-widest">Design (Canva Pro)</span>
                                    <span className="font-medium">$15/mo</span>
                                </div>
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-zinc-400 uppercase tracking-widest">Freelance writer</span>
                                    <span className="font-medium">$300/mo</span>
                                </div>
                                <div className="pt-6 border-t border-white/10 flex justify-between items-center">
                                    <span className="text-zinc-400 font-bold uppercase tracking-[0.2em] text-xs">Your current marketing stack</span>
                                    <div className="text-right">
                                        <span className="text-2xl font-bold text-red-500">$504/mo</span>
                                        <ZARPrice usd={504} className="text-red-400/50 text-xs" />
                                    </div>
                                </div>
                                <p className="text-xs text-zinc-600 italic mt-2">(and you still do all the work yourself)</p>
                            </div>
                            <div className="p-8 gradient-cobalt rounded-xl text-center shadow-3xl">
                                <span className="text-xs uppercase tracking-[0.3em] font-bold text-white/70">Guild AI — Founding Member Rate</span>
                                <div className="text-5xl font-black mt-2">$119/mo</div>
                                <ZARPrice usd={119} className="text-white/50 text-sm" />
                                <p className="text-xs mt-1 font-medium text-white/40 line-through tracking-tighter">Regular price $149/mo</p>
                                <p className="text-xs mt-3 font-medium text-white/60 tracking-tighter italic">Founding rate locked in permanently</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Pricing */}
            <section className="py-24 px-6">
                <div className="container mx-auto max-w-6xl">
                    <div className="text-center mb-6">
                        <h2 className="text-4xl md:text-5xl font-bold font-heading mb-6 tracking-tight">Founding Member Pricing.</h2>
                        <p className="text-zinc-400 max-w-xl mx-auto">Lock in your rate before public launch. One system replaces 6+ tools — and does the work for you.</p>
                    </div>

                    {/* Founding member banner */}
                    <div className="mb-10 p-4 rounded-2xl border border-indigo-500/30 bg-indigo-500/5 flex items-center justify-center gap-3 text-sm max-w-2xl mx-auto">
                        <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse shrink-0" />
                        <span className="text-indigo-300 font-medium">Founding members lock in today's rate permanently — it never increases, even when public pricing does.</span>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        {plans.map((p, i) => (
                            <div key={i} className={`glass-panel p-10 rounded-3xl relative flex flex-col ${p.popular ? 'border-indigo-500/50 scale-105 z-10 shadow-2xl shadow-indigo-500/10' : 'border-white/10'}`}>
                                {p.popular && <Badge className="absolute -top-4 left-1/2 -translate-x-1/2 bg-indigo-600 text-white font-bold border-none">MOST POPULAR</Badge>}
                                <h3 className="text-2xl font-bold font-heading mb-1">{p.name}</h3>
                                <div className="flex items-baseline gap-2 mb-1">
                                    <span className="text-5xl font-black">{p.price}</span>
                                    <span className="text-zinc-400 text-sm">/mo</span>
                                    <span className="text-zinc-600 text-sm line-through">{p.regularPrice}</span>
                                </div>
                                <ZARPrice usd={parseInt(p.price.replace('$', ''))} className="mb-1" />
                                <p className="text-xs text-indigo-400/70 font-medium mb-5 uppercase tracking-widest">Founding rate — locked for life</p>
                                <p className="text-zinc-400 text-sm mb-8">{p.description}</p>
                                <Button 
                                    className={`w-full py-7 rounded-2xl mb-10 text-lg font-bold ${p.popular ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-xl shadow-indigo-500/20 active:scale-95' : 'bg-white/5 hover:bg-white/10 text-white'}`} 
                                    onClick={() => p.name === 'Scale' ? navigate('/contact') : navigate('/waitlist')}
                                >
                                    {p.cta}
                                </Button>
                                <ul className="space-y-4 flex-1">
                                    {p.features.map((f, fi) => (
                                        <li key={fi} className="flex items-center text-sm text-zinc-400 gap-3">
                                            <div className="w-5 h-5 rounded-full bg-indigo-500/10 flex items-center justify-center shrink-0">
                                                <Check size={12} className="text-indigo-400" strokeWidth={3} />
                                            </div>
                                            {f}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>

                    {/* Guarantee */}
                    <div className="mt-12 text-center">
                        <p className="text-zinc-500 text-sm max-w-lg mx-auto leading-relaxed">
                            <span className="text-zinc-300 font-medium">30-day guarantee:</span> Publish a full month of content and capture your first leads. If you don't, your first month is refunded. Email Arno directly.
                        </p>
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section className="py-32 px-6">
                <div className="container mx-auto max-w-5xl">
                    <div className="glass-panel p-20 rounded-3xl relative border border-white/10 shadow-glow text-center overflow-hidden">
                        <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-transparent pointer-events-none" />
                        <motion.div
                            initial={{ scale: 0.95, opacity: 0 }}
                            whileInView={{ scale: 1, opacity: 1 }}
                            transition={{ duration: 0.6 }}
                            viewport={{ once: true }}
                        >
                            <h2 className="text-5xl md:text-6xl font-black font-heading tracking-tight mb-8">
                                Your content-to-customer <br /> <span className="text-indigo-400 underline decoration-indigo-500/30">engine is ready.</span>
                            </h2>
                            <p className="text-xl text-zinc-400 max-w-2xl mx-auto mb-4 leading-relaxed">
                                Guild creates your content, publishes it automatically, captures every lead who engages, and nurtures them into buyers. You approve and watch your business grow.
                            </p>
                            <p className="text-sm text-indigo-300/70 mb-12 font-medium">
                                Founding members lock in today's rate permanently. 50 spots. Rate increases at public launch.
                            </p>
                            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
                                <Button size="lg" className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-12 py-8 text-xl font-bold shadow-2xl shadow-indigo-500/20" onClick={() => navigate('/waitlist')}>
                                    Claim Your Founding Rate →
                                </Button>
                            </div>
                            <p className="mt-8 text-zinc-400 text-sm italic">Your data is yours. Cancel anytime. No lock-in contracts.</p>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-20 px-6 border-t border-white/5 bg-zinc-950/20 backdrop-blur-3xl">
                <div className="container mx-auto max-w-7xl">
                    <div className="grid md:grid-cols-4 gap-12 mb-16">
                        <div className="col-span-1 md:col-span-1">
                            <div className="flex items-center gap-3 mb-6">
                                <img src={guildLogo} alt="Guild" className="w-8 h-8 rounded-md grayscale opacity-50" />
                                <span className="font-bold tracking-tight text-white/50 underline decoration-white/10 uppercase text-sm">Guild AI</span>
                            </div>
                            <p className="text-zinc-600 text-sm leading-relaxed">
                                The only platform that turns content into customers — automatically.
                            </p>
                        </div>
                        <div>
                            <h4 className="font-heading font-black text-xs tracking-widest uppercase text-zinc-400 mb-8">Product</h4>
                            <ul className="space-y-4 text-sm font-medium text-zinc-400">
                                <li><Link to="/features" className="hover:text-indigo-400 transition-colors">Features</Link></li>
                                <li><Link to="/how-it-works" className="hover:text-indigo-400 transition-colors">How It Works</Link></li>
                                <li><Link to="/integrations" className="hover:text-indigo-400 transition-colors">Integrations</Link></li>
                                <li><Link to="/pricing" className="hover:text-indigo-400 transition-colors">Pricing</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-heading font-black text-xs tracking-widest uppercase text-zinc-400 mb-8">Company</h4>
                            <ul className="space-y-4 text-sm font-medium text-zinc-400">
                                <li><Link to="/about" className="hover:text-white transition-colors">Our Vision</Link></li>
                                <li><Link to="/affiliates" className="hover:text-white transition-colors">Affiliate Program</Link></li>
                                <li><Link to="/contact" className="hover:text-white transition-colors">Support & Contact</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-heading font-black text-xs tracking-widest uppercase text-zinc-400 mb-8">Legal</h4>
                            <ul className="space-y-4 text-sm font-medium text-zinc-400">
                                <li><Link to="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                                <li><Link to="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
                                <li><Link to="/refund" className="hover:text-white transition-colors">Refund Policy</Link></li>
                            </ul>
                        </div>
                    </div>
                     <div className="flex flex-col md:flex-row justify-between items-center pt-8 border-t border-white/5 text-xs uppercase tracking-[0.2em] font-bold text-zinc-700">
                        <p>© 2026 GUILD AI • ALL RIGHTS RESERVED</p>
                        <div className="flex gap-8 mt-4 md:mt-0">
                            <span className="hover:text-indigo-400 cursor-pointer transition-colors uppercase">Twitter/X</span>
                            <span className="hover:text-indigo-400 cursor-pointer transition-colors uppercase">LinkedIn</span>
                            <span className="hover:text-indigo-400 cursor-pointer transition-colors uppercase">Instagram</span>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    )
}

function AgentSimulatedLogs() {
    const logs = [
        { agent: 'GUILD', msg: 'Learning your brand voice from onboarding conversation...', status: 'active' },
        { agent: 'WRITER', msg: 'Drafting 3 LinkedIn posts for this week — checking against brand voice...', status: 'active' },
        { agent: 'QUALITY', msg: 'Checking ICP alignment on "Post_01" — passed ✓', status: 'success' },
        { agent: 'DESIGNER', msg: 'Creating Instagram carousel — applying brand colours and typography...', status: 'active' },
        { agent: 'VIDEO', msg: 'Generating 15-second product showcase reel...', status: 'pending' },
        { agent: 'QUALITY', msg: 'Checking brand voice on "Carousel_01" — passed ✓', status: 'success' },
        { agent: 'SCHEDULER', msg: 'LinkedIn post queued for Tuesday 12:30pm — peak engagement window...', status: 'active' },
        { agent: 'CRM', msg: 'New lead captured: Sarah M. via Instagram comment — ICP score 92%...', status: 'success' },
        { agent: 'NURTURE', msg: 'Sending personalised welcome sequence to 3 new contacts...', status: 'active' },
        { agent: 'GROWTH', msg: 'Reels posted at 6pm getting 2.5× more saves — adjusting schedule...', status: 'active' },
    ];

    const [visibleLogs, setVisibleLogs] = useState([]);

    useEffect(() => {
        let i = 0;
        const interval = setInterval(() => {
            setVisibleLogs(prev => [...prev.slice(-12), logs[i % logs.length]]);
            i++;
        }, 1500);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-3">
            {visibleLogs.map((log, idx) => (
                <motion.div 
                    key={idx} 
                    initial={{ opacity: 0, x: -10 }} 
                    animate={{ opacity: 1, x: 0 }}
                    className="flex gap-4 items-start"
                >
                    <span className="text-indigo-400 font-bold shrink-0">[{log.agent}]</span>
                    <span className="text-zinc-400">{log.msg}</span>
                    <span className="ml-auto text-indigo-500/50 text-xs animate-pulse">●</span>
                </motion.div>
            ))}
        </div>
    );
}

export default LandingPage
