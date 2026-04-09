import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import {
  Sparkles, ArrowLeft, Search, Users, TrendingUp, DollarSign,
  FileText, Briefcase, Shield, Brain, Zap, Globe, Target, Layers,
  Rocket, SearchIcon
} from 'lucide-react'
import { motion } from 'framer-motion'

function AIAgentsPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  const categories = [
    { id: 'all', name: 'Launch Fleet', count: 14, icon: <Rocket size={14}/> },
    { id: 'marketing_sales', name: 'Growth & CRM', count: 6, icon: <TrendingUp size={14}/> },
    { id: 'content_creative', name: 'Production', count: 3, icon: <FileText size={14}/> },
    { id: 'intelligence', name: 'Intelligence', count: 3, icon: <Brain size={14}/> },
    { id: 'ops', name: 'Operations', count: 2, icon: <Layers size={14}/> }
  ]

  const agents = [
    // Core Flywheel
    { name: 'OrchestratorAgent', category: 'ops', description: 'Central intelligence — decomposes goals, delegates, and coordinates the entire fleet.' },
    { name: 'ContentMarketingAgent', category: 'content_creative', description: 'Creates all text content across formats and platforms with platform-specific optimization.' },
    { name: 'CopywriterAgent', category: 'content_creative', description: 'Generates high-converting copy for ads, emails, and landing pages with brand voice enforcement.' },
    { name: 'CreativeProductionAgent', category: 'content_creative', description: 'Visualizes concepts using Imagen 3 and Veo 3 for high-fidelity images and social videos.' },
    { name: 'GrowthAgent', category: 'marketing_sales', description: 'Drives SEO, paid ads strategy, and social growth planning through recursive data analysis.' },
    { name: 'CampaignAgent', category: 'marketing_sales', description: 'Orchestrates multi-platform campaigns and performs real-time A/B optimization.' },
    { name: 'LeadAgent', category: 'marketing_sales', description: 'Automates lead qualification, scoring, and personalization of every outreach touchpoint.' },
    { name: 'SalesPipelineAgent', category: 'marketing_sales', description: 'Manages the outreach funnel, optimizes pipelines, and executes nurture campaigns.' },
    { name: 'CRMAgent', category: 'marketing_sales', description: 'Synchronizes client data, logs interactions, and automates CRM pipeline maintenance.' },
    { name: 'CustomerIntelligenceAgent', category: 'intelligence', description: 'Analyzes target audience behavior, segments profiles, and predicts churn events.' },
    { name: 'CalendarHarmonyAgent', category: 'ops', description: 'Smart scheduling assistant that learns behavioral patterns to optimize your executive focus.' },
    { name: 'JudgeAgent', category: 'intelligence', description: 'Advanced Quality Assurance that evaluates every output against brand, ICP, and SEO rubrics.' },
    { name: 'ResearchAgent', category: 'intelligence', description: 'Continuous web research, competitor monitoring, and industry trend detection.' },
    { name: 'ContentIntelligenceAgent', category: 'marketing_sales', description: 'Analyzes performance data to refine content strategy and detect new growth gaps.' }
  ]

  const filteredAgents = agents.filter(agent => {
    const matchesCategory = selectedCategory === 'all' || agent.category === selectedCategory
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         agent.description.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesCategory && matchesSearch
  })

  return (
    <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
      <div className="container mx-auto max-w-7xl">
        <Link to="/landing">
          <Button variant="ghost" className="text-zinc-500 hover:text-white mb-12 group">
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
                    <Sparkles size={14} /> The Launch Fleet: 14 Elite Agents
                </div>
                <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                    Your Autonomous <br /> <span className="text-gradient-cobalt">Workforce</span>
                </h1>
                <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
                    A hyper-specialized fleet of agents optimized for the Content-to-Customer Flywheel. 
                    Working 24/7 to solve your business growth.
                </p>
            </motion.div>
        </section>

        {/* Directory */}
        <section className="mb-32">
            <div className="max-w-6xl mx-auto">
                <div className="flex flex-col md:flex-row gap-6 mb-12">
                    <div className="relative flex-1">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600" size={18} />
                        <Input 
                            placeholder="Find flywheel capabilities..." 
                            className="pl-12 py-7 bg-transparent border-white/10 rounded-2xl text-lg focus:ring-indigo-500/50"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                    <div className="flex flex-wrap gap-2 items-center">
                        {categories.map((c) => (
                            <button
                                key={c.id}
                                onClick={() => setSelectedCategory(c.id)}
                                className={`px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center gap-2 ${selectedCategory === c.id ? 'glass-panel border-indigo-500/50 text-white shadow-glow-sm' : 'text-zinc-500 hover:text-zinc-300'}`}
                            >
                                <span className="text-indigo-400">{c.icon}</span> {c.name}
                                <span className="px-1.5 py-0.5 rounded-md text-[10px] border border-white/10">{c.count}</span>
                            </button>
                        ))}
                    </div>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredAgents.map((agent, i) => (
                        <motion.div 
                            key={i} 
                            initial={{ opacity: 0, y: 10 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            viewport={{ once: true }}
                            className="glass-panel p-8 rounded-2xl transition-all group border-white/10"
                        >
                            <div className="flex justify-between items-start mb-4">
                                <h4 className="text-lg font-bold font-heading group-hover:text-indigo-400 transition-colors uppercase tracking-tight">{agent.name}</h4>
                                <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 group-hover:bg-indigo-500 group-hover:text-white transition-all">
                                    <Zap size={14} />
                                </div>
                            </div>
                            <p className="text-sm text-zinc-500 leading-relaxed font-light">{agent.description}</p>
                            <div className="mt-6 flex items-center gap-2">
                                <div className="h-px flex-1 bg-white/5" />
                                <span className="text-[10px] font-black tracking-widest uppercase text-zinc-600">Active v2.0</span>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>

        {/* Future Expansion */}
        <section className="mb-32 text-center">
            <div className="inline-flex items-center gap-2 px-6 py-2 rounded-full border border-white/10 text-xs font-bold text-zinc-500 mb-12">
                <Layers size={14} /> 100+ SPECIALIZED AGENTS COMING POST-LAUNCH
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 opacity-30 grayscale">
                {['Financial Advisor', 'Chief of Staff', 'Contract Analyzer', 'Talent Scout', 'Brand Architect', 'Competitor Monitor'].map((name) => (
                    <div key={name} className="glass-panel p-4 rounded-xl text-[10px] font-bold uppercase tracking-tight">
                        {name}
                    </div>
                ))}
            </div>
        </section>

        {/* CTA */}
        <section className="container mx-auto max-w-4xl">
            <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow">
                <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Hire the Flywheel.</h2>
                <p className="text-zinc-500 mb-10 text-lg font-light">The complete content-to-customer engine. Synchronized and autonomous.</p>
                <Link to="/signup">
                    <Button size="lg" className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-12 py-8 text-xl font-bold border-t border-white/20">
                        Initial Onboarding
                    </Button>
                </Link>
            </div>
        </section>
      </div>
    </div>
  )
}

export default AIAgentsPage
