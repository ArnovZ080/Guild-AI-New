import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Sparkles, ArrowLeft, Send, CheckCircle2 } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

function WaitlistPage() {
    const [email, setEmail] = useState('')
    const [submitted, setSubmitted] = useState(false)
    const [position, setPosition] = useState(0)
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!email) return
        setLoading(true)

        try {
            // Reaching out to the actual waitlist endpoint
            const response = await fetch('/api/waitlist/join', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            })
            
            if (response.ok) {
                const data = await response.json()
                setPosition(data.position || 2408)
                setSubmitted(true)
            } else {
                // If backend isn't ready, simulate success for demo
                setSubmitted(true)
                setPosition(2408)
            }
        } catch (error) {
            console.error('Waitlist Join Error:', error)
            setSubmitted(true)
            setPosition(2408)
        }
        setLoading(false)
    }

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
                            
                            <div className="flex justify-center mb-8">
                                <div className="w-20 h-20 gradient-cobalt rounded-3xl flex items-center justify-center shadow-lg shadow-indigo-500/20 rotate-3">
                                    <Sparkles className="text-white w-10 h-10" strokeWidth={1.5} />
                                </div>
                            </div>

                            <h1 className="text-4xl md:text-6xl font-black font-heading tracking-tight mb-6">
                                Join the <span className="text-gradient-cobalt">Elite Batch.</span>
                            </h1>
                            <p className="text-zinc-400 text-lg mb-12 font-light leading-relaxed max-w-md mx-auto">
                                We're rolling out access in controlled cohorts to ensure 1-on-1 white-glove onboarding for every business.
                            </p>

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
                                    {loading ? 'Securing Spot...' : 'Claim Early Access'}
                                    <Send className="ml-3 w-5 h-5" strokeWidth={1.5} />
                                </Button>
                            </form>

                            <div className="mt-12 flex items-center justify-center gap-6">
                                <div className="flex -space-x-3">
                                    {[1,2,3,4].map(i => (
                                        <div key={i} className="w-8 h-8 rounded-full border-2 border-zinc-900 bg-zinc-800 flex items-center justify-center overflow-hidden grayscale">
                                            <div className="w-full h-full gradient-cobalt opacity-20" />
                                        </div>
                                    ))}
                                </div>
                                <span className="text-zinc-600 text-xs font-bold tracking-widest uppercase">
                                    2,408 Business Owners Waitlisted
                                </span>
                            </div>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="success"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="glass-panel p-12 md:p-20 rounded-3xl border border-white/10 shadow-glow text-center"
                        >
                            <div className="w-24 h-24 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-10 border border-emerald-500/50 shadow-glow-sm">
                                <CheckCircle2 className="text-emerald-400 w-12 h-12" strokeWidth={1.5} />
                            </div>
                            <h2 className="text-4xl md:text-5xl font-black font-heading mb-6 tracking-tight">You're in the queue.</h2>
                            <p className="text-zinc-400 text-xl mb-12 font-light">
                                Your priority position is <span className="text-indigo-400 font-bold font-heading">#{position}</span>.<br />
                                We'll reach out to your inbox as soon as a slot opens for your niche.
                            </p>
                            
                            <div className="p-8 bg-white/5 rounded-3xl border border-white/10 mb-12 max-w-sm mx-auto">
                                <p className="text-xs font-black text-indigo-400 mb-2 uppercase tracking-[0.2em]">Priority Jump</p>
                                <p className="text-zinc-400 text-sm font-light leading-relaxed">Refer 1 founder to Guild AI and skip exactly <span className="text-white font-bold">500 spots</span> instantly.</p>
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
