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
            agents: 'Standard Agents',
            credits: '100 credits/month',
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
            agents: '5 Agents',
            credits: '500 credits/month',
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
            agents: '10 Agents',
            credits: '1,000 credits/month',
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
            agents: '25 Agents',
            credits: '2,500 credits/month',
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
            agents: 'All 115+ Agents',
            credits: '10,000 credits/month',
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
            icon: <GitBranch className="w-6 h-6" />,
            title: 'Intelligent Orchestration',
            description: 'One AI Orchestrator coordinates 115+ specialized agents automatically—like a CEO managing your entire company.',
            color: 'from-violet-500 to-purple-500',
            benefit: 'Guild: 115+ agents, Orchestrator coordinates'
        },
        {
            icon: <Shield className="w-6 h-6" />,
            title: 'Judge Layer Quality Assurance',
            description: 'Every output is automatically validated before you see it. Built-in QA for every task.',
            color: 'from-blue-500 to-cyan-500',
            benefit: 'Zero manual quality checks needed - save 10+ hours/week'
        },
        {
            icon: <TrendingUp className="w-6 h-6" />,
            title: 'Cross-Agent Meta KPIs',
            description: '7 KPIs that measure Guild\'s own performance. Track accuracy, coverage, and ROI.',
            color: 'from-green-500 to-emerald-500',
            benefit: 'See exactly how your AI performs in real-time'
        }
    ]

    const handleSignup = (planName) => {
        navigate(`/signup?plan=${planName.toLowerCase()}`)
    }

    return (
        <div className="min-h-screen bg-slate-50 overflow-x-hidden">
            <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-lg border-b border-slate-200">
                <div className="container mx-auto px-4 py-4 max-w-7xl flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <img src={guildLogo} alt="Guild Logo" className="w-10 h-10 rounded-lg" />
                        <span className="text-2xl font-bold bg-gradient-to-r from-sky-600 to-emerald-600 bg-clip-text text-transparent">Guild AI</span>
                    </div>
                    <div className="flex items-center space-x-4">
                        <Link to="/login"><Button variant="ghost">Login</Button></Link>
                        <Button className="bg-gradient-to-r from-sky-600 to-emerald-600 text-white" onClick={() => handleSignup('Growth')}>Get Started</Button>
                    </div>
                </div>
            </nav>

            <section className="container mx-auto px-4 py-24 text-center max-w-5xl">
                <Badge className="mb-6 bg-sky-100 text-sky-700 border-sky-200">
                    <Sparkles className="w-3 h-3 mr-1" />
                    115+ Specialized AI Agents • Intelligent Orchestration
                </Badge>
                <h1 className="text-6xl md:text-8xl font-bold mb-8 bg-gradient-to-r from-slate-900 to-emerald-800 bg-clip-text text-transparent leading-tight">
                    Other Platforms Give You AI Tools. Guild Gives You An AI Organization.
                </h1>
                <p className="text-2xl text-slate-600 mb-12 max-w-4xl mx-auto">
                    One intelligent Orchestrator coordinates 115+ specialized agents.
                    They calculate strategy, launch campaigns, and execute everything autonomously—all with built-in quality validation.
                </p>
                <div className="flex justify-center gap-6">
                    <Button size="lg" className="bg-slate-900 text-white px-10 py-8 text-xl rounded-2xl shadow-xl hover:scale-105 transition-transform" onClick={() => handleSignup('Free')}>
                        Start Free Trial <ArrowRight className="ml-2" />
                    </Button>
                </div>
            </section>

            <section className="container mx-auto px-4 py-24 bg-white border-y border-slate-200">
                <div className="grid md:grid-cols-3 gap-12 max-w-7xl mx-auto">
                    {featuresList.map((f, i) => (
                        <div key={i} className="p-8 rounded-3xl bg-slate-50 border border-slate-100 hover:shadow-2xl transition-all">
                            <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${f.color} flex items-center justify-center text-white mb-6 shadow-lg`}>
                                {f.icon}
                            </div>
                            <h3 className="text-2xl font-bold mb-4">{f.title}</h3>
                            <p className="text-slate-600 mb-6">{f.description}</p>
                            <div className="p-4 bg-sky-50 rounded-xl text-sky-700 text-sm font-bold">💡 {f.benefit}</div>
                        </div>
                    ))}
                </div>
            </section>

            <section className="container mx-auto px-4 py-32 max-w-7xl">
                <div className="text-center mb-16">
                    <h2 className="text-5xl font-bold mb-4">Fortune 500 Capabilities. Startup Pricing.</h2>
                    <p className="text-xl text-slate-600">Save 99% vs hiring a human team. Unlimited scaling for 1/1000th the cost.</p>
                </div>
                <div className="grid lg:grid-cols-5 gap-6">
                    {plans.map((p, i) => (
                        <Card key={i} className={`rounded-3xl border-2 transition-all hover:scale-105 ${p.popular ? 'border-sky-500 shadow-2xl z-10' : 'border-slate-100'}`}>
                            <CardHeader>
                                <CardTitle className="text-2xl">{p.name}</CardTitle>
                                <div className="text-4xl font-black mt-4">{p.price}<span className="text-lg font-normal text-slate-400">{p.period}</span></div>
                                <p className="text-slate-500 text-sm mt-2">{p.description}</p>
                            </CardHeader>
                            <CardContent>
                                <Button className={`w-full mb-8 rounded-xl py-6 ${p.popular ? 'bg-sky-600' : 'bg-slate-900'}`} onClick={() => handleSignup(p.name)}>Select {p.name}</Button>
                                <ul className="space-y-4">
                                    {p.features.map((f, fi) => (
                                        <li key={fi} className="flex items-center text-sm"><Check className="w-4 h-4 mr-2 text-emerald-500" /> {f}</li>
                                    ))}
                                </ul>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </section>

            <footer className="bg-slate-900 text-white py-24">
                <div className="container mx-auto px-4 max-w-7xl">
                    <div className="grid md:grid-cols-4 gap-12">
                        <div>
                            <div className="flex items-center gap-2 mb-6">
                                <img src={guildLogo} alt="Logo" className="w-8 h-8 rounded" />
                                <span className="text-2xl font-bold">Guild AI</span>
                            </div>
                            <p className="text-slate-400">The world's first autonomous AI organization. 115+ specialized agents working for you 24/7.</p>
                        </div>
                        <div>
                            <h4 className="font-bold mb-6">Product</h4>
                            <ul className="space-y-4 text-slate-400">
                                <li><Link to="/pricing">Pricing</Link></li>
                                <li><Link to="/features">Features</Link></li>
                                <li><Link to="/waitlist">Waitlist</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-bold mb-6">Legal</h4>
                            <ul className="space-y-4 text-slate-400">
                                <li><Link to="/privacy">Privacy Policy</Link></li>
                                <li><Link to="/terms">Terms of Service</Link></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    )
}

export default LandingPage
