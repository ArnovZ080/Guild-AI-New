import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { 
  ArrowLeft, Shield, TrendingUp, Zap, Brain, 
  Target, Users, Workflow, BarChart3, FileCheck, Clock,
  Database, Globe, Lock, Cpu, MessageSquare, CheckCircle2,
  Sparkles, Layers, Search, Rocket
} from 'lucide-react'
import { motion } from 'framer-motion'

function FeaturesPage() {
  const coreFeatures = [
    {
      icon: <Shield className="w-6 h-6" />,
      title: 'Judge Layer™ QA',
      description: 'Every output is automatically validated before you see it. True quality assurance using reasoning models to verify factuality and brand alignment.',
      benefits: ['Zero-slop generation', 'Automatic fact-verification', 'Brand voice enforcement'],
      color: 'from-blue-500 to-indigo-500'
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'Recursive Learning Engine',
      description: 'The platform learns from your feedback and performance data. Your workforce gets smarter every day based on actual results.',
      benefits: ['Custom model fine-tuning', 'Identity-first reasoning', 'Performance-led iteration'],
      color: 'from-indigo-500 to-purple-500'
    },
    {
      icon: <Layers className="w-6 h-6" />,
      title: '114 Specialized Agents',
      description: 'Not generic chatbots. We have 114 hyper-specialized agents like "Retention Specialist", "Growth Orchestrator", and "Rubric Designer".',
      benefits: ['Task-specific expertise', 'Inter-agent coordination', 'Agent Activity Theater view'],
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: <Brain className="text-pink-400 group-hover:scale-110 transition-transform" />,
      title: 'Source of Truth Hub',
      description: 'Centralized knowledge graph of your business niche, ICP, goals, and legacy. The foundation for all autonomous actions.',
      benefits: ['One-click context injection', 'Multi-source RAG sync', 'Centralized brand identity'],
      color: 'from-pink-500 to-rose-500'
    }
  ]

  const capabilityGrids = [
    { icon: <Workflow />, title: 'Visual Orchestration', desc: 'Watch agents collaborate in real-time.' },
    { icon: <Globe />, title: '123 Integrations', desc: 'LinkedIn, HubSpot, QuickBooks, and 120+ more.' },
    { icon: <Lock />, title: 'Enterprise Privacy', desc: 'Your data is never used to train public models.' },
    { icon: <Cpu />, title: 'Vertex AI 3.0', desc: 'Powered by Gemini 2.0 and Imagen 3 / Veo 3.' },
    { icon: <Search />, title: 'Smart Prospecting', desc: 'Autonomous lead scraping and enrichment.' },
    { icon: <MessageSquare />, title: 'Omnichannel Nurture', desc: 'SMS, Email, and Social automation in one place.' },
    { icon: <Rocket />, title: 'Fast Setup', desc: 'Deployment in 20 minutes via Source of Truth.' },
    { icon: <Target />, title: 'Goal-Based Execution', desc: 'Tell the agents the goal; they plan the tasks.' }
  ]

  return (
    <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
      <div className="container mx-auto max-w-6xl">
        <Link to="/landing">
          <Button variant="ghost" className="text-zinc-500 hover:text-white mb-12 group">
            <ArrowLeft className="mr-2 group-hover:-translate-x-1 transition-transform" />
            Back to Landing
          </Button>
        </Link>

        {/* Hero */}
        <section className="text-center mb-32">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-panel border border-white/10 text-xs font-bold tracking-widest text-indigo-400 mb-8 uppercase">
                    <Sparkles size={14} /> The Competitive Edge
                </div>
                <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                    Built for <br /> <span className="text-gradient-cobalt">Autonomous ROI</span>
                </h1>
                <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
                    Most AI platforms are just interfaces for LLMs. Guild AI is an integrated workforce architecture 
                    designed to move leads through the flywheel with zero manual intervention.
                </p>
            </motion.div>
        </section>

        {/* Core Pillars */}
        <div className="grid md:grid-cols-2 gap-8 mb-32">
            {coreFeatures.map((f, i) => (
                <div key={i} className="glass-panel p-10 rounded-3xl group hover:border-indigo-500/20 transition-all">
                    <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${f.color} flex items-center justify-center text-white mb-8 shadow-glow-sm`}>
                        {f.icon}
                    </div>
                    <h3 className="text-3xl font-bold font-heading mb-4">{f.title}</h3>
                    <p className="text-zinc-500 mb-8 font-light leading-relaxed">{f.description}</p>
                    <div className="space-y-3">
                        {f.benefits.map((b, bi) => (
                            <div key={bi} className="flex gap-3 items-center text-sm">
                                <CheckCircle2 size={16} className="text-indigo-500" />
                                <span className="text-zinc-400">{b}</span>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>

        {/* Technical Capabilities */}
        <section className="mb-32">
            <div className="text-center mb-16">
                <h2 className="text-4xl font-bold font-heading tracking-tight mb-4">Deep Platform Capabilities</h2>
                <p className="text-zinc-500">A full-stack ecosystem for modern business growth.</p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {capabilityGrids.map((c, i) => (
                    <div key={i} className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                        <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                            {c.icon}
                        </div>
                        <h4 className="font-bold text-sm mb-1">{c.title}</h4>
                        <p className="text-[10px] text-zinc-500 leading-normal font-light">{c.desc}</p>
                    </div>
                ))}
            </div>
        </section>

        {/* CTA */}
        <section className="container mx-auto max-w-4xl">
            <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow overflow-hidden relative">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500 to-transparent" />
                <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Deploy your workforce in minutes.</h2>
                <p className="text-zinc-500 mb-10 text-lg font-light">Join 12,000+ businesses scaling autonomously with Guild.</p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Link to="/signup">
                        <Button size="lg" className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-12 py-8 text-xl font-bold border-t border-white/20 w-full sm:w-auto">
                            Get Started
                        </Button>
                    </Link>
                    <Link to="/contact">
                        <Button variant="outline" size="lg" className="rounded-full px-12 py-8 text-xl border-white/10 text-white w-full sm:w-auto">
                            Book a Demo
                        </Button>
                    </Link>
                </div>
            </div>
        </section>
      </div>
    </div>
  )
}

export default FeaturesPage
