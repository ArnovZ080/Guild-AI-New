import { Link, useNavigate } from 'react-router-dom'
import Footer from '@/components/Footer'
import { Button } from '@/components/ui/button'
import RadialOrbitalTimeline from '@/components/ui/radial-orbital-timeline'
import {
  ArrowLeft, Clock, Brain, Sparkles, CheckCircle2,
  Globe, Target, Users, TrendingUp
} from 'lucide-react'
import { motion } from 'framer-motion'

const timelineData = [
  {
    id: 1,
    title: "LEARN",
    category: "Onboarding",
    date: "Step 1",
    content: "Tell Guild about your business in a natural conversation — not a form. It learns your voice, your audience, your goals, and gets smarter every cycle.",
    icon: Brain,
    relatedIds: [2],
    status: "completed",
    energy: 100,
  },
  {
    id: 2,
    title: "CREATE",
    category: "Content",
    date: "Step 2",
    content: "Blog posts, social content, reels, emails, and ad creatives — written in your exact brand voice and quality-checked before you ever see them.",
    icon: Sparkles,
    relatedIds: [1, 3],
    status: "completed",
    energy: 95,
  },
  {
    id: 3,
    title: "APPROVE",
    category: "Review",
    date: "Step 3",
    content: "Scroll your content queue. Approve with one tap, edit anything, or ask Guild to regenerate. Most founders spend 5–10 minutes on a full week of content.",
    icon: CheckCircle2,
    relatedIds: [2, 4],
    status: "in-progress",
    energy: 80,
  },
  {
    id: 4,
    title: "PUBLISH",
    category: "Distribution",
    date: "Step 4",
    content: "Approved content goes live on the right platform at the right time automatically. Guild learns when your audience is most active and adjusts schedules accordingly.",
    icon: Globe,
    relatedIds: [3, 5],
    status: "in-progress",
    energy: 90,
  },
  {
    id: 5,
    title: "CAPTURE",
    category: "CRM",
    date: "Step 5",
    content: "Every person who engages with your content is captured in your CRM, scored against your ideal customer profile, and ready for follow-up. No spreadsheets.",
    icon: Target,
    relatedIds: [4, 6],
    status: "pending",
    energy: 70,
  },
  {
    id: 6,
    title: "NURTURE",
    category: "Automation",
    date: "Step 6",
    content: "Personalised follow-up sequences go out automatically — in your voice, pre-approved by you. Guild handles the nurture. You handle the close.",
    icon: Users,
    relatedIds: [5, 7],
    status: "pending",
    energy: 60,
  },
  {
    id: 7,
    title: "CONVERT",
    category: "Growth",
    date: "Step 7",
    content: "Guild tracks what content drives real sales and does more of it. Every cycle the system gets smarter about your business and your buyers.",
    icon: TrendingUp,
    relatedIds: [6, 1],
    status: "pending",
    energy: 85,
  },
]

function HowItWorksPage() {
  const navigate = useNavigate()

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
        <section className="text-center mb-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-panel border border-white/10 text-xs font-bold tracking-widest text-indigo-400 mb-8 uppercase">
              <Clock size={14} /> From conversation to customers
            </div>
            <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
              Here's How <span className="text-gradient-cobalt">Guild Works</span>
            </h1>
            <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
              One connected system. Seven steps. Fully automated. Click any node to explore each phase.
            </p>
          </motion.div>
        </section>

        {/* Orbital Timeline */}
        <section className="mb-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            <RadialOrbitalTimeline timelineData={timelineData} />
          </motion.div>
          <p className="text-center text-xs text-zinc-600 mt-2">
            Click any step to explore · Click the background to resume rotation
          </p>
        </section>

        {/* Founding member nudge */}
        <section className="mb-32 text-center">
          <div className="inline-flex items-center gap-3 px-6 py-3 rounded-full glass-panel border border-indigo-400/40 shadow-glow-sm text-sm">
            <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
            <span className="text-indigo-300 font-medium">Founding cohort open now — 50 spots before public launch in August 2026</span>
          </div>
        </section>

        {/* CTA */}
        <section className="container mx-auto max-w-4xl">
          <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-400/40 shadow-glow-sm shadow-glow relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500/20 to-transparent" />
            <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Ready to Turn Your Content Into Customers?</h2>
            <p className="text-zinc-400 mb-3 text-lg font-light">One system. Content created, published, leads captured, nurtured to sale.</p>
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
      <Footer />
    </div>
  )
}

export default HowItWorksPage
