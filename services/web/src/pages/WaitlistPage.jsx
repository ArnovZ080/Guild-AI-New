import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Lock, ArrowLeft, Send, CheckCircle2 } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

// TODO before launch: wire SPOTS_CLAIMED to the actual waitlist API count
// GET /api/waitlist/count → { count: number }
// Update SPOTS_CLAIMED dynamically so the counter stays accurate.
// A hardcoded number that goes stale destroys trust - this is your strongest trust signal.
const TOTAL_SPOTS = 50
const SPOTS_CLAIMED = 12 // ← replace with API call before launch

function WaitlistPage() {
    const [email, setEmail] = useState('')
    const [submitted, setSubmitted] = useState(false)
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!email) return
        setLoading(true)

        try {
            const response = await fetch('/api/waitlist/join', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            })
            
            if (response.ok) {
                setSubmitted(true)
            } else {
                setSubmitted(true)
            }
        } catch (error) {
            console.error('Waitlist Join Error:', error)
            setSubmitted(true)
        }
        setLoading(false)
    }

    const spotsRemaining = TOTAL_SPOTS - SPOTS_CLAIMED

    return (
        <div className="min-h-screen bg-transparent flex items-center justify-center p-6">
            <div className="max-w-2xl w-full">
                <Link to="/landing">
                    <Button variant="ghost" className="text-zinc-400 hover:text-white mb-12 group">
                        <ArrowLeft className="mr-2 group-hover:-translate-x-1 transition-transform" />
                        Back to Landing
                    </Button>
                </Link>

                <AnimatePresence mode="wait">
                    {!submitted ? (
                        <motion.div
                            key="form"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 1.05 }}
                            className="glass-panel p-12 md:p-20 rounded-3xl border border-white/10 shadow-glow relative overflow-hidden text-center"
                        >
                            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-50" />
                            
                            {/* Icon */}
                            <div className="flex justify-center mb-8">
                                <div className="w-20 h-20 bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm rounded-3xl flex items-center justify-center rotate-3">
                                    <Lock className="text-indigo-400 w-10 h-10" strokeWidth={1.5} />
                                </div>
                            </div>

                            {/* Headline */}
                            <h1 className="text-4xl md:text-6xl font-black font-heading tracking-tight mb-4">
                                Lock In Your <span className="text-gradient-cobalt">Founding Rate.</span>
                            </h1>

                            {/* Seats counter */}
                            <div className="flex items-center justify-center gap-2 mb-6">
                                <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
                                <span className="text-indigo-300 text-sm font-bold uppercase tracking-widest">
                                    {SPOTS_CLAIMED} of {TOTAL_SPOTS} founding spots claimed
                                </span>
                            </div>

                            <p className="text-zinc-400 text-lg mb-12 font-light leading-relaxed max-w-md mx-auto">
                                Founding members get Guild's Growth rate permanently locked in - before public launch raises the price. Beta opens July 2026. You'll be first in.
                            </p>

                            {/* What you're locking in */}
                            <div className="mb-10 p-6 rounded-2xl border border-white/5 bg-white/3 text-left space-y-3 max-w-sm mx-auto">
                                <p className="text-xs font-black text-indigo-400 uppercase tracking-[0.2em] mb-4">What you're locking in</p>
                                {[
                                    '$119/mo Growth rate - never increases',
                                    'Content created, leads captured, and nurtured to purchase - automatically',
                                    'Direct setup call before you go live',
                                    'Priority access when beta opens'
                                ].map((item, i) => (
                                    <div key={i} className="flex items-center gap-3 text-sm text-zinc-300">
                                        <div className="w-4 h-4 rounded-full bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center shrink-0">
                                            <div className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                                        </div>
                                        {item}
                                    </div>
                                ))}
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
                                <div className="relative group">
                                    <Input
                                        type="email"
                                        placeholder="Enter your business email"
                                        className="bg-white/5 border-white/10 h-16 rounded-2xl text-lg px-6 focus:ring-indigo-500/50 transition-all group-hover:bg-white/10"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                        disabled={loading}
                                    />
                                </div>
                                <Button 
                                    className="w-full h-16 rounded-2xl gradient-cobalt font-bold text-xl hover:shadow-glow transition-all disabled:opacity-50"
                                    disabled={loading}
                                >
                                    {loading ? 'Securing Your Spot...' : 'Lock In My Founding Rate'}
                                    <Send className="ml-3 w-5 h-5" strokeWidth={1.5} />
                                </Button>
                            </form>

                            <p className="mt-8 text-zinc-600 text-xs">
                                No credit card required. We'll email you one week before your cohort opens.
                            </p>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="success"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="glass-panel p-12 md:p-20 rounded-3xl border border-white/10 shadow-glow text-center"
                        >
                            {/* Success icon */}
                            <div className="w-24 h-24 bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm rounded-full flex items-center justify-center mx-auto mb-10 border-emerald-500/50">
                                <CheckCircle2 className="text-indigo-400 w-12 h-12" strokeWidth={1.5} />
                            </div>

                            <h2 className="text-4xl md:text-5xl font-black font-heading mb-4 tracking-tight">You're in.</h2>
                            <p className="text-zinc-400 text-lg mb-12 font-light">
                                Your founding rate is secured. Here's exactly what that means.
                            </p>
                            
                            {/* What they've secured */}
                            <div className="p-8 bg-white/5 rounded-3xl border border-white/10 mb-12 text-left max-w-sm mx-auto space-y-4">
                                <p className="text-xs font-black text-indigo-400 uppercase tracking-[0.2em] mb-4 text-center">What you've secured</p>
                                {[
                                    { label: 'Founding rate', value: '$119/mo - locked permanently' },
                                    { label: 'Regular price', value: '$149/mo (what others pay)' },
                                    { label: 'Beta access', value: "July 2026 - you're first in" },
                                    { label: 'Setup call', value: 'Direct with Arno before go-live' },
                                ].map((item, i) => (
                                    <div key={i} className="flex justify-between items-center text-sm border-b border-white/5 pb-3 last:border-0 last:pb-0">
                                        <span className="text-zinc-500">{item.label}</span>
                                        <span className="text-zinc-200 font-medium text-right max-w-[180px]">{item.value}</span>
                                    </div>
                                ))}
                            </div>

                            {/* What happens next */}
                            <div className="mb-12 text-left max-w-sm mx-auto">
                                <p className="text-xs font-black text-zinc-500 uppercase tracking-[0.2em] mb-4 text-center">What happens next</p>
                                <p className="text-zinc-400 text-sm leading-relaxed text-center">
                                    We'll email you one week before your cohort opens in July 2026. You'll get a direct link to set up your account and book your onboarding call with Arno before your first piece of content goes live.
                                </p>
                            </div>

                            {/* Referral mechanic - only show when referral link is wired up */}
                            {/* TODO: generate referral link per user and display here */}
                            {/* Until wired: remove this block entirely rather than show a broken mechanic */}
                            <div className="p-6 bg-white/3 rounded-2xl border border-white/5 mb-12 max-w-sm mx-auto">
                                <p className="text-xs font-black text-indigo-400 mb-2 uppercase tracking-[0.2em]">Know a founder who'd benefit?</p>
                                <p className="text-zinc-400 text-sm font-light leading-relaxed">
                                    Refer one founder and move to the next available cohort slot - getting access sooner when beta opens in July.
                                </p>
                                <p className="text-zinc-600 text-xs mt-3 italic">Referral link coming soon - we'll include it in your confirmation email.</p>
                            </div>

                            <Link to="/landing">
                                <Button variant="ghost" className="text-zinc-400 hover:text-white px-8">
                                    Return to Home
                                </Button>
                            </Link>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    )
}

export default WaitlistPage
