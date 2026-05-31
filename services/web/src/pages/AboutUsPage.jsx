import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import {
  ArrowLeft, Lightbulb, Heart, Shield, Zap, Sparkles
} from 'lucide-react'
import { motion } from 'framer-motion'
import guildLogo from '@/assets/guild-logo.png'

function AboutUsPage() {
  const navigate = useNavigate()

  const values = [
    {
      icon: <Shield />,
      title: 'Quality Before You See It',
      description: 'Every piece of content passes through an automated quality layer before it reaches you - checked against your brand voice, your ideal customer, and your accuracy standards. You only review what\'s already worth approving.',
      color: 'blue-500'
    },
    {
      icon: <Lightbulb />,
      title: 'You Stay in Control',
      description: 'Guild shows you what it\'s doing and why. Every decision is visible, every piece of content requires your approval, and you can adjust the strategy at any time. Automation without blind trust.',
      color: 'blue-500'
    },
    {
      icon: <Heart />,
      title: 'Built for the Founder, Not the Enterprise',
      description: 'Not for corporate marketing teams. Not for developers. For the business owner who does everything and needs the one tool that actually closes the loop - from content all the way to customers.',
      color: 'blue-500'
    },
    {
      icon: <Zap />,
      title: 'From First Post to Paying Customer',
      description: 'Any tool can create content. Guild creates it, publishes it, captures every lead who engages, and nurtures them to purchase - as one connected system that gets smarter every cycle.',
      color: 'blue-500'
    }
  ]

  const milestones = [
    {
      year: '2025',
      title: 'The Frustration',
      description: 'We watched smart business owners juggle 6–8 separate marketing tools, spend 10+ hours a week on content, and still struggle to turn any of it into customers. The tools weren\'t the problem. The gap between content and conversion was.'
    },
    {
      year: 'EARLY 2026',
      title: 'The Rebuild',
      description: 'We scrapped the first attempt and started over with a focused vision: one system that handles the complete journey from content to customer. No bloat. No shortcuts. Every component connected to the next.'
    },
    {
      year: 'MID 2026',
      title: 'The Launch',
      description: 'Guild opens to its founding cohort - 50 business owners who lock in their rate before public launch. A complete growth engine: content created, quality-checked, published, leads captured, nurtured to sale. All on-brand. All in one place.'
    }
  ]

  return (
    <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
      {/* Nav Link */}
      <div className="container mx-auto max-w-6xl mb-12">
        <Link to="/landing">
          <Button variant="ghost" className="text-zinc-400 hover:text-white group">
            <ArrowLeft className="mr-2 group-hover:-translate-x-1 transition-transform" />
            Back to Landing
          </Button>
        </Link>
      </div>

      {/* Hero */}
      <section className="container mx-auto max-w-6xl text-center mb-32">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <div className="w-20 h-20 rounded-2xl bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center mx-auto mb-8 shadow-2xl">
            <img src={guildLogo} alt="Guild" className="w-12 h-12" />
          </div>
          <h1 className="text-5xl md:text-7xl font-bold font-heading tracking-tight mb-8">
            Built for Business Owners, <br />
            <span className="text-gradient-cobalt">Not Marketing Teams</span>
          </h1>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto leading-relaxed font-light">
            Guild exists because small business owners deserve the same growth power as companies with full marketing teams - without the headcount, the tool sprawl, or the hours of manual work every week.
          </p>
        </motion.div>
      </section>

      {/* Story */}
      <section className="container mx-auto max-w-4xl mb-32">
        <div className="glass-panel p-12 rounded-3xl relative overflow-hidden">
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <Sparkles size={80} className="text-indigo-400" />
          </div>
          <h2 className="text-3xl font-bold font-heading mb-4">Why Guild Exists</h2>
          <p className="text-indigo-300 text-lg font-medium mb-8 leading-relaxed border-l-2 border-indigo-500/40 pl-4">
            "What would it take to make the whole thing work, end to end, without the founder being the glue?" - that's the only question Guild was built to answer.
          </p>
          <div className="space-y-6 text-zinc-400 leading-relaxed text-lg font-light">
            <p>
              I built Guild out of a specific frustration. After 25 years working with businesses across strategy, operations, and growth, I kept seeing the same pattern: smart founders spending 10+ hours a week on marketing that wasn't converting. Not because they lacked talent or effort - but because every tool they used handled one piece of the job and left the rest to them.
            </p>
            <p>
              Create content in one tool. Schedule it in another. Capture leads somewhere else. Follow up manually. Track results in a spreadsheet. The "automation" still required constant attention. The loop was never closed.
            </p>
            <p>
              Guild closes the loop. It learns your business through a guided conversation, creates content that genuinely sounds like you, checks it before you ever see it, publishes it at the right time, captures every person who engages, and nurtures them toward purchase - as one connected system that gets smarter every cycle.
            </p>
            <p className="text-zinc-300 font-medium not-italic">
              That's the only question we asked when we built it: what would it take to make the whole thing work, end to end, without the founder being the glue?
            </p>
          </div>
          <div className="mt-10 pt-8 border-t border-white/5">
            <p className="text-sm text-zinc-500 font-medium">- Arno, Founder of Guild AI</p>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="container mx-auto max-w-6xl mb-32">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold font-heading mb-4 tracking-tight">What We Actually Believe</h2>
          <p className="text-zinc-400">The principles behind every decision we make.</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {values.map((v, i) => (
            <div key={i} className="glass-panel p-8 rounded-2xl group hover:border-indigo-500/30 transition-all">
              <div className={`w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center text-indigo-400 mb-6 shadow-glow-sm`}>
                {v.icon}
              </div>
              <h3 className="text-xl font-bold font-heading mb-3">{v.title}</h3>
              <p className="text-base text-zinc-400 leading-relaxed font-light">{v.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Milestones */}
      <section className="container mx-auto max-w-5xl mb-32">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold font-heading mb-4 tracking-tight">How We Got Here</h2>
        </div>
        <div className="space-y-8 relative before:absolute before:inset-0 before:ml-10 before:-z-10 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-indigo-500 before:to-transparent">
          {milestones.map((m, i) => (
            <div key={i} className="flex gap-10 items-start">
              <div className="w-20 h-20 rounded-full glass-panel flex items-center justify-center shrink-0 border border-white/10 shadow-glow-sm bg-zinc-900 font-heading font-black text-xs tracking-tighter text-indigo-400">
                {m.year}
              </div>
              <div className="glass-panel p-8 rounded-2xl flex-1 border border-white/10">
                <h4 className="text-xl font-bold font-heading mb-2">{m.title}</h4>
                <p className="text-base text-zinc-400 font-light leading-relaxed">{m.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto max-w-4xl">
        <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-400/40 shadow-glow-sm shadow-glow relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500/20 to-transparent" />
          <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Join the Founding Cohort</h2>
          <p className="text-zinc-400 mb-3 text-lg font-light">50 spots. Your rate locked in before public launch. Beta opens July 2026.</p>
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
  )
}

export default AboutUsPage
