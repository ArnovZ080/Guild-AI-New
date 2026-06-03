import { useState } from 'react'
import Footer from '@/components/Footer'
import { Link, useNavigate } from 'react-router-dom'
import ZARPrice from '@/components/ui/ZARPrice'
import { Button } from '@/components/ui/button'
import { Check, Sparkles, Shield, ArrowLeft, Lock } from 'lucide-react'
import { motion } from 'framer-motion'

function PricingPage() {
    const navigate = useNavigate()

    const plans = [
        {
            name: 'Starter',
            foundingPrice: '$39',
            regularPrice: '$49',
            foundingUsd: 39,
            period: '/mo',
            description: 'Content created, published, and on-brand - without the agency fee.',
            features: [
                '50 content pieces per month',
                'Blog posts, social media & images',
                '3 connected platforms',
                'Quality checks on every piece',
                'Brand Identity Hub',
                'Pre-built marketing templates',
                'Email support'
            ],
            buttonText: 'Claim Founding Access',
            buttonAction: 'waitlist',
            color: 'from-blue-500 to-cyan-500'
        },
        {
            name: 'Growth',
            foundingPrice: '$119',
            regularPrice: '$149',
            foundingUsd: 119,
            period: '/mo',
            description: 'Create content, capture every lead who engages, and nurture them to purchase - without doing any of it manually.',
            features: [
                '200 content pieces per month',
                '10 AI-generated videos',
                'Unlimited connected platforms',
                'Built-in CRM & lead capture',
                'Automated nurture sequences',
                'Ad creative generation',
                'Smart scheduling with learning',
                'Priority support'
            ],
            buttonText: 'Claim Founding Access',
            buttonAction: 'waitlist',
            popular: true,
            color: 'from-indigo-600 to-blue-600'
        },
        {
            name: 'Scale',
            foundingPrice: '$239',
            regularPrice: '$299',
            foundingUsd: 239,
            period: '/mo',
            description: 'Run multiple brands or client accounts from one place. Agency power at a founder\'s price.',
            features: [
                '500 content pieces per month',
                '30 AI-generated videos',
                'Unlimited connected platforms',
                'Advanced workflow builder',
                'A/B testing on content & ads',
                'White-label brand portal',
                'Dedicated onboarding call',
                'Priority support'
            ],
            buttonText: 'Talk to Arno',
            buttonAction: 'contact',
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

                {/* Header */}
                <section className="text-center mb-12">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                            Founding Member <span className="text-gradient-cobalt">Pricing</span>
                        </h1>
                        <p className="text-xl text-zinc-400 max-w-2xl mx-auto font-light leading-relaxed">
                            One system replaces 6+ separate tools - and does the work for you. Lock in your rate before public launch and it never changes.
                        </p>
                    </motion.div>
                </section>

                {/* Founding member banner */}
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.15 }}
                    className="mb-14 max-w-3xl mx-auto"
                >
                    <div className="flex items-start gap-4 p-6 rounded-2xl border border-indigo-500/30 bg-indigo-500/5 backdrop-blur-sm">
                        <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center shrink-0">
                            <Lock size={18} className="text-indigo-400" />
                        </div>
                        <div className="text-left">
                            <p className="text-indigo-300 font-bold mb-1 text-sm uppercase tracking-widest">Founding Member Pricing - Locked For Life</p>
                            <p className="text-zinc-400 text-sm leading-relaxed">
                                Guild is in beta. The first 50 members lock in today's rate permanently. When Guild raises prices at public launch in August 2026, your founding rate never changes. You're buying in at the floor.
                            </p>
                        </div>
                    </div>
                </motion.div>

                {/* Pricing cards */}
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
                                <h3 className="text-2xl font-bold font-heading mb-3">{p.name}</h3>

                                {/* Founding price */}
                                <div className="flex items-baseline gap-2 mb-1">
                                    <span className="text-5xl font-bold font-heading">{p.foundingPrice}</span>
                                    <span className="text-zinc-400">{p.period}</span>
                                </div>
                                <ZARPrice usd={p.foundingUsd} period={p.period} />

                                {/* Regular price struck through */}
                                <p className="text-zinc-600 text-sm mt-1 line-through">
                                    Regular price: {p.regularPrice}/mo
                                </p>
                                <p className="text-indigo-400/80 text-xs font-bold uppercase tracking-widest mt-1">
                                    Founding rate - locked for life
                                </p>

                                <p className="text-base text-zinc-400 mt-5 font-light leading-relaxed">{p.description}</p>
                            </div>

                            <Button
                                className={`w-full py-7 rounded-2xl font-bold text-lg transition-all mb-10 ${p.popular ? 'bg-indigo-500 hover:bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' : 'bg-white/5 border border-white/10 hover:bg-white/10 text-white'}`}
                                onClick={() => p.buttonAction === 'contact' ? navigate('/contact') : navigate('/waitlist')}
                            >
                                {p.buttonText}
                            </Button>

                            <div className="space-y-4 mt-auto">
                                {p.features.map((f, j) => (
                                    <div key={j} className="flex gap-3 items-center text-sm">
                                        <div className={`w-5 h-5 rounded-full bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center shrink-0`}>
                                            <Check size={12} strokeWidth={3} className="text-white" />
                                        </div>
                                        <span className="text-zinc-400 font-light">{f}</span>
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    ))}
                </div>

                {/* Add-ons */}
                <div className="mt-12 text-center">
                    <p className="text-zinc-600 text-sm">
                        Add-ons: Extra video from $0.50 · Extra content $0.10/piece · Additional brand profiles $29/mo
                    </p>
                </div>

                {/* Guarantee */}
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="mt-14 max-w-2xl mx-auto text-center"
                >
                    <div className="flex items-start gap-4 p-8 rounded-2xl border border-white/10 glass-panel">
                        <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center shrink-0 border border-white/10">
                            <Shield size={18} className="text-zinc-400" />
                        </div>
                        <div className="text-left">
                            <p className="text-white font-bold mb-2">30-Day Guarantee</p>
                            <p className="text-zinc-400 text-sm leading-relaxed">
                                Publish a full month of content and capture your first leads. If you don't, your first month is refunded in full - no forms, no questions. Email Arno directly.
                            </p>
                        </div>
                    </div>
                </motion.div>

                {/* Tool replacement anchor */}
                <div className="mt-16 text-center">
                    <p className="text-zinc-200 text-2xl md:text-3xl font-heading font-bold max-w-4xl mx-auto leading-relaxed">
                        This replaces Buffer + Canva + Mailchimp + HubSpot + a freelance writer + a video editor - and does the work for you.
                    </p>
                </div>

                {/* Trust signals */}
                <div className="mt-8 text-center space-y-2">
                    <p className="text-zinc-400 text-xl md:text-2xl font-medium">Your data is yours. Cancel anytime. No lock-in contracts.</p>
                </div>

                {/* Contact section - replacing "Enterprise Grade Support" */}
                <div className="mt-24 glass-panel p-12 rounded-3xl border border-white/10">
                    <div className="grid md:grid-cols-2 gap-12 items-center">
                        <div>
                            <h3 className="text-3xl font-bold font-heading mb-4">Need Something Specific?</h3>
                            <p className="text-zinc-400 text-lg font-light leading-relaxed">
                                Every founding member gets a direct onboarding call. For agencies, multiple brand profiles, or custom requirements - talk to Arno directly.
                            </p>
                        </div>
                        <div className="flex justify-center md:justify-end">
                            <Link to="/contact">
                                <Button variant="outline" className="px-10 py-6 text-lg rounded-full border-white/20 hover:bg-white/5 transition-all">
                                    Contact Arno
                                </Button>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    )
}

export default PricingPage
