import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { 
  Sparkles, ArrowLeft, Users, TrendingUp, DollarSign,
  FileText, Briefcase, Shield, Brain, Zap, Globe, Target, Layers,
  Rocket, MessageSquare, CheckCircle2, Clock
} from 'lucide-react'
import { motion } from 'framer-motion'

function HowItWorksPage() {
  const navigate = useNavigate()

  const steps = [
    {
        step: '01',
        title: 'Tell Guild about your business',
        description: 'A natural conversation — not a form. Guild asks about what you do, who your customers are, what your brand sounds like, and what you\'re trying to achieve. Takes about 10 minutes. You can come back and add more at any time.',
        detail: 'Upload your product catalogue, brand guidelines, or any business documents. Guild reads them immediately and every future piece of content reflects what it learns.'
    },
    {
        step: '02',
        title: 'Guild creates your content — and checks it before you see it',
        description: "Blog posts, social media updates, reels, email newsletters, ad creatives — all written and designed in your exact brand voice, formatted correctly for each platform. Before any of it reaches you, Guild's quality layer checks every piece for brand consistency, factual accuracy, SEO alignment, and ideal customer fit.",
        detail: 'This is what makes Guild different from every other AI content tool. You only ever review content that has already passed quality control. No prompting. No filtering. No fixing.'
    },
    {
        step: '03',
        title: 'You review and approve',
        description: 'Scroll through your content queue. Approve with one tap, edit anything you want to adjust, or ask Guild to regenerate with feedback. You are always in control — nothing goes live without your say.',
        detail: 'Most founders spend 5–10 minutes reviewing a full week of content. That\'s it.'
    },
    {
        step: '04',
        title: 'Content publishes automatically',
        description: 'Approved content goes live on the right platform at the right time, without you lifting a finger. Guild learns when your specific audience is most active and adjusts the schedule accordingly — syncing with your calendar so nothing clashes.',
        detail: 'Instagram at 6pm, LinkedIn at 12pm, email on Tuesday mornings — Guild works this out from your audience data, not generic best practices.'
    },
    {
        step: '05',
        title: 'Leads come to you',
        description: 'When someone comments, clicks, subscribes, or engages with your content, Guild captures them automatically. Each contact is scored against your ideal customer profile — high-scoring leads are flagged immediately so you know who to prioritise.',
        detail: 'No spreadsheets. No manual tracking. Every person who shows interest is in your CRM, scored, and ready for follow-up.'
    },
    {
        step: '06',
        title: 'Guild follows up — you close the deal',
        description: 'Personalised email sequences go out automatically — welcoming new contacts, sharing relevant content, building trust over time, and making the offer when the moment is right. Every message is written in your voice and pre-approved by you.',
        detail: 'Guild handles the nurture. You handle the conversation when a prospect is ready to buy. The loop closes itself.'
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

        {/* Hero */}
        <section className="text-center mb-24">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-panel border border-white/10 text-xs font-bold tracking-widest text-indigo-400 mb-8 uppercase">
                    <Clock size={14} /> From conversation to customers
                </div>
                <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                    Here's How <span className="text-gradient-cobalt">Guild Works</span>
                </h1>
                <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
                    You tell Guild about your business once. From there, it creates your content, publishes it, captures every lead who engages, and nurtures them toward purchase — as one connected system that gets smarter every cycle.
                </p>
            </motion.div>
        </section>

        {/* Step-by-Step Journey */}
        <section className="mb-24">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {steps.map((s, i) => (
                    <motion.div 
                        key={i} 
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1 }}
                        viewport={{ once: true }}
                        className="glass-panel p-8 rounded-3xl group border-white/10 hover:border-indigo-500/30 transition-all flex flex-col"
                    >
                        <div className="flex justify-between items-start mb-6">
                            <span className="text-5xl font-black text-indigo-500/10 group-hover:text-indigo-500/20 transition-colors uppercase font-heading">{s.step}</span>
                            <div className="p-3 rounded-2xl bg-indigo-500/5 text-indigo-400">
                                {i === 0 && <Brain size={24} />}
                                {i === 1 && <Sparkles size={24} />}
                                {i === 2 && <CheckCircle2 size={24} />}
                                {i === 3 && <Globe size={24} />}
                                {i === 4 && <Target size={24} />}
                                {i === 5 && <Users size={24} />}
                            </div>
                        </div>
                        <h3 className="text-2xl font-bold font-heading mb-4 leading-tight">{s.title}</h3>
                        <p className="text-base text-zinc-400 mb-6 font-light leading-relaxed flex-grow">{s.description}</p>
                        <div className="pt-6 border-t border-white/5">
                            <p className="text-xs uppercase tracking-widest font-black text-indigo-400/50 mb-2">Worth Knowing</p>
                            <p className="text-xs text-zinc-600 font-medium leading-relaxed italic">{s.detail}</p>
                        </div>
                    </motion.div>
                ))}
            </div>
        </section>

        {/* Founding member nudge */}
        <section className="mb-32 text-center">
            <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full glass-panel border border-indigo-500/20 text-sm">
                <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
                <span className="text-indigo-300 font-medium">Founding cohort open now — 50 spots before public launch in August 2026</span>
            </div>
        </section>

        {/* CTA */}
        <section className="container mx-auto max-w-4xl">
            <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500/20 to-transparent" />
                <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Ready to Close the Loop?</h2>
                <p className="text-zinc-400 mb-3 text-lg font-light">Join the founding cohort and lock in your rate before public launch.</p>
                <p className="text-zinc-600 text-sm mb-10">Your data is yours. Cancel anytime. No lock-in contracts.</p>
                <Button
                    size="lg"
                    className="bg-white text-black hover:bg-zinc-200 rounded-full px-12 py-8 text-xl font-bold transition-all hover:scale-105 active:scale-95 shadow-2xl"
                    onClick={() => navigate('/waitlist')}
                >
                    Claim Your Founding Rate
                </Button>
            </div>
        </section>
      </div>
    </div>
  )
}

export default HowItWorksPage
