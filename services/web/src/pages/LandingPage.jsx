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
        { title: 'LEARN', description: 'Tell Guild about your business in a simple conversation. It remembers everything - your voice, your audience, your goals.', icon: <Brain />, color: 'from-blue-600 to-indigo-600' },
        { title: 'CREATE', description: 'Blog posts, social media, reels, emails, and ad creatives - all written and designed in your brand voice.', icon: <Sparkles />, color: 'from-blue-600 to-indigo-600' },
        { title: 'PUBLISH', description: 'Your content goes live at the perfect time on every platform. Automatically, every week.', icon: <Layout />, color: 'from-blue-600 to-indigo-600' },
        { title: 'ATTRACT', description: 'People discover your business through the content Guild creates - across social, search, and email.', icon: <Target />, color: 'from-blue-600 to-indigo-600' },
        { title: 'CAPTURE', description: 'When someone engages, Guild adds them to your contacts and scores how likely they are to buy.', icon: <Users />, color: 'from-blue-600 to-indigo-600' },
        { title: 'NURTURE', description: 'Personalised follow-up emails and messages keep the conversation going until they are ready to buy.', icon: <MessageSquare />, color: 'from-blue-600 to-indigo-600' },
        { title: 'CONVERT', description: 'Guild tracks what content drives sales and does more of it. Every week, the system gets smarter.', icon: <Rocket />, color: 'from-blue-600 to-indigo-600' },
    ];

    const plans = [
        {
            name: 'Starter',
            price: '$49',
            description: 'Start creating on-brand content with AI.',
            features: [
                'Personalised business onboarding',
                '50 content pieces per month',
                'Blog posts, social media & images',
                '3 connected platforms',
                'Brand quality checks on every piece',
                'Pre-built marketing templates'
            ],
            cta: 'Get Started',
            popular: false
        },
        {
            name: 'Growth',
            price: '$149',
            description: 'Create content, capture leads, and grow your customer base.',
            features: [
                'Everything in Starter',
                '200 content pieces per month',
                '10 AI-generated videos',
                'Unlimited connected platforms',
                'Contacts & lead tracking (CRM)',
                'Automated follow-up emails',
                'Facebook & Instagram ad designs'
            ],
            cta: 'Start Free Trial',
            popular: true
        },
        {
            name: 'Scale',
            price: '$299',
            description: 'For growing businesses and agencies managing multiple brands.',
            features: [
                'Everything in Growth',
                '500 content pieces per month',
                '30 AI-generated videos',
                'Custom workflow builder',
                'A/B testing on content & ads',
                'White-label for client brands',
                'Priority support'
            ],
            cta: 'Start Free Trial',
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
                        <Button className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-6 shadow-xl shadow-indigo-500/20 border-t border-white/20" onClick={() => handleSignup('Growth')}>
                            Get Started
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
                            AI-Powered Content & Growth for Small Business
                        </Badge>
                        <h1 className="text-6xl md:text-8xl font-bold font-heading leading-[1.1] tracking-tight mb-8">
                            Guild knows your business, <br />
                            <span className="text-gradient-cobalt">finds your customers,</span> <br />
                            and turns them into buyers.
                        </h1>
                        <p className="text-xl text-zinc-400 max-w-3xl mx-auto mb-10 leading-relaxed font-light">
                            You're paying for 6 different tools and still doing all the work yourself. Guild replaces them with one system that creates your content, posts it at the right time, and follows up with every person who engages - so you can run your business instead of your marketing.
                        </p>
                        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                            <Button size="lg" className="bg-white text-black hover:bg-zinc-200 rounded-full px-10 py-7 text-lg font-bold transition-all hover:scale-105 active:scale-95" onClick={() => handleSignup('Growth')}>
                                Start Your Free Trial <ArrowRight className="ml-2 text-indigo-600" />
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
                        <h2 className="text-4xl md:text-5xl font-bold font-heading mb-6 tracking-tight">How Guild Grows Your Business</h2>
                        <p className="text-zinc-400 max-w-2xl mx-auto text-lg leading-relaxed">
                            Most AI tools help you create content. Guild creates it, publishes it, finds the people who engage, and turns them into paying customers.
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
                    
                    <div className="mt-20 flex justify-center gap-8 items-center flex-wrap opacity-60 hover:opacity-100 transition-all duration-700">
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
                                        <h4 className="text-xl font-bold mb-2 font-heading">Everything Stays On-Brand</h4>
                                        <p className="text-base text-zinc-400 leading-relaxed font-light">Every post, email, and video is checked for brand voice, accuracy, and quality before you see it. No generic AI content. No embarrassing mistakes. You review and approve - nothing goes live without your say.</p>
                                    </div>
                                </div>
                                <div className="flex gap-6">
                                    <div className="w-12 h-12 rounded-xl border border-white/10 glass-panel flex items-center justify-center shrink-0 text-indigo-400 shadow-glow-sm">
                                        <Layout size={22} strokeWidth={1.5} />
                                    </div>
                                    <div>
                                        <h4 className="text-xl font-bold mb-2 font-heading">Posts When Your Audience Is Watching</h4>
                                        <p className="text-base text-zinc-400 leading-relaxed font-light">Guild learns when your followers are most active and schedules your content automatically. It syncs with your calendar so nothing clashes with your meetings or personal time.</p>
                                    </div>
                                </div>
                                <div className="flex gap-6">
                                    <div className="w-12 h-12 rounded-xl border border-white/10 glass-panel flex items-center justify-center shrink-0 text-indigo-400 shadow-glow-sm">
                                        <Award size={22} strokeWidth={1.5} />
                                    </div>
                                    <div>
                                        <h4 className="text-xl font-bold mb-2 font-heading">Professional Graphics and Video</h4>
                                        <p className="text-base text-zinc-400 leading-relaxed font-light">AI-generated images for your social posts, carousels, and ads. AI-generated video for reels and product showcases. Content that looks like you hired a creative agency - ready in minutes, not weeks.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="glass-panel p-10 rounded-2xl relative border border-white/10">
                            <h3 className="text-2xl font-bold font-heading mb-8">The Math is Simple</h3>
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
                                <span className="text-xs uppercase tracking-[0.3em] font-bold text-white/70">Guild AI Growth Plan</span>
                                <div className="text-5xl font-black mt-2">$149/mo</div>
                                <ZARPrice usd={149} className="text-white/50 text-sm" />
                                <p className="text-xs mt-4 font-medium text-white/50 tracking-tighter italic">Save 10+ hours a week on marketing</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Pricing */}
            <section className="py-24 px-6">
                <div className="container mx-auto max-w-6xl">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl md:text-5xl font-bold font-heading mb-6 tracking-tight">Simple Pricing. Real Results.</h2>
                        <p className="text-zinc-400 max-w-xl mx-auto">One subscription replaces 6+ separate tools - and does the work for you.</p>
                    </div>
                    <div className="grid md:grid-cols-3 gap-8">
                        {plans.map((p, i) => (
                            <div key={i} className={`glass-panel p-10 rounded-3xl relative flex flex-col ${p.popular ? 'border-indigo-500/50 scale-105 z-10 shadow-2xl shadow-indigo-500/10' : 'border-white/10'}`}>
                                {p.popular && <Badge className="absolute -top-4 left-1/2 -translate-x-1/2 bg-indigo-600 text-white font-bold border-none">MOST POPULAR</Badge>}
                                <h3 className="text-2xl font-bold font-heading mb-1">{p.name}</h3>
                                <div className="flex items-baseline gap-1 mb-2">
                                    <span className="text-5xl font-black">{p.price}</span>
                                    <span className="text-zinc-400 text-sm">/mo</span>
                                </div>
                                <ZARPrice usd={parseInt(p.price.replace('$', ''))} className="mb-6" />
                                <p className="text-zinc-400 text-sm mb-8">{p.description}</p>
                                <Button className={`w-full py-7 rounded-2xl mb-10 text-lg font-bold ${p.popular ? 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-xl shadow-indigo-500/20 active:scale-95' : 'bg-white/5 hover:bg-white/10 text-white'}`} onClick={() => handleSignup(p.name)}>
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
                                Ready to Stop Doing <br /> <span className="text-indigo-400 underline decoration-indigo-500/30">Your Own Marketing?</span>
                            </h2>
                            <p className="text-xl text-zinc-400 max-w-2xl mx-auto mb-12 leading-relaxed">
                                Guild creates your content, publishes it, and follows up with every person who engages. You just approve and watch your business grow.
                            </p>
                            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
                                <Button size="lg" className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-12 py-8 text-xl font-bold shadow-2xl shadow-indigo-500/20" onClick={() => handleSignup('Growth')}>
                                    Start Your Free Trial
                                </Button>
                            </div>
                            <p className="mt-8 text-zinc-400 text-sm italic">No credit card required. Cancel anytime.</p>
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
                                AI-powered growth for small businesses.
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
        { agent: 'GUILD', msg: 'Learning your brand voice from uploaded documents...', status: 'active' },
        { agent: 'WRITER', msg: 'Drafting 3 LinkedIn posts for this week...', status: 'active' },
        { agent: 'DESIGNER', msg: 'Creating Instagram carousel for spring collection...', status: 'active' },
        { agent: 'VIDEO', msg: 'Generating 15-second product showcase reel...', status: 'pending' },
        { agent: 'QUALITY', msg: 'Checking brand voice on "Post_01" - passed ✓', status: 'success' },
        { agent: 'SCHEDULER', msg: 'LinkedIn post scheduled for Tuesday 12:30pm (peak engagement)...', status: 'active' },
        { agent: 'CRM', msg: 'New lead captured: Sarah M. from Instagram comment (ICP: 92%)...', status: 'success' },
        { agent: 'NURTURE', msg: 'Sending welcome email to 3 new subscribers...', status: 'active' },
        { agent: 'GROWTH', msg: 'Instagram reels at 6pm getting 2.5x more saves - adjusting schedule...', status: 'active' },
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
