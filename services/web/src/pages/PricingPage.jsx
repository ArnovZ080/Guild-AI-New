import { useState } from 'react'
import { Link } from 'react-router-dom'
import ZARPrice from '@/components/ui/ZARPrice'
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
                'Brand Identity Hub',
                'Quality Control Checks',
                'Standard Scheduling'
            ],
            buttonText: 'Start 21-Day Trial',
            color: 'from-blue-500 to-cyan-500'
        },
        {
            name: 'Growth',
            price: billingCycle === 'monthly' ? '$149' : '$119',
            period: '/mo',
            description: 'The complete content-to-customer process.',
            features: [
                '200 Content Pieces /mo',
                '10 AI Videos /mo',
                'Unlimited Integrations',
                'Built-in CRM & Lead Capture',
                'Automated Nurture Sequences',
                'Strategic Learning'
            ],
            buttonText: 'Start My Trial',
            popular: true,
            color: 'from-indigo-600 to-blue-600'
        },
        {
            name: 'Scale',
            price: billingCycle === 'monthly' ? '$299' : '$239',
            period: '/mo',
            description: 'Advanced features for scaling operations.',
            features: [
                '500 Content Pieces /mo',
                '30 AI Videos /mo',
                'Advanced Content Planner',
                'White-label Brand Portal',
                'Custom Feature Design',
                'Priority Support'
            ],
            buttonText: 'Contact for Scale',
            color: 'from-purple-600 to-pink-600'
        }
    ]

    return (
        <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
            <div className="container mx-auto max-w-7xl">
                <Link to="/landing">
                    <Button variant="ghost" className="text-zinc-400 hover:text-white mb-12 group">
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
                            Transparent <span className="text-gradient-cobalt">Pricing</span>
                        </h1>
                        <p className="text-xl text-zinc-400 max-w-2xl mx-auto font-light leading-relaxed mb-12">
                            No per-user fees. No hidden costs. Just one system that handles your growth at a predictable price.
                        </p>

                        <div className="flex items-center justify-center gap-2 p-1 bg-white/5 border border-white/10 rounded-2xl w-fit mx-auto backdrop-blur-xl">
                            <button
                                className={`px-8 py-3 rounded-xl text-sm font-bold transition-all ${billingCycle === 'monthly' ? 'bg-indigo-500 text-white shadow-glow-sm' : 'text-zinc-400 hover:text-zinc-300'}`}
                                onClick={() => setBillingCycle('monthly')}
                            >
                                Monthly
                            </button>
                            <button
                                className={`px-8 py-3 rounded-xl text-sm font-bold transition-all ${billingCycle === 'yearly' ? 'bg-indigo-500 text-white shadow-glow-sm' : 'text-zinc-400 hover:text-zinc-300'}`}
                                onClick={() => setBillingCycle('yearly')}
                            >
                                Yearly <span className="ml-1 opacity-60 font-medium">(-20%)</span>
                            </button>
                        </div>
                    </motion.div>
                </section>

                <div className="grid lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {plans.map((p, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.1 }}
                            className={`glass-panel p-10 rounded-3xl flex flex-col relative group ${p.popular ? 'border-indigo-500/50 shadow-glow' : 'border-white/10'}`}
                        >
                            {p.popular && (
                                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-indigo-500 text-white text-xs font-bold px-4 py-1.5 rounded-full flex items-center gap-1.5 shadow-lg shadow-indigo-500/20">
                                    <Sparkles size={12} />
                                    MOST POPULAR
                                </div>
                            )}

                            <div className="mb-8">
                                <h3 className="text-2xl font-bold font-heading mb-2">{p.name}</h3>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-5xl font-bold font-heading">{p.price}</span>
                                    <span className="text-zinc-400">{p.period}</span>
                                </div>
                                <ZARPrice usd={parseInt(p.price.replace('$', ''))} period={p.period} />
                                <p className="text-base text-zinc-400 mt-4 font-light">{p.description}</p>
                            </div>

                            <Link to={`/signup?plan=${p.name.toLowerCase()}`} className="mb-10">
                                <Button className={`w-full py-7 rounded-2xl font-bold text-lg transition-all ${p.popular ? 'bg-indigo-500 hover:bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'bg-white/5 border border-white/10 hover:bg-white/10 text-white'}`}>
                                    {p.buttonText}
                                </Button>
                            </Link>

                            <div className="space-y-4 mt-auto">
                                {p.features.map((f, j) => (
                                    <div key={j} className="flex gap-3 items-center text-sm">
                                        <div className={`w-5 h-5 rounded-full bg-gradient-to-br ${p.color} flex items-center justify-center shrink-0`}>
                                            <Check size={12} strokeWidth={3} className="text-white" />
                                        </div>
                                        <span className="text-zinc-400 font-light">{f}</span>
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    ))}
                </div>

                <div className="mt-24 glass-panel p-12 rounded-3xl border border-white/10">
                    <div className="grid md:grid-cols-2 gap-12 items-center">
                        <div>
                            <h3 className="text-3xl font-bold font-heading mb-4">Enterprise Grade Support</h3>
                            <p className="text-zinc-400 text-lg font-light leading-relaxed">
                                Need custom integrations or white-label solutions? Our team can build specific capabilities for your business.
                            </p>
                        </div>
                        <div className="flex justify-center md:justify-end">
                            <Link to="/contact">
                                <Button variant="outline" className="px-10 py-6 text-lg rounded-full border-white/20 hover:bg-white/5 transition-all">
                                    Contact Sales
                                </Button>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PricingPage
