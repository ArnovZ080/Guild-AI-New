import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { 
  ArrowLeft, Shield, TrendingUp, Zap, Brain, 
  Target, Users, Workflow, BarChart3, FileCheck, Clock,
  Database, Globe, Lock, Cpu, MessageSquare, CheckCircle2,
  Sparkles, Layers, Search, Rocket
} from 'lucide-react'
import { motion } from 'framer-motion'

function FeaturesPage() {
  const navigate = useNavigate()

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
                    <Sparkles size={14} /> The only platform that closes the full loop
                </div>
                <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                    Every Feature Exists <br /> <span className="text-gradient-cobalt">to Get You Customers.</span>
                </h1>
                <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
                    Not to impress you on a features page. Every capability in Guild connects to the next — from learning your business, to creating content, to capturing leads, to closing sales. One loop. No gaps.
                </p>
            </motion.div>
        </section>

        {/* Core Pillars */}
        <div className="grid md:grid-cols-2 gap-8 mb-32">
            <div className="glass-panel p-10 rounded-3xl group hover:border-indigo-500/20 transition-all">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white mb-8 shadow-glow-sm">
                    <Shield className="w-6 h-6" />
                </div>
                <h3 className="text-3xl font-bold font-heading mb-4">Content That Checks Itself Before You See It</h3>
                <p className="text-zinc-400 mb-8 font-light leading-relaxed">Before any piece of content reaches you, Guild's quality layer has already checked it against your brand voice, your ideal customer profile, your SEO requirements, and your factual accuracy standards. You only review what's already worth approving. No other platform does this.</p>
                <div className="space-y-3">
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">No generic AI output — ever</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Consistent brand voice across every platform</span>
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
                <h3 className="text-3xl font-bold font-heading mb-4">Gets Smarter the Longer You Use It</h3>
                <p className="text-zinc-400 mb-8 font-light leading-relaxed">Content that performs well shapes the next campaign. Leads that convert refine who gets targeted next. Guild builds a compounding understanding of your business — making it more valuable every month, and making switching feel pointless.</p>
                <div className="space-y-3">
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Learns what content drives sales for your business</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Strategy adjusts automatically based on real results</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Performance improves month over month, not week over week</span>
                    </div>
                </div>
            </div>
            <div className="glass-panel p-10 rounded-3xl group hover:border-indigo-500/20 transition-all">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white mb-8 shadow-glow-sm">
                    <Layers className="w-6 h-6" />
                </div>
                <h3 className="text-3xl font-bold font-heading mb-4">Every Content Format. One System.</h3>
                <p className="text-zinc-400 mb-8 font-light leading-relaxed">Blog posts, social updates, Instagram reels, carousels, email newsletters, ad creatives, and AI-generated video — all from one system that knows your brand deeply. No switching tools. No reformatting. No re-briefing a designer.</p>
                <div className="space-y-3">
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Text, images, and AI video — all on-brand</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Platform-specific formatting (LinkedIn ≠ Instagram)</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">A full week of content generated in minutes</span>
                    </div>
                </div>
            </div>
            <div className="glass-panel p-10 rounded-3xl group hover:border-indigo-500/20 transition-all">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center text-white mb-8 shadow-glow-sm">
                    <Brain className="w-6 h-6" />
                </div>
                <h3 className="text-3xl font-bold font-heading mb-4">Knows Your Business. Not Just Your Industry.</h3>
                <p className="text-zinc-400 mb-8 font-light leading-relaxed">Guild learns through conversation and from every document you upload — product details, brand guidelines, customer profiles, past campaigns, even competitor research. Every piece of context makes every future output sharper.</p>
                <div className="space-y-3">
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Upload any document to make Guild smarter instantly</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Business context injected into every piece of content</span>
                    </div>
                    <div className="flex gap-3 items-center text-sm">
                        <CheckCircle2 size={16} className="text-indigo-500" />
                        <span className="text-zinc-400">Your competitive edge compounds over time</span>
                    </div>
                </div>
            </div>
        </div>

        {/* Technical Capabilities */}
        <section className="mb-32">
            <div className="text-center mb-16">
                <h2 className="text-4xl font-bold font-heading tracking-tight mb-4">Everything Working Together</h2>
                <p className="text-zinc-400">Every capability connects. No gaps in the loop.</p>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Workflow />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Full Transparency</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Watch your content pipeline work in real-time. See every decision, every check, every output.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Globe />
                    </div>
                    <h4 className="font-bold text-sm mb-1">60+ Integrations</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Instagram, LinkedIn, Mailchimp, HubSpot, Shopify, Google Ads, and more — connected from day one.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Lock />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Your Data Is Private</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Your business data is never shared, never sold, and never used to train public models.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Sparkles />
                    </div>
                    <h4 className="font-bold text-sm mb-1">AI Video & Images</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Professional graphics and short-form video, generated in minutes and checked for brand alignment before you see them.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Search />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Lead Capture Built In</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Anyone who engages with your content is captured and scored against your ideal customer profile. Automatically.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <MessageSquare />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Automated Nurture Sequences</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Personalised email sequences that move leads from first touch to purchase — written in your voice, sent at the right time.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Rocket />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Live in 10 Minutes</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Complete your Business Identity conversation and your first week of content is ready for review the same day.</p>
                </div>
                <div className="glass-panel p-6 rounded-2xl hover:bg-white/5 transition-colors text-center md:text-left">
                    <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 mx-auto md:mx-0">
                        <Target />
                    </div>
                    <h4 className="font-bold text-sm mb-1">Goal-Driven Strategy</h4>
                    <p className="text-sm text-zinc-400 leading-normal font-light">Set your business goals. Guild tracks what's working, reports back, and automatically does more of what's converting.</p>
                </div>
            </div>
        </section>

        {/* CTA */}
        <section className="container mx-auto max-w-4xl">
            <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow overflow-hidden relative">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500 to-transparent" />
                <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">See It Working on Your Business</h2>
                <p className="text-zinc-400 mb-3 text-lg font-light">Join the founding cohort and lock in your rate before public launch.</p>
                <p className="text-zinc-600 text-sm mb-10">50 spots. Beta opens July 2026. Rate locked permanently.</p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Button
                        size="lg"
                        className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-12 py-8 text-xl font-bold border-t border-white/20 w-full sm:w-auto"
                        onClick={() => navigate('/waitlist')}
                    >
                        Claim Founding Access
                    </Button>
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
