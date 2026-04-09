import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Check, Sparkles, Zap, Shield, Rocket, ArrowLeft } from 'lucide-react'
import { motion } from 'framer-motion'

function PricingPage() {
    const [billingCycle, setBillingCycle] = useState('monthly');

    const plans = [
        {
            name: 'Starter',
            price: billingCycle === 'monthly' ? '$49' : '$39',
            period: '/mo',
            description: 'Essential growth for solo founders.',
            features: [
                '50 Content Pieces /mo',
                '3 Connected Platforms',
                'Business Identity Hub',
                'Judge Layer™ QA',
                'Standard Scheduling'
            ],
            buttonText: 'Start 21-Day Trial',
            color: 'from-blue-500 to-cyan-500'
        },
        {
            name: 'Growth',
            price: billingCycle === 'monthly' ? '$149' : '$119',
            period: '/mo',
            description: 'The complete content-to-customer flywheel.',
            features: [
                '200 Content Pieces /mo',
                '10 AI Videos /mo',
                'Unlimited Integrations',
                'Built-in CRM & Lead Capture',
                'Nurture Engine Automation',
                'Behavioral Learning'
            ],
            buttonText: 'Deploy Growth Engine',
            popular: true,
            color: 'from-indigo-600 to-blue-600'
        },
        {
            name: 'Scale',
            price: billingCycle === 'monthly' ? '$299' : '$239',
            period: '/mo',
            description: 'Autonomous mastery for high-scale ops.',
            features: [
                '500 Content Pieces /mo',
                '30 AI Videos /mo',
                'Advanced Workflow Builder',
                'White-label Agent Portal',
                'Custom Agent Development',
                'Liaison Support'
            ],
            buttonText: 'Scale My Fleet',
            color: 'from-purple-600 to-pink-600'
        }
    ]

    return (
        <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
            <div className="container mx-auto max-w-7xl">
                <Link to="/landing">
                    <Button variant="ghost" className="text-zinc-500 hover:text-white mb-12 group">
                        <ArrowLeft className="mr-2 group-hover:-translate-x-1 transition-transform" />
                        Back to Landing
                    </Button>
                </Link>

                <section className="text-center mb-20">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                            Simple <span className="text-gradient-cobalt">Unit Economics</span>
                        </h1>
                        <p className="text-xl text-zinc-400 max-w-2xl mx-auto font-light leading-relaxed mb-12">
                            No per-seat licenses. No hidden fees. Just powerful orchestration at a predictable cost.
                        </p>

                        <div className="flex items-center justify-center gap-2 p-1 bg-white/5 border border-white/10 rounded-2xl w-fit mx-auto backdrop-blur-xl">
                            <button
                                className={`px-8 py-3 rounded-xl text-sm font-bold transition-all ${billingCycle === 'monthly' ? 'bg-indigo-500 text-white shadow-glow-sm' : 'text-zinc-500 hover:text-zinc-300'}`}
                                onClick={() => setBillingCycle('monthly')}
                            >
                                Monthly
                            </button>
                            <button
                                className={`px-8 py-3 rounded-xl text-sm font-bold transition-all ${billingCycle === 'yearly' ? 'bg-indigo-500 text-white shadow-glow-sm' : 'text-zinc-500 hover:text-zinc-300'}`}
                                onClick={() => setBillingCycle('yearly')}
                            >
                                Yearly <span className="ml-1 opacity-60 font-medium">(-20%)</span>
                            </button>
                        </div>
                    </motion.div>
                </section>

                <div className="grid lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {plans.map((p, i) => (
                        <div key={i} className={`glass-panel rounded-3xl p-10 flex flex-col relative transition-all duration-500 group ${p.popular ? 'border-indigo-500/40 shadow-glow scale-105 z-10' : 'border-white/5 hover:border-white/10'}`}>
                            {p.popular && (
                                <div className="absolute -top-4 left-1/2 -translate-x-1/2 gradient-cobalt text-white px-6 py-1.5 rounded-full text-[10px] font-black tracking-widest uppercase shadow-lg shadow-indigo-500/20">
                                    Strategic Choice
                                </div>
                            )}
                            
                            <div className="mb-8">
                                <h3 className="text-2xl font-bold font-heading mb-2">{p.name}</h3>
                                <p className="text-sm text-zinc-500 font-light">{p.description}</p>
                            </div>

                            <div className="mb-10 flex items-baseline gap-1">
                                <span className="text-6xl font-black font-heading tracking-tighter">{p.price}</span>
                                <span className="text-zinc-500 text-lg">{p.period}</span>
                            </div>

                            <div className="space-y-4 mb-12 flex-1">
                                {p.features.map((f, fi) => (
                                    <div key={fi} className="flex gap-3 items-center text-sm">
                                        <div className="w-5 h-5 rounded-full bg-emerald-500/10 flex items-center justify-center shrink-0">
                                            <Check size={12} className="text-emerald-500" strokeWidth={3} />
                                        </div>
                                        <span className="text-zinc-400 font-light">{f}</span>
                                    </div>
                                ))}
                            </div>

                            <Link to={`/signup?plan=${p.name.toLowerCase()}`}>
                                <Button className={`w-full py-8 rounded-2xl text-lg font-bold border-t border-white/20 transition-all ${p.popular ? 'gradient-cobalt hover:shadow-glow' : 'bg-white/5 hover:bg-white/10 text-white'}`}>
                                    {p.buttonText}
                                    <ArrowLeft className="ml-2 rotate-180" size={18} />
                                </Button>
                            </Link>
                        </div>
                    ))}
                </div>

                <div className="mt-24 text-center">
                    <p className="text-zinc-600 text-sm flex items-center justify-center gap-4">
                        <Shield size={16} /> All plans include bank-level encryption & data isolation.
                    </p>
                </div>
            </div>
        </div>
    )
}

export default PricingPage
