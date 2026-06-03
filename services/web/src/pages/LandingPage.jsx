import { useState, useEffect, useRef } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import ZARPrice from '@/components/ui/ZARPrice'
import { Button } from '@/components/ui/button'
import { ShinyButton } from '@/components/ui/shiny-button'
import { MagicTextReveal } from '@/components/ui/magic-text-reveal'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import {
  Check, ArrowRight, Sparkles, Shield, TrendingUp,
  Users, Zap, Brain, Target, Award, Calculator,
  GitBranch, MessageSquare, Play, Layout, Rocket,
  Menu, X
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import guildLogo from '@/assets/guild-logo.png'
import { useWaitlistStatus } from '@/hooks/useWaitlistStatus'
import {
  fadeUp, fadeIn, scaleIn, slideInLeft, slideInRight,
  staggerContainer, viewportOnce, springTransition
} from '@/lib/transitions'
import { TiltCard } from '@/components/ui/tilt-card'
import Footer from '@/components/Footer'

function LandingPage() {
    const navigate = useNavigate();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const { spotsRemaining, totalSpots, loading } = useWaitlistStatus();
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 20);
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const growthSteps = [
        { title: 'LEARN', description: 'Tell Guild about your business once. It learns your voice, audience, and goals — and gets smarter every cycle.', icon: <Brain />, color: 'from-blue-600 to-indigo-600' },
        { title: 'CREATE', description: 'Blog posts, social content, reels, and emails — written in your brand voice and quality-checked before you see them.', icon: <Sparkles />, color: 'from-blue-600 to-indigo-600' },
        { title: 'PUBLISH', description: 'Content goes live at the optimal time on every platform. Automatically. Every week. Zero scheduling.', icon: <Layout />, color: 'from-blue-600 to-indigo-600' },
        { title: 'ATTRACT', description: 'People find your business through content Guild creates — across social, search, and email. You show up consistently.', icon: <Target />, color: 'from-blue-600 to-indigo-600' },
        { title: 'CAPTURE', description: 'Every engagement becomes a scored lead in your CRM. No spreadsheets. No manual tracking. No lead lost.', icon: <Users />, color: 'from-blue-600 to-indigo-600' },
        { title: 'NURTURE', description: 'Personalised sequences go out automatically — in your voice, at the right moment — until they\'re ready to buy.', icon: <MessageSquare />, color: 'from-blue-600 to-indigo-600' },
        { title: 'CONVERT', description: 'Guild tracks what drives sales and does more of it. Every cycle, it gets sharper on your business and your buyers.', icon: <Rocket />, color: 'from-blue-600 to-indigo-600' },
    ];

    const plans = [
        {
            name: 'Starter',
            price: '$39',
            regularPrice: '$49',
            description: 'Content created, published, and on-brand - without the agency fee.',
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
            description: 'Create content, capture every lead who engages, and nurture them to purchase - without doing any of it manually.',
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
            <motion.nav
                initial={{ y: -20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                className="fixed top-0 left-0 right-0 z-50"
                style={{
                    backdropFilter: scrolled || mobileMenuOpen ? 'blur(20px) saturate(1.6)' : 'blur(0px)',
                    WebkitBackdropFilter: scrolled || mobileMenuOpen ? 'blur(20px) saturate(1.6)' : 'blur(0px)',
                    background: scrolled || mobileMenuOpen ? 'rgba(2,2,3,0.90)' : 'transparent',
                    borderBottom: scrolled || mobileMenuOpen ? '1px solid rgba(255,255,255,0.06)' : '1px solid transparent',
                    transition: 'all 0.4s cubic-bezier(0.16,1,0.3,1)',
                    padding: scrolled ? '12px 0' : '24px 0',
                }}
            >
                <div className="container mx-auto px-6 flex items-center justify-between max-w-7xl">
                    <motion.div
                        animate={{ scale: scrolled ? 0.9 : 1 }}
                        transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                        className="flex items-center gap-3"
                    >
                        <img src={guildLogo} alt="Guild" className="w-9 h-9 border border-white/10 rounded-lg shadow-2xl" />
                        <span className="text-xl font-bold tracking-tight">Guild <span className="text-indigo-400">AI</span></span>
                    </motion.div>

                    {/* Desktop links */}
                    <div className="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-400">
                        <Link to="/how-it-works" className="hover:text-white transition-colors duration-200">How It Works</Link>
                        <Link to="/features" className="hover:text-white transition-colors duration-200">Features</Link>
                        <Link to="/pricing" className="hover:text-white transition-colors duration-200">Pricing</Link>
                        <Link to="/about" className="hover:text-white transition-colors duration-200">About</Link>
                    </div>

                    {/* Desktop CTAs */}
                    <div className="hidden md:flex items-center gap-4">
                        <Link to="/login" className="text-sm font-medium text-zinc-400 hover:text-white px-4 py-2 transition-colors duration-200">Login</Link>
                        <ShinyButton onClick={() => navigate('/waitlist')} className="text-sm px-5 py-2.5">
                            Claim Founding Access
                        </ShinyButton>
                    </div>

                    {/* Mobile: hamburger + CTA */}
                    <div className="flex md:hidden items-center gap-3">
                        <ShinyButton onClick={() => navigate('/waitlist')} className="text-xs px-4 py-2">
                            Get Access
                        </ShinyButton>
                        <button
                            onClick={() => setMobileMenuOpen(o => !o)}
                            className="p-2 text-zinc-400 hover:text-white transition-colors"
                            aria-label="Toggle menu"
                        >
                            {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
                        </button>
                    </div>
                </div>

                {/* Mobile dropdown menu */}
                <AnimatePresence>
                    {mobileMenuOpen && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
                            className="md:hidden overflow-hidden border-t border-white/6"
                        >
                            <div className="container mx-auto px-6 py-4 flex flex-col gap-1">
                                {[
                                    { to: '/how-it-works', label: 'How It Works' },
                                    { to: '/features', label: 'Features' },
                                    { to: '/pricing', label: 'Pricing' },
                                    { to: '/about', label: 'About' },
                                    { to: '/login', label: 'Login' },
                                ].map(({ to, label }) => (
                                    <Link
                                        key={to}
                                        to={to}
                                        onClick={() => setMobileMenuOpen(false)}
                                        className="py-3 px-2 text-sm font-medium text-zinc-400 hover:text-white border-b border-white/5 last:border-0 transition-colors"
                                    >
                                        {label}
                                    </Link>
                                ))}
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </motion.nav>

            {/* Hero */}
            <section className="pt-44 pb-24 px-6 relative overflow-hidden">
                <div className="container mx-auto max-w-6xl text-center relative z-10">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <p className="text-lg text-zinc-300 font-semibold mb-6 tracking-tight">
                            You're paying for 6 different tools. And still doing all the work yourself.
                        </p>
                        <h1 className="text-6xl md:text-8xl font-bold font-heading leading-[1.1] tracking-tight mb-6">
                            Guild knows your business, <br />
                            <span className="text-gradient-cobalt">finds your customers,</span> <br />
                            and turns them into buyers.
                        </h1>
                        <Badge className="mb-6 bg-white/5 text-indigo-300 border border-white/10 px-4 py-1 flex items-center gap-2 w-fit mx-auto backdrop-blur-sm">
                            <Sparkles size={14} className="animate-pulse" />
                            Founding Member Access - 50 spots. First come, first locked.
                        </Badge>
                        <p className="text-xl text-zinc-400 max-w-3xl mx-auto mb-10 leading-relaxed font-light">
                            Guild replaces them with one system that creates your content, publishes it at the right time, captures every lead who engages, and nurtures them into customers - without you doing any of it manually.
                        </p>
                        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                            <ShinyButton onClick={() => navigate('/waitlist')} className="text-lg px-10 py-5">
                                Claim Founding Access
                            </ShinyButton>
                            <Link to="/how-it-works">
                                <button className="flex items-center gap-2 text-zinc-400 hover:text-white border border-white/10 hover:border-white/20 rounded-full px-8 py-4 text-base transition-all duration-200 group">
                                    <Play className="fill-indigo-400/60 group-hover:fill-indigo-400 transition-all" size={14} />
                                    See How It Works
                                </button>
                            </Link>
                        </div>
                        {/* Social proof strip */}
                        <div className="mt-10 flex items-center justify-center gap-3">
                            <div className="flex items-center gap-2 px-5 py-2.5 rounded-full glass-panel border border-white/10 text-sm">
                                <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
                                <span className="text-zinc-400 font-medium">Founding cohort open - <span className="text-indigo-300 font-bold">{loading ? '--' : spotsRemaining} of {totalSpots} spots</span> remaining</span>
                            </div>
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
                    <motion.div
                        variants={staggerContainer}
                        initial="hidden"
                        whileInView="visible"
                        viewport={viewportOnce}
                        className="text-center mb-20"
                    >
                        <motion.h2 variants={fadeUp} className="text-4xl md:text-5xl font-bold font-heading mb-6 tracking-tight">The Only Platform That Closes the Full Loop</motion.h2>
                        <motion.p variants={fadeUp} className="text-zinc-400 max-w-2xl mx-auto text-lg leading-relaxed">
                            Most tools help you create content and leave the rest to you. Guild creates it, publishes it, captures everyone who engages, and turns them into paying customers - as one connected system.
                        </motion.p>
                    </motion.div>

                    {/* Glass step cards */}
                    <motion.div
                        variants={staggerContainer}
                        initial="hidden"
                        whileInView="visible"
                        viewport={viewportOnce}
                        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
                    >
                        {growthSteps.map((step, i) => (
                            <motion.div
                                key={i}
                                variants={fadeUp}
                                whileHover={{ y: -4, transition: { duration: 0.25, ease: [0.16,1,0.3,1] } }}
                                className="relative overflow-hidden rounded-2xl cursor-default group"
                                style={{
                                    background: 'rgba(255,255,255,0.055)',
                                    border: '1px solid rgba(255,255,255,0.10)',
                                }}
                            >
                                {/* Top accent line */}
                                <div className="absolute top-0 left-0 right-0 h-[1px]"
                                    style={{ background: 'linear-gradient(90deg, transparent, rgba(94,106,210,0.6) 50%, transparent)' }} />

                                {/* Large decorative step number — sits behind content */}
                                <div className="absolute -bottom-3 -right-2 text-[80px] font-black leading-none select-none pointer-events-none"
                                    style={{ color: 'rgba(94,106,210,0.08)', letterSpacing: '-4px' }}>
                                    {String(i + 1).padStart(2, '0')}
                                </div>

                                {/* Hover glow */}
                                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                                    style={{ background: 'radial-gradient(ellipse at 50% 0%, rgba(94,106,210,0.10) 0%, transparent 70%)' }} />

                                <div className="relative z-10 p-6">
                                    {/* Icon + step number pill */}
                                    <div className="flex items-center justify-between mb-5">
                                        <div className="w-10 h-10 rounded-xl flex items-center justify-center text-indigo-300"
                                            style={{ background: 'rgba(94,106,210,0.12)', border: '1px solid rgba(94,106,210,0.2)' }}>
                                            {step.icon}
                                        </div>
                                        <span className="label-eyebrow text-indigo-500/50">{String(i + 1).padStart(2, '0')}</span>
                                    </div>

                                    {/* Title */}
                                    <h3 className="label-eyebrow text-indigo-300 mb-2">{step.title}</h3>

                                    {/* Description — short, readable */}
                                    <p className="text-sm text-zinc-300 leading-relaxed font-light">{step.description}</p>
                                </div>
                            </motion.div>
                        ))}
                    </motion.div>

                    {/* Integration pills with brand colours */}
                    <div className="mt-16">
                        <p className="label-eyebrow text-zinc-600 text-center mb-8">Connects with the tools you already use</p>
                        <div className="flex justify-center gap-3 items-center flex-wrap">
                            {[
                                { name: 'Instagram', dot: '#E1306C' },
                                { name: 'LinkedIn', dot: '#0A66C2' },
                                { name: 'Facebook', dot: '#1877F2' },
                                { name: 'Mailchimp', dot: '#FFE01B' },
                                { name: 'Shopify', dot: '#96BF48' },
                                { name: 'Google Ads', dot: '#4285F4' },
                            ].map(({ name, dot }) => (
                                <div key={name} className="flex items-center gap-2 px-4 py-2 rounded-full border border-white/8 bg-white/3 hover:border-white/15 transition-colors">
                                    <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: dot }} />
                                    <span className="text-sm text-zinc-400">{name}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            <hr className="section-divider" />
            {/* Magic Text Interactive Section */}
            <section className="py-24 px-6 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-b from-transparent via-indigo-950/10 to-transparent pointer-events-none" />
                <motion.div
                    variants={fadeUp}
                    initial="hidden"
                    whileInView="visible"
                    viewport={viewportOnce}
                    className="container mx-auto max-w-6xl text-center"
                >
                    <p className="label-eyebrow text-indigo-400/70 mb-6">The system in one sentence</p>
                    <p className="text-zinc-500 text-sm mb-10 tracking-wide">Hover to reveal ↓</p>
                    <div className="flex justify-center">
                        <MagicTextReveal
                            text="Guild does the work."
                            color="rgba(165, 180, 252, 1)"
                            fontSize={typeof window !== 'undefined' ? (window.innerWidth < 640 ? 36 : window.innerWidth < 1024 ? 52 : 64) : 64}
                            fontFamily="Inter, sans-serif"
                            fontWeight={800}
                            spread={70}
                            speed={0.5}
                            density={3}
                            resetOnMouseLeave={true}
                            style={{
                                background: 'transparent',
                                border: 'none',
                                backdropFilter: 'none',
                            }}
                        />
                    </div>
                    <p className="text-zinc-600 text-sm mt-10 max-w-sm mx-auto leading-relaxed">
                        Content created, published, leads captured and nurtured — without you lifting a finger.
                    </p>
                </motion.div>
            </section>

            <hr className="section-divider" />
            {/* Differentiators */}
            <section className="py-32 px-6">
                <div className="container mx-auto max-w-6xl">
                    <div className="grid lg:grid-cols-2 gap-20 items-center">
                        <motion.div
                            variants={slideInLeft}
                            initial="hidden"
                            whileInView="visible"
                            viewport={viewportOnce}
                            className="relative"
                        >
                            <div className="absolute -inset-20 bg-indigo-500/5 blur-[100px] rounded-full" />
                            <h2 className="text-4xl md:text-5xl font-bold font-heading mb-8 relative">
                                What Makes <br /> <span className="text-indigo-400">Guild Different</span>
                            </h2>
                            <motion.div
                                variants={staggerContainer}
                                initial="hidden"
                                whileInView="visible"
                                viewport={viewportOnce}
                                className="space-y-8 relative"
                            >
                                <div className="flex gap-6">
                                    <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center shrink-0 text-indigo-400">
                                        <Shield size={22} strokeWidth={1.5} />
                                    </div>
                                    <div>
                                        <h4 className="text-xl font-bold mb-2 font-heading">Content That Checks Itself Before You See It</h4>
                                        <p className="text-base text-zinc-400 leading-relaxed font-light">Before any content reaches you, Guild has already checked it against your brand voice, your ideal customer profile, your SEO requirements, and your factual accuracy standards. You only review what's already worth approving. No generic AI output. No off-brand mistakes. No other platform does this.</p>
                                    </div>
                                </div>
                                <div className="flex gap-6">
                                    <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center shrink-0 text-indigo-400">
                                        <Layout size={22} strokeWidth={1.5} />
                                    </div>
                                    <div>
                                        <h4 className="text-xl font-bold mb-2 font-heading">Posts When Your Audience Is Actually Watching</h4>
                                        <p className="text-base text-zinc-400 leading-relaxed font-light">Guild learns when your followers are most active and schedules your content automatically. It syncs with your calendar so nothing clashes with your meetings or personal time. The longer you use it, the smarter the scheduling gets.</p>
                                    </div>
                                </div>
                                <div className="flex gap-6">
                                    <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center shrink-0 text-indigo-400">
                                        <Award size={22} strokeWidth={1.5} />
                                    </div>
                                    <div>
                                        <h4 className="text-xl font-bold mb-2 font-heading">Gets Smarter the Longer You Use It</h4>
                                        <p className="text-base text-zinc-400 leading-relaxed font-light">Content that performs well shapes the next campaign. Leads that convert refine who gets targeted next. Guild builds a deep understanding of your business over time - making it more valuable every month, and making switching feel pointless.</p>
                                    </div>
                                </div>
                            </motion.div>
                        </motion.div>
                        <motion.div
                            variants={slideInRight}
                            initial="hidden"
                            whileInView="visible"
                            viewport={viewportOnce}
                            className="glass-panel p-10 rounded-2xl relative border border-white/10"
                        >
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
                                        <ZARPrice usd={504} className="text-red-300 text-xs" />
                                    </div>
                                </div>
                                <p className="text-xs text-zinc-600 italic mt-2">(and you still do all the work yourself)</p>
                                <p className="text-lg md:text-xl text-white font-heading font-bold mt-6 leading-relaxed">This replaces Buffer + Canva + Mailchimp + HubSpot + a freelance writer + a video editor - and does the work for you.</p>
                            </div>
                            <div className="p-8 gradient-cobalt rounded-xl text-center shadow-3xl">
                                <span className="text-xs uppercase tracking-[0.3em] font-bold text-white/70">Guild AI - Founding Member Rate</span>
                                <div className="text-5xl font-black mt-2">$119/mo</div>
                                <ZARPrice usd={119} className="text-white/80 text-sm" />
                                <p className="text-xs mt-1 font-medium text-white/40 line-through tracking-tighter">Regular price $149/mo</p>
                                <p className="text-xs mt-3 font-medium text-white/60 tracking-tighter italic">Founding rate locked in permanently</p>
                            </div>
                        </motion.div>
                    </div>
                </div>
            </section>

            <hr className="section-divider" />
            {/* Pricing */}
            <section className="py-24 px-6">
                <div className="container mx-auto max-w-6xl">
                    <motion.div
                        variants={fadeUp}
                        initial="hidden"
                        whileInView="visible"
                        viewport={viewportOnce}
                        className="text-center mb-6"
                    >
                        <h2 className="text-4xl md:text-5xl font-bold font-heading mb-6 tracking-tight">Founding Member Pricing.</h2>
                        <p className="text-zinc-400 max-w-xl mx-auto">Lock in your rate before public launch. One system replaces 6+ tools - and does the work for you.</p>
                    </motion.div>

                    {/* Founding member banner */}
                    <div className="mb-10 p-4 rounded-2xl border border-indigo-500/30 bg-indigo-500/5 flex items-center justify-center gap-3 text-sm max-w-2xl mx-auto">
                        <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse shrink-0" />
                        <span className="text-indigo-300 font-medium">Founding members lock in today's rate permanently - it never increases, even when public pricing does.</span>
                    </div>

                    <motion.div
                        variants={staggerContainer}
                        initial="hidden"
                        whileInView="visible"
                        viewport={viewportOnce}
                        className="grid md:grid-cols-3 gap-8"
                    >
                        {plans.map((p, i) => (
                            <motion.div key={i} variants={scaleIn}>
                            <TiltCard
                                className={`glass-panel p-10 rounded-3xl relative flex flex-col h-full ${p.popular ? 'border-indigo-500/50 shadow-2xl shadow-indigo-500/10' : 'border-white/10'}`}
                                glowColor={p.popular ? 'rgba(99,102,241,0.18)' : 'rgba(94,106,210,0.10)'}
                            >
                                {p.popular && <Badge className="absolute -top-4 left-1/2 -translate-x-1/2 bg-indigo-600 text-white font-bold border-none">MOST POPULAR</Badge>}
                                <h3 className="text-2xl font-bold font-heading mb-1">{p.name}</h3>
                                <div className="flex items-baseline gap-2 mb-1">
                                    <span className="text-5xl font-black">{p.price}</span>
                                    <span className="text-zinc-400 text-sm">/mo</span>
                                    <span className="text-zinc-600 text-sm line-through">{p.regularPrice}</span>
                                </div>
                                <ZARPrice usd={parseInt(p.price.replace('$', ''))} className="mb-1" />
                                <p className="text-xs text-indigo-400/70 font-medium mb-5 uppercase tracking-widest">Founding rate - locked for life</p>
                                <p className="text-zinc-400 text-sm mb-8">{p.description}</p>
                                <ShinyButton
                                    className="w-full mb-10 text-base justify-center"
                                    onClick={() => p.name === 'Scale' ? navigate('/contact') : navigate('/waitlist')}
                                >
                                    {p.cta}
                                </ShinyButton>
                                <ul className="space-y-4 flex-1">
                                    {p.features.map((f, fi) => (
                                        <li key={fi} className="flex items-center text-sm text-zinc-400 gap-3">
                                            <div className="w-5 h-5 rounded-full bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center shrink-0">
                                                <Check size={12} className="text-indigo-400" strokeWidth={3} />
                                            </div>
                                            {f}
                                        </li>
                                    ))}
                                </ul>
                            </TiltCard>
                            </motion.div>
                        ))}
                    </motion.div>

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
                                Your content is finding <br /> <span className="text-indigo-400 underline decoration-indigo-500/30">customers right now.</span>
                            </h2>
                            <p className="text-xl text-zinc-400 max-w-2xl mx-auto mb-4 leading-relaxed">
                                Guild creates your content, publishes it automatically, captures every lead who engages, and nurtures them into buyers. You approve. Your business grows.
                            </p>
                            <p className="text-sm text-indigo-300/70 mb-12 font-medium">
                                Founding members lock in today's rate permanently. 50 spots. Rate increases at public launch.
                            </p>
                            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
                                <ShinyButton onClick={() => navigate('/waitlist')} className="text-lg px-12 py-5">
                                    Claim Your Founding Rate
                                </ShinyButton>
                            </div>
                            <p className="mt-8 text-zinc-300 text-lg md:text-xl font-medium">Your data is yours. Cancel anytime. No lock-in contracts.</p>
                        </motion.div>
                    </div>
                </div>
            </section>

            <Footer />
        </div>
    )
}

function AgentSimulatedLogs() {
    const logs = [
        { agent: 'GUILD', msg: 'Learning your brand voice from onboarding conversation...', status: 'active' },
        { agent: 'WRITER', msg: 'Drafting 3 LinkedIn posts for this week - checking against brand voice...', status: 'active' },
        { agent: 'QUALITY', msg: 'Checking ICP alignment on "Post_01" - passed ✓', status: 'success' },
        { agent: 'DESIGNER', msg: 'Creating Instagram carousel - applying brand colours and typography...', status: 'active' },
        { agent: 'VIDEO', msg: 'Generating 15-second product showcase reel...', status: 'pending' },
        { agent: 'QUALITY', msg: 'Checking brand voice on "Carousel_01" - passed ✓', status: 'success' },
        { agent: 'SCHEDULER', msg: 'LinkedIn post queued for Tuesday 12:30pm - peak engagement window...', status: 'active' },
        { agent: 'CRM', msg: 'New lead captured: Sarah M. via Instagram comment - ICP score 92%...', status: 'success' },
        { agent: 'NURTURE', msg: 'Sending personalised welcome sequence to 3 new contacts...', status: 'active' },
        { agent: 'GROWTH', msg: 'Reels posted at 6pm getting 2.5× more saves - adjusting schedule...', status: 'active' },
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
