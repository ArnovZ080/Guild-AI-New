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
    { id: 'all', name: 'All Platforms', count: 21, icon: <Globe size={14} /> },
    { id: 'marketing', name: 'Social & Ads', count: 8, icon: <BarChart3 size={14} /> },
    { id: 'email_crm', name: 'Email & CRM', count: 6, icon: <Mail size={14} /> },
    { id: 'ops', name: 'Calendar & Tools', count: 7, icon: <Briefcase size={14} /> }
  ]

  const integrations = [
    // Social & Ads
    { name: 'LinkedIn', category: 'marketing', description: 'Publish articles, posts, and updates. Grow your professional audience.', icon: <Users size={18} />, color: 'from-blue-600 to-blue-800' },
    { name: 'Instagram', category: 'marketing', description: 'Publish posts, stories, and AI-generated reels automatically.', icon: <Image size={18} />, color: 'from-purple-500 to-pink-500' },
    { name: 'Facebook', category: 'marketing', description: 'Schedule page posts and manage community engagement.', icon: <Facebook size={18} />, color: 'from-blue-500 to-blue-700' },
    { name: 'Twitter/X', category: 'marketing', description: 'Post updates, threads, and engage with trending topics.', icon: <Zap size={18} />, color: 'from-zinc-800 to-black' },
    { name: 'Meta Ads', category: 'marketing', description: 'Create ad visuals and copy. Launch campaigns with AI-optimised targeting.', icon: <BarChart3 size={18} />, color: 'from-blue-400 to-indigo-500' },
    { name: 'Google Ads', category: 'marketing', description: 'Generate search and display ads based on keyword research.', icon: <Target size={18} />, color: 'from-yellow-400 to-red-500' },
    { name: 'WordPress', category: 'marketing', description: 'Publish SEO-optimised blog posts directly to your site.', icon: <Layout size={18} />, color: 'from-blue-800 to-blue-900' },
    { name: 'Shopify', category: 'marketing', description: 'Create product-focused content and blog posts for your store.', icon: <ShoppingCart size={18} />, color: 'from-emerald-500 to-green-600' },

    // Email & CRM
    { name: 'HubSpot', category: 'email_crm', description: 'Sync contacts, track deals, and automate your sales sales process.', icon: <Database size={18} />, color: 'from-orange-500 to-orange-600' },
    { name: 'Pipedrive', category: 'email_crm', description: 'Manage your sales sales process and log every customer interaction.', icon: <Briefcase size={18} />, color: 'from-zinc-800 to-zinc-900' },
    { name: 'Built-in CRM', category: 'email_crm', description: 'Guild\'s own contact manager - capture leads from content engagement automatically.', icon: <Check size={18} />, color: 'from-indigo-600 to-blue-600' },
    { name: 'SendGrid', category: 'email_crm', description: 'Send transactional emails and automated nurture sequences.', icon: <Mail size={18} />, color: 'from-blue-400 to-blue-500' },
    { name: 'Mailchimp', category: 'email_crm', description: 'Manage email lists and send newsletters to your subscribers.', icon: <MessageSquare size={18} />, color: 'from-yellow-500 to-yellow-600' },
    { name: 'ConvertKit', category: 'email_crm', description: 'Advanced email sequences for creators and course sellers.', icon: <Folder size={18} />, color: 'from-indigo-400 to-indigo-500' },

    // Calendar & Tools
    { name: 'Google Calendar', category: 'ops', description: 'Sync your schedule so content never clashes with your meetings.', icon: <Calendar size={18} />, color: 'from-blue-500 to-blue-600' },
    { name: 'Outlook', category: 'ops', description: 'Connect your work calendar for conflict-free content scheduling.', icon: <Calendar size={18} />, color: 'from-blue-600 to-blue-700' },
    { name: 'Slack', category: 'ops', description: 'Get notifications and approve content without opening Guild.', icon: <MessageSquare size={18} />, color: 'from-purple-500 to-pink-500' },
    { name: 'Gmail', category: 'ops', description: 'Send follow-up emails and track replies from your own address.', icon: <Mail size={18} />, color: 'from-red-500 to-red-600' },
    { name: 'WhatsApp', category: 'ops', description: 'Reach customers directly on the platform they use most.', icon: <MessageSquare size={18} />, color: 'from-emerald-500 to-emerald-600' },
    { name: 'Stripe', category: 'ops', description: 'Track payments and understand which customers are most valuable.', icon: <DollarSign size={18} />, color: 'from-indigo-500 to-purple-500' },
    { name: 'Paystack', category: 'ops', description: 'Accept payments from customers across Africa and beyond.', icon: <CreditCard size={18} />, color: 'from-blue-400 to-blue-600' }
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
                    <Globe size={14} /> Works with your existing tools
                </div>
                <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                    Connect the Tools <br /> <span className="text-gradient-cobalt">You Already Use</span>
                </h1>
                <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
                    Guild plugs into the platforms where your audience already is and the tools you already pay for. Connect in one click - no code required.
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
                            className={`px-4 py-2.5 rounded-xl text-sm font-medium transition-all flex items-center gap-2 ${selectedCategory === c.id ? 'glass-panel border-indigo-500/50 text-white shadow-glow-sm' : 'text-zinc-400 hover:text-zinc-300'}`}
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
                        </div>
                        <p className="text-base text-zinc-400 leading-relaxed font-light">{it.description}</p>
                    </motion.div>
                ))}
            </div>
            
            <div className="mt-20 text-center">
                <div className="inline-flex items-center gap-2 px-6 py-2 rounded-full border border-white/10 text-xs font-bold text-zinc-500 uppercase tracking-widest">
                    More integrations coming soon. Request one →
                </div>
            </div>
        </section>

        {/* CTA */}
        <section className="container mx-auto max-w-4xl">
            <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow">
                <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Connect Your Tools in One Click</h2>
                <p className="text-zinc-400 mb-10 text-lg font-light">No code. No setup fees. Just connect and go.</p>
                <Link to="/signup">
                    <Button size="lg" className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-12 py-8 text-xl font-bold border-t border-white/20">
                        Start Your Free Trial
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
