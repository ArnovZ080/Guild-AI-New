import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { 
  Sparkles, ArrowLeft, Search, Check, Globe, Zap,
  Mail, Calendar, FileText, Database, Cloud, Code,
  MessageSquare, ShoppingCart, DollarSign, Users,
  BarChart3, Briefcase, Image, Video, Music, Folder,
  Instagram, Facebook, Twitter, Ghost, Layout
} from 'lucide-react'
import { motion } from 'framer-motion'

function IntegrationsPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  const categories = [
    { id: 'all', name: 'Launch Set', count: 21, icon: <Globe size={14} /> },
    { id: 'marketing', name: 'Ads & Social', count: 8, icon: <BarChart3 size={14} /> },
    { id: 'email_crm', name: 'Email & CRM', count: 6, icon: <Mail size={14} /> },
    { id: 'ops', name: 'Ops & Productivity', count: 7, icon: <Briefcase size={14} /> }
  ]

  const integrations = [
    // Publishing & Ads
    { name: 'LinkedIn', category: 'marketing', description: 'Native social selling and professional presence orchestration.', icon: <Users size={18} />, color: 'from-blue-600 to-blue-800' },
    { name: 'Instagram', category: 'marketing', description: 'Visual storytelling via Imagen 3 and automated reel publishing.', icon: <Image size={18} />, color: 'from-purple-500 to-pink-500' },
    { name: 'Facebook', category: 'marketing', description: 'Community management and automated page updates.', icon: <Facebook size={18} />, color: 'from-blue-500 to-blue-700' },
    { name: 'Twitter/X', category: 'marketing', description: 'Real-time trending content creation and thread drafting.', icon: <Zap size={18} />, color: 'from-zinc-800 to-black' },
    { name: 'Meta Ads', category: 'marketing', description: 'Autonomous creative generation and budget optimization.', icon: <BarChart3 size={18} />, color: 'from-blue-400 to-indigo-500' },
    { name: 'Google Ads', category: 'marketing', description: 'Keyword research and search-intent ad orchestration.', icon: <Target size={18} />, color: 'from-yellow-400 to-red-500' },
    { name: 'WordPress', category: 'marketing', description: 'Full-cycle blog production and SEO optimization sync.', icon: <Layout size={18} />, color: 'from-blue-800 to-blue-900' },
    { name: 'Shopify', category: 'marketing', description: 'Product-focused content creation for e-commerce growth.', icon: <ShoppingCart size={18} />, color: 'from-emerald-500 to-green-600' },

    // Email & CRM
    { name: 'HubSpot', category: 'email_crm', description: 'Deep contact intelligence and automated lead progression.', icon: <Database size={18} />, color: 'from-orange-500 to-orange-600' },
    { name: 'Pipedrive', category: 'email_crm', description: 'Sales pipeline automation and touchpoint tracking.', icon: <Briefcase size={18} />, color: 'from-zinc-800 to-zinc-900' },
    { name: 'Built-in CRM', category: 'email_crm', description: 'Guild\'s native lightweight CRM for content-first lead capture.', icon: <Check size={18} />, color: 'from-indigo-600 to-blue-600' },
    { name: 'SendGrid', category: 'email_crm', description: 'High-performance transactional and sequence delivery.', icon: <Mail size={18} />, color: 'from-blue-400 to-blue-500' },
    { name: 'Mailchimp', category: 'email_crm', description: 'Creative newsletter sync and audience segmentation.', icon: <MessageSquare size={18} />, color: 'from-yellow-500 to-yellow-600' },
    { name: 'ConvertKit', category: 'email_crm', description: 'Advanced creator-focused nurture automation sync.', icon: <Folder size={18} />, color: 'from-indigo-400 to-indigo-500' },

    // Ops
    { name: 'Google Calendar', category: 'ops', description: 'Autonomous session booking and focus-block management.', icon: <Calendar size={18} />, color: 'from-blue-500 to-blue-600' },
    { name: 'Outlook', category: 'ops', description: 'Professional scheduling and thread-aware coordination.', icon: <Calendar size={18} />, color: 'from-blue-600 to-blue-700' },
    { name: 'Slack', category: 'ops', description: 'Real-time human-in-the-loop triggers and agent streaming.', icon: <MessageSquare size={18} />, color: 'from-purple-500 to-pink-500' },
    { name: 'Gmail', category: 'ops', description: 'Communication analysis and automated follow-up drafting.', icon: <Mail size={18} />, color: 'from-red-500 to-red-600' },
    { name: 'WhatsApp', category: 'ops', description: 'Direct customer engagement and nurture orchestration.', icon: <MessageSquare size={18} />, color: 'from-emerald-500 to-emerald-600' },
    { name: 'Stripe', category: 'ops', description: 'Revenue intelligence and customer LTV analysis.', icon: <DollarSign size={18} />, color: 'from-indigo-500 to-purple-500' },
    { name: 'Paystack', category: 'ops', description: 'Global billing and regional payment orchestration.', icon: <CreditCard size={18} />, color: 'from-blue-400 to-blue-600' }
  ]

  const filteredIntegrations = integrations.filter(it => {
    const matchesCategory = selectedCategory === 'all' || it.category === selectedCategory
    const matchesSearch = it.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         it.description.toLowerCase().includes(searchQuery.toLowerCase())
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
                    <Globe size={14} /> Launch Ecosystem: 21 Critical Nodes
                </div>
                <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                    Connect Your <br /> <span className="text-gradient-cobalt">Flywheel Stack</span>
                </h1>
                <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
                    Guild AI doesn't live in a silo. We connect to your existing toolstack to record intelligence, 
                    execute strategy, and capture customers where they already live.
                </p>
            </motion.div>
        </section>

        {/* Search / Filter */}
        <section className="mb-24 max-w-6xl mx-auto">
            <div className="flex flex-col md:flex-row gap-6 mb-12">
                <div className="relative flex-1">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600" size={18} />
                    <Input 
                        placeholder="Search launch integrations..." 
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
                        </button>
                    ))}
                </div>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredIntegrations.map((it, i) => (
                    <motion.div 
                        key={i} 
                        initial={{ opacity: 0, scale: 0.98 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        transition={{ delay: i * 0.05 }}
                        className="glass-panel p-8 rounded-2xl group transition-all border-white/10"
                    >
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-600 to-blue-600 flex items-center justify-center text-white mb-6 shadow-lg group-hover:scale-110 transition-transform shadow-indigo-500/20">
                            {it.icon || <Zap size={20} />}
                        </div>
                        <div className="flex justify-between items-center mb-3">
                             <h4 className="text-lg font-bold font-heading">{it.name}</h4>
                             <Badge className="bg-indigo-500/10 text-indigo-400 border-none text-[8px] uppercase tracking-widest font-black">Active v2</Badge>
                        </div>
                        <p className="text-sm text-zinc-500 leading-relaxed font-light">{it.description}</p>
                    </motion.div>
                ))}
            </div>
            
            <div className="mt-20 text-center">
                <div className="inline-flex items-center gap-2 px-6 py-2 rounded-full border border-white/10 text-xs font-bold text-zinc-600 uppercase tracking-widest">
                    + 100 More Automations Coming Q3 2026
                </div>
            </div>
        </section>

        {/* CTA */}
        <section className="container mx-auto max-w-4xl">
            <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow">
                <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Ready to integrate?</h2>
                <p className="text-zinc-500 mb-10 text-lg font-light">Join the automated future. No more manual data entry or siloed workflows.</p>
                <Link to="/signup">
                    <Button size="lg" className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-12 py-8 text-xl font-bold border-t border-white/20">
                        Connect My Fleet
                    </Button>
                </Link>
            </div>
        </section>
      </div>
    </div>
  )
}

function CreditCard(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <rect width="20" height="14" x="2" y="5" rx="2" />
      <line x1="2" x2="22" y1="10" y2="10" />
    </svg>
  )
}

function Target(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <circle cx="12" cy="12" r="6" />
      <circle cx="12" cy="12" r="2" />
    </svg>
  )
}

export default IntegrationsPage
