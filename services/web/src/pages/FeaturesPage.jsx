import { useState } from 'react'
import Footer from '@/components/Footer'
import { Link, useNavigate } from 'react-router-dom'
import { ShinyButton } from '@/components/ui/shiny-button'
import {
  ArrowLeft, Shield, TrendingUp, Brain,
  Target, Workflow, Globe, Lock,
  Sparkles, Layers, Search, MessageSquare, Rocket,
  CheckCircle2, Check
} from 'lucide-react'
import { motion } from 'framer-motion'
import { fadeUp, scaleIn, staggerContainer, viewportOnce } from '@/lib/transitions'

// ── Mini animated previews shown on hover ──────────────────────────────

function TypewriterPreview() {
  const lines = [
    { text: 'Checking brand voice…', done: true },
    { text: 'SEO alignment…', done: true },
    { text: 'Ideal customer fit…', done: true },
    { text: 'Ready to review ✓', done: false, highlight: true },
  ]
  return (
    <div className="font-mono text-xs space-y-1.5 p-3 rounded-lg bg-black/40 border border-white/8">
      {lines.map((l, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, x: -8 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.3, duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
          className={`flex items-center gap-2 ${l.highlight ? 'text-emerald-400' : 'text-zinc-400'}`}
        >
          {l.done && <Check size={10} className="text-indigo-400 shrink-0" />}
          {l.highlight && <Sparkles size={10} className="shrink-0" />}
          {l.text}
        </motion.div>
      ))}
    </div>
  )
}

function BarChartPreview() {
  const bars = [40, 55, 48, 70, 65, 85, 90]
  return (
    <div className="flex items-end gap-1.5 h-16 px-3">
      {bars.map((h, i) => (
        <motion.div
          key={i}
          initial={{ height: 0 }}
          animate={{ height: `${h}%` }}
          transition={{ delay: i * 0.08, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="flex-1 rounded-t-sm"
          style={{ background: `rgba(94,106,210,${0.4 + i * 0.08})` }}
        />
      ))}
    </div>
  )
}

function PlatformPreview() {
  const platforms = ['IG', 'LI', '✉', 'FB', '▶', 'GA']
  return (
    <div className="flex flex-wrap gap-2 p-3">
      {platforms.map((p, i) => (
        <motion.div
          key={i}
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: i * 0.1, duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
          className="w-9 h-9 rounded-xl bg-indigo-500/15 border border-indigo-400/30 flex items-center justify-center text-xs font-bold text-indigo-300"
        >
          {p}
        </motion.div>
      ))}
    </div>
  )
}

function LeadPreview() {
  const leads = [
    { name: 'Sarah M.', score: 94, hot: true },
    { name: 'James T.', score: 78, hot: true },
    { name: 'Priya K.', score: 61, hot: false },
  ]
  return (
    <div className="space-y-2 p-3">
      {leads.map((l, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, x: 12 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.15, duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
          className="flex items-center justify-between text-xs"
        >
          <span className="text-zinc-300 font-medium">{l.name}</span>
          <div className="flex items-center gap-2">
            <div className="w-16 h-1.5 rounded-full bg-white/10">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${l.score}%` }}
                transition={{ delay: i * 0.15 + 0.2, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
                className="h-full rounded-full"
                style={{ background: l.hot ? '#5E6AD2' : '#52586A' }}
              />
            </div>
            <span className={l.hot ? 'text-indigo-400 font-bold' : 'text-zinc-500'}>{l.score}</span>
          </div>
        </motion.div>
      ))}
    </div>
  )
}

// ── Bento cell ──────────────────────────────────────────────────────────

function BentoCell({ icon: Icon, title, description, checks, preview: Preview, span = '', accent = false }) {
  const [hovered, setHovered] = useState(false)

  return (
    <motion.div
      variants={scaleIn}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      whileHover={{ y: -3, transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] } }}
      className={`glass-panel rounded-2xl p-7 relative overflow-hidden flex flex-col gap-4 cursor-default
        ${span}
        ${accent ? 'border-indigo-500/30' : ''}
        transition-colors duration-300 hover:border-indigo-400/25`}
    >
      {/* Permanent subtle top glow - more intense on hover */}
      <div
        className="absolute inset-0 pointer-events-none rounded-2xl transition-opacity duration-300"
        style={{
          background: 'radial-gradient(ellipse at 30% 0%, rgba(94,106,210,0.08) 0%, transparent 70%)',
          opacity: hovered ? 2 : 1,
        }}
      />

      <div className="flex items-start justify-between gap-4">
        <div className={`w-11 h-11 rounded-xl flex items-center justify-center text-indigo-400 shrink-0 transition-all duration-300
          ${hovered ? 'bg-indigo-500/20 border-indigo-400/50 scale-110' : 'bg-indigo-500/10 border border-indigo-400/30'}`}>
          <Icon size={20} strokeWidth={1.5} />
        </div>
        {accent && (
          <span className="label-eyebrow text-indigo-400/60 text-[9px]">Core feature</span>
        )}
      </div>

      <div>
        <h3 className="font-bold text-base leading-snug mb-2">{title}</h3>
        <p className="text-sm text-zinc-400 leading-relaxed font-light">{description}</p>
      </div>

      {/* Live preview - always visible, not just on hover */}
      {Preview && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3, duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="mt-auto"
        >
          <Preview />
        </motion.div>
      )}

      {checks && !Preview && (
        <ul className="space-y-2 mt-auto">
          {checks.map((c, i) => (
            <li key={i} className="flex items-center gap-2 text-xs text-zinc-400">
              <CheckCircle2 size={12} className="text-indigo-500 shrink-0" />
              {c}
            </li>
          ))}
        </ul>
      )}
    </motion.div>
  )
}

// ── Page ────────────────────────────────────────────────────────────────

function FeaturesPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
      <div className="container mx-auto max-w-6xl">
        <Link to="/landing">
          <button className="text-zinc-500 hover:text-white mb-12 flex items-center gap-2 text-sm transition-colors group">
            <ArrowLeft size={14} className="group-hover:-translate-x-1 transition-transform" />
            Back to Landing
          </button>
        </Link>

        {/* Hero */}
        <section className="text-center mb-20">
          <motion.div
            variants={staggerContainer}
            initial="hidden"
            animate="visible"
          >
            <motion.div variants={fadeUp} className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-panel border border-white/8 text-xs label-eyebrow text-indigo-400 mb-8">
              <Sparkles size={12} /> The only platform that closes the full loop
            </motion.div>
            <motion.h1 variants={fadeUp} className="text-5xl md:text-7xl font-bold leading-[1.1] tracking-tight mb-6">
              Every Feature Exists <br />
              <span className="text-gradient-cobalt">to Get You Customers.</span>
            </motion.h1>
            <motion.p variants={fadeUp} className="text-lg text-zinc-500 max-w-2xl mx-auto font-light leading-relaxed">
              Not to impress you on a features page. Every capability connects - from learning your business, to creating content, to capturing leads, to closing sales.
            </motion.p>
          </motion.div>
        </section>

        {/* Bento Grid */}
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-20 auto-rows-auto"
        >
          {/* Hero cell - 2 cols */}
          <BentoCell
            icon={Shield}
            title="Content That Checks Itself Before You See It"
            description="Guild's quality layer checks every piece against your brand voice, ICP, SEO standards, and accuracy before it reaches you. You only review what's already worth approving."
            preview={TypewriterPreview}
            accent
            span="md:col-span-2"
          />

          {/* Gets smarter */}
          <BentoCell
            icon={TrendingUp}
            title="Gets Smarter Every Cycle"
            description="Content that converts shapes the next campaign. Leads that buy refine targeting. Compounding value, month over month."
            preview={BarChartPreview}
          />

          {/* Every format */}
          <BentoCell
            icon={Layers}
            title="Every Format. One System."
            description="Blog posts, reels, carousels, emails, ads - all on-brand, all formatted for each platform, all in minutes."
            preview={PlatformPreview}
          />

          {/* Lead capture */}
          <BentoCell
            icon={Search}
            title="Lead Capture Built In"
            description="Every engagement becomes a scored lead in your CRM. No spreadsheets. No manual tracking."
            preview={LeadPreview}
          />

          {/* Knows your business */}
          <BentoCell
            icon={Brain}
            title="Knows Your Business, Not Just Your Industry"
            description="Upload your brand guide, product docs, competitor research. Every future output reflects everything it learns."
            checks={['Upload any document instantly', 'Context injected into every piece', 'Your edge compounds over time']}
          />

          {/* Integrations */}
          <BentoCell
            icon={Globe}
            title="21 Integrations at Launch"
            description="Instagram, LinkedIn, Mailchimp, HubSpot, Shopify, Google Ads - connected from day one."
            checks={['No switching tools', 'More added regularly', 'One-click connect']}
          />

          {/* Privacy */}
          <BentoCell
            icon={Lock}
            title="Your Data Is Private"
            description="Never shared, never sold, never used to train public models. Your business context stays yours."
            checks={['No third-party sharing', 'No public model training', 'You own everything']}
          />

          {/* Nurture */}
          <BentoCell
            icon={MessageSquare}
            title="Automated Nurture Sequences"
            description="Personalised email sequences written in your voice, sent at the right moment - from first touch to purchase."
            checks={['Written in your voice', 'Pre-approved by you', 'Timed to engagement signals']}
            span="md:col-span-2"
          />

          {/* Speed */}
          <BentoCell
            icon={Rocket}
            title="Live in 10 Minutes"
            description="Tell Guild about your business in a short conversation and your first week of content is ready the same day."
            checks={['10-min onboarding', 'Same-day first batch', 'No technical setup']}
          />
        </motion.div>

        {/* CTA */}
        <section className="max-w-4xl mx-auto">
          <motion.div
            variants={fadeUp}
            initial="hidden"
            whileInView="visible"
            viewport={viewportOnce}
            className="glass-panel p-16 rounded-3xl text-center border border-indigo-400/30 relative overflow-hidden"
          >
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-px bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent" />
            <h2 className="text-4xl font-bold mb-6 tracking-tight">See It Working on Your Business</h2>
            <p className="text-zinc-500 mb-3 text-lg font-light">Join the founding cohort and lock in your rate before public launch.</p>
            <p className="text-zinc-600 text-sm mb-10">50 spots. Rate locked permanently.</p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <ShinyButton onClick={() => navigate('/waitlist')} className="text-base px-10 py-4">
                Claim Founding Access
              </ShinyButton>
              <Link to="/how-it-works">
                <button className="text-zinc-400 hover:text-white border border-white/10 hover:border-white/20 rounded-full px-10 py-4 text-base transition-all">
                  See How It Works
                </button>
              </Link>
            </div>
          </motion.div>
        </section>
      </div>
      <Footer />
    </div>
  )
}

export default FeaturesPage
