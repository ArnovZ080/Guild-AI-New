import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Check, ArrowRight, Sparkles, Shield, TrendingUp, Users, Zap, Brain, Target, Award, Calculator, GitBranch } from 'lucide-react'
import guildLogo from '@/assets/guild-logo.png'

function LandingPage() {
    const navigate = useNavigate();

    const plans = [
        {
            name: 'Free',
            price: '$0',
            period: '/forever',
            description: 'Try Guild AI risk-free',
            features: [
                'All standard agents included',
                '100 monthly credits',
                'Judge Layer Quality Assurance',
                'Core integrations',
                'Community support',
                'Hire additional agents at $15/mo'
            ],
            popular: false,
            isFree: true
        },
        {
            name: 'Starter',
            price: '$49',
            period: '/month',
            description: 'Perfect for getting started',
            features: [
                '5 AI Agents included',
                '500 monthly credits',
                'Judge Layer Quality Assurance',
                'Core integrations',
                'Email support',
                'Hire additional agents at $12/mo'
            ],
            popular: false
        },
        {
            name: 'Growth',
            price: '$99',
            period: '/month',
            description: 'For growing businesses',
            features: [
                '10 AI Agents included',
                '1,000 monthly credits',
                'Judge Layer Quality Assurance',
                'All integrations (36 operational)',
                'Priority support',
                'Meta KPIs tracking',
                'Hire additional agents at $11/mo'
            ],
            popular: true
        },
        {
            name: 'Professional',
            price: '$199',
            period: '/month',
            description: 'For serious automation',
            features: [
                '25 AI Agents included',
                '2,500 monthly credits',
                'Judge Layer Quality Assurance',
                'All integrations + priority access',
                'Premium support',
                'Advanced analytics',
                'Custom workflows',
                'Hire additional agents at $10/mo'
            ],
            popular: false
        },
        {
            name: 'Enterprise',
            price: '$499',
            period: '/month',
            description: 'Unlimited AI workforce',
            features: [
                'All 115+ AI Agents included',
                '10,000 monthly credits',
                'Judge Layer Quality Assurance',
                'All integrations + custom connectors',
                'Dedicated support',
                'White-label options',
                'API access',
            ],
            popular: false
        }
    ]

    const featuresList = [
        {
            icon: <GitBranch className="w-6 h-6" strokeWidth={1.5} />,
            title: 'Intelligent Orchestration',
            description: 'One AI Orchestrator coordinates 115+ specialized agents automatically—like a CEO managing your entire company.',
            benefit: 'Guild: 115+ agents, Orchestrator coordinates'
        },
        {
            icon: <Shield className="w-6 h-6" strokeWidth={1.5} />,
            title: 'Judge Layer Quality Assurance',
            description: 'Every output is automatically validated before you see it. Built-in QA for every task.',
            benefit: 'Zero manual quality checks needed - save 10+ hours/week'
        },
        {
            icon: <TrendingUp className="w-6 h-6" strokeWidth={1.5} />,
            title: 'Cross-Agent Meta KPIs',
            description: "7 KPIs that measure Guild's own performance. Track accuracy, coverage, and ROI.",
            benefit: 'See exactly how your AI performs in real-time'
        }
    ]

    const handleSignup = (planName) => {
        navigate(`/signup?plan=${planName.toLowerCase()}`)
    }

    return (
        <div className="min-h-screen bg-surface-base overflow-x-hidden relative">
            {/* Ambient background */}
            <div className="bg-ambient-glow" />
            <div className="bg-ambient-glow-secondary" />

            {/* Navigation */}
            <nav className="sticky top-0 z-50 glass-panel">
                <div className="container mx-auto px-4 py-4 max-w-7xl flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <img src={guildLogo} alt="Guild Logo" className="w-10 h-10 rounded-lg" />
                        <span className="text-2xl font-bold text-gradient-cobalt font-heading">Guild AI</span>
                    </div>
                    <div className="flex items-center space-x-4">
                        <Link to="/login"><Button variant="ghost">Login</Button></Link>
                        <Button className="bg-cobalt text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.2)] hover:bg-cobalt-light" onClick={() => handleSignup('Growth')}>Get Started</Button>
                    </div>
                </div>
            </nav>

            {/* Hero */}
            <section className="container mx-auto px-4 py-24 text-center max-w-5xl relative">
                <Badge className="mb-6 bg-cobalt/10 text-cobalt-light border border-cobalt/20">
                    <Sparkles className="w-3 h-3 mr-1" strokeWidth={1.5} />
                    115+ Specialized AI Agents • Intelligent Orchestration
                </Badge>
                <h1 className="text-6xl md:text-8xl font-bold mb-8 text-white leading-tight font-heading tracking-tight">
                    Other Platforms Give You AI Tools. Guild Gives You An AI{' '}
                    <span className="text-gradient-cobalt">Organization.</span>
                </h1>
                <p className="text-xl text-zinc-500 mb-12 max-w-4xl mx-auto leading-relaxed">
                    One intelligent Orchestrator coordinates 115+ specialized agents.
                    They calculate strategy, launch campaigns, and execute everything autonomously—all with built-in quality validation.
                </p>
                <div className="flex justify-center gap-6">
                    <Button size="lg" className="bg-cobalt text-white px-10 py-8 text-lg rounded-xl shadow-lg shadow-cobalt/20 hover:bg-cobalt-light hover:shadow-xl transition-all font-heading" onClick={() => handleSignup('Free')}>
                        Start Free Trial <ArrowRight className="ml-2" strokeWidth={1.5} />
                    </Button>
                </div>
            </section>

            {/* Features */}
            <section className="container mx-auto px-4 py-24 border-y border-white/5">
                <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
                    {featuresList.map((f, i) => (
                        <div key={i} className="glass-panel p-8 rounded-2xl guild-card-hover">
                            <div className="w-12 h-12 rounded-xl gradient-cobalt flex items-center justify-center text-white mb-6 shadow-lg shadow-cobalt/20">
                                {f.icon}
                            </div>
                            <h3 className="text-xl font-semibold mb-3 text-zinc-100 font-heading">{f.title}</h3>
                            <p className="text-zinc-500 mb-6 leading-relaxed">{f.description}</p>
                            <div className="p-3 bg-cobalt/5 rounded-lg text-cobalt-light text-sm font-medium border border-cobalt/10">💡 {f.benefit}</div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Pricing */}
            <section className="container mx-auto px-4 py-24 max-w-7xl">
                <div className="text-center mb-16">
                    <h2 className="text-5xl font-bold mb-4 text-zinc-100 font-heading tracking-tight">Fortune 500 Capabilities. Startup Pricing.</h2>
                    <p className="text-lg text-zinc-500">Save 99% vs hiring a human team. Unlimited scaling for 1/1000th the cost.</p>
                </div>
                <div className="grid lg:grid-cols-5 gap-4">
                    {plans.map((p, i) => (
                        <Card key={i} className={`rounded-2xl transition-all ${p.popular ? 'border-cobalt/40 shadow-[0_0_30px_rgba(26,111,255,0.15)] scale-105 z-10' : 'border-white/5'}`}>
                            <CardHeader>
                                <CardTitle className="text-xl">{p.name}</CardTitle>
                                <div className="text-3xl font-bold mt-3 text-zinc-100 font-heading">{p.price}<span className="text-base font-normal text-zinc-600">{p.period}</span></div>
                                <p className="text-zinc-500 text-sm mt-1">{p.description}</p>
                            </CardHeader>
                            <CardContent>
                                <Button className={`w-full mb-6 rounded-lg py-5 ${p.popular ? 'bg-cobalt hover:bg-cobalt-light shadow-[inset_0_1px_0_rgba(255,255,255,0.2)]' : 'bg-white/5 hover:bg-white/10 border border-white/5 text-white/70'}`} onClick={() => handleSignup(p.name)}>Select {p.name}</Button>
                                <ul className="space-y-3">
                                    {p.features.map((f, fi) => (
                                        <li key={fi} className="flex items-start text-sm text-zinc-500"><Check className="w-4 h-4 mr-2 mt-0.5 text-cobalt-light shrink-0" strokeWidth={1.5} /> {f}</li>
                                    ))}
                                </ul>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </section>

            {/* Footer */}
            <footer className="border-t border-white/5 py-20">
                <div className="container mx-auto px-4 max-w-7xl">
                    <div className="grid md:grid-cols-4 gap-12">
                        <div>
                            <div className="flex items-center gap-2 mb-6">
                                <img src={guildLogo} alt="Logo" className="w-8 h-8 rounded" />
                                <span className="text-xl font-bold text-zinc-100 font-heading">Guild AI</span>
                            </div>
                            <p className="text-zinc-600 text-sm leading-relaxed">The world's first autonomous AI organization. 115+ specialized agents working for you 24/7.</p>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-6 text-zinc-500 font-heading text-sm">Product</h4>
                            <ul className="space-y-3 text-zinc-600 text-sm">
                                <li><Link to="/pricing" className="hover:text-zinc-500 transition-colors">Pricing</Link></li>
                                <li><Link to="/features" className="hover:text-zinc-500 transition-colors">Features</Link></li>
                                <li><Link to="/waitlist" className="hover:text-zinc-500 transition-colors">Waitlist</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-6 text-zinc-500 font-heading text-sm">Legal</h4>
                            <ul className="space-y-3 text-zinc-600 text-sm">
                                <li><Link to="/privacy" className="hover:text-zinc-500 transition-colors">Privacy Policy</Link></li>
                                <li><Link to="/terms" className="hover:text-zinc-500 transition-colors">Terms of Service</Link></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    )
}

export default LandingPage
