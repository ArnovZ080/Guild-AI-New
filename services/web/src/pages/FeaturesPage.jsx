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

  return (
    <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
      <div className="container mx-auto max-w-6xl">
        <Link to="/landing">
          <Button variant="ghost" className="text-zinc-400 hover:text-white mb-12 group">
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
                    <Sparkles size={14} /> Everything you need to grow
                </div>
                <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                    One Platform. <br /> <span className="text-gradient-cobalt">Every Tool You Need.</span>
                </h1>
                <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
                    Content creation, scheduling, lead capture, email follow-ups, and performance tracking - all in one place, all on-brand, all connected.
                </p>
            </motion.div>
        </section>

        {/* Core Pillars */}
        <div className="grid md:grid-cols-2 gap-8 mb-32">
            <div className="glass-panel p-10 rounded-3xl group hover:border-indigo-500/20 transition-all">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white mb-8 shadow-glow-sm">
                    <Shield className="w-6 h-6" />
                </div>
                <h3 className="text-3xl font-bold font-heading mb-4">Brand Quality on Every Piece</h3>
                <p className="text-zinc-400 mb-8 font-light leading-relaxed">Every post, email, and video passes through automated quality checks before you see it. Brand voice, factual accuracy, SEO, and audience targeting - all verified.</p>
                <div className="space-y-3">
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">No generic AI content</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Consistent brand voice everywhere</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">You approve everything before it goes live</span>
                    </div>
                </div>
            </div>
            <div className="glass-panel p-10 rounded-3xl group hover:border-indigo-500/20 transition-all">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white mb-8 shadow-glow-sm">
                    <TrendingUp className="w-6 h-6" />
                </div>
                <h3 className="text-3xl font-bold font-heading mb-4">Gets Smarter Every Week</h3>
                <p className="text-zinc-400 mb-8 font-light leading-relaxed">Guild tracks which content gets engagement, which leads convert, and which messages get responses. Then it adjusts your strategy automatically.</p>
                <div className="space-y-3">
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Learns what works for your business</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Suggests strategy changes based on real data</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Performance improves month over month</span>
                    </div>
                </div>
            </div>
            <div className="glass-panel p-10 rounded-3xl group hover:border-indigo-500/20 transition-all">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white mb-8 shadow-glow-sm">
                    <Layers className="w-6 h-6" />
                </div>
                <h3 className="text-3xl font-bold font-heading mb-4">Content Across Every Format</h3>
                <p className="text-zinc-400 mb-8 font-light leading-relaxed">Blog posts, social media updates, Instagram reels, carousels, email newsletters, ad creatives, and AI-generated video - all from one system that knows your brand.</p>
                <div className="space-y-3">
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Text, images, and video - all on-brand</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Platform-specific formatting (LinkedIn ≠ Instagram)</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Generate a full week of content in minutes</span>
                    </div>
                </div>
            </div>
            <div className="glass-panel p-10 rounded-3xl group hover:border-indigo-500/20 transition-all">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center text-white mb-8 shadow-glow-sm">
                    <Brain className="w-6 h-6" />
                </div>
                <h3 className="text-3xl font-bold font-heading mb-4">Knows Your Business Deeply</h3>
                <p className="text-zinc-400 mb-8 font-light leading-relaxed">Guild learns through conversation and from every document you upload - product details, brand guidelines, customer profiles, even industry research. The longer you use it, the better it gets.</p>
                <div className="space-y-3">
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Upload any document to make Guild smarter</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Business context injected into every piece of content</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Your competitive advantage grows over time</span>
                    </div>
                </div>
            </div>
        </div>

        {/* Technical Capabilities */}
        <section className="mb-32">
            <div className="text-center mb-16">
                <h2 className="text-4xl font-bold font-heading tracking-tight mb-4">Deep Platform Capabilities</h2>
                <p className="text-zinc-400">A full-stack ecosystem for modern business growth.</p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Workflow />
                    </div>
                    <h4 className="font-bold text-sm mb-1">See What's Happening</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Watch your AI team work in real-time with full transparency.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Globe />
                    </div>
                    <h4 className="font-bold text-sm mb-1">30+ Integrations</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Instagram, LinkedIn, Mailchimp, HubSpot, Google Ads, and more.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Lock />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Your Data Is Private</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Your business data is never shared or used to train public models.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Sparkles />
                    </div>
                    <h4 className="font-bold text-sm mb-1">AI Video & Images</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Professional-quality graphics and short-form video, generated in minutes.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Search />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Finds Your Leads</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">People who engage with your content are captured and scored automatically.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <MessageSquare />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Automated Follow-Ups</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Email sequences that nurture leads from first touch to sale.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Rocket />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Ready in 10 Minutes</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Tell Guild about your business and start creating content the same day.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Target />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Goal Tracking</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Set business goals. Guild tracks progress and repeats what works.</p>
                </div>
            </div>
        </section>

        {/* CTA */}
        <section className="container mx-auto max-w-4xl">
            <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow overflow-hidden relative">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500 to-transparent" />
                <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Start Growing Your Business Today</h2>
                <p className="text-zinc-400 mb-10 text-lg font-light">Free trial. No credit card required.</p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Link to="/signup">
                        <Button size="lg" className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-12 py-8 text-xl font-bold border-t border-white/20 w-full sm:w-auto">
                            Start Your Free Trial
                        </Button>
                    </Link>
                    <Link to="/how-it-works">
                        <Button variant="outline" size="lg" className="rounded-full px-12 py-8 text-xl border-white/10 text-white w-full sm:w-auto">
                            See How It Works
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
