import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { 
  ArrowLeft, Lightbulb, Heart, Shield, Zap, Sparkles
} from 'lucide-react'
import { motion } from 'framer-motion'
import guildLogo from '@/assets/guild-logo.png'

function AboutUsPage() {
  const values = [
    {
        icon: <Shield />,
        title: 'Quality You Can Trust',
        description: 'Every piece of content is checked for brand voice, accuracy, and quality before you see it. You approve everything  -  nothing goes live without your say.',
        color: 'from-blue-500 to-indigo-500'
    },
    {
        icon: <Lightbulb />,
        title: 'You Stay in Control',
        description: 'Guild shows you what it\'s doing and why. You can see every decision, approve every piece of content, and adjust the strategy at any time.',
        color: 'from-indigo-500 to-purple-500'
    },
    {
        icon: <Heart />,
        title: 'Built for Small Business',
        description: 'Not for enterprises. Not for developers. For the solopreneur, the small team, the founder who does everything and needs one less thing to worry about.',
        color: 'from-purple-500 to-pink-500'
    },
    {
        icon: <Zap />,
        title: 'It Actually Works',
        description: 'Not a chatbot you have to prompt 50 times. Tell Guild what you want to achieve, and it plans, creates, and executes  -  then reports back on what happened.',
        color: 'from-pink-500 to-rose-500'
    }
  ]

  const milestones = [
    {
        year: '2025',
        title: 'The Problem',
        description: 'We watched small business owners juggle 6-8 separate marketing tools and spend 10+ hours a week on content that wasn\'t growing their business. We knew AI could do better.'
    },
    {
        year: 'EARLY 2026',
        title: 'The Rebuild',
        description: 'We scrapped our first attempt and started over with a focused vision: one system that handles the complete journey from content to customer. No bloat. No shortcuts.'
    },
    {
        year: 'MID 2026',
        title: 'The Launch',
        description: 'Guild opens to beta users  -  a complete growth engine that creates content, publishes it, captures leads, and nurtures them to sale. All on-brand. All in one place.'
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
          <div className="w-20 h-20 rounded-2xl border border-white/10 glass-panel flex items-center justify-center mx-auto mb-8 shadow-2xl">
            <img src={guildLogo} alt="Guild" className="w-12 h-12" />
          </div>
          <h1 className="text-5xl md:text-7xl font-bold font-heading tracking-tight mb-8">
            Built for Business Owners, <br />
            <span className="text-gradient-cobalt">Not Developers</span>
          </h1>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto leading-relaxed font-light">
            Guild was built because small business owners deserve the same marketing power as big companies  -  without hiring a team, learning complicated tools, or spending hours on content every week.
          </p>
        </motion.div>
      </section>

      {/* Story */}
      <section className="container mx-auto max-w-4xl mb-32">
        <div className="glass-panel p-12 rounded-3xl relative overflow-hidden">
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <Sparkles size={80} className="text-indigo-400" />
          </div>
          <h2 className="text-3xl font-bold font-heading mb-8">Our Story</h2>
          <div className="space-y-6 text-zinc-400 leading-relaxed text-lg font-light">
            <p>
              Guild started with a frustration every small business owner knows: you're told AI will save you time, but every tool you try needs you to write the prompts, check the output, copy it to another app, schedule it manually, and track the results in a spreadsheet. The 'automation' still takes 10 hours a week.
            </p>
            <p>
              We asked a different question: what if one system could handle everything  -  create the content, check that it sounds like you, publish it at the right time, and follow up with the people who engage? Not as separate features, but as one connected process that gets smarter the longer you use it.
            </p>
            <p>
              That's what we built. Guild learns your business, creates your content, publishes it, captures leads, and nurtures them  -  all on-brand, all connected, all in one place. And it gets better every week because it learns what works for your specific business.
            </p>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="container mx-auto max-w-6xl mb-32">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold font-heading mb-4 tracking-tight">Core Values</h2>
          <p className="text-zinc-400">The principles that guide every line of code we write.</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {values.map((v, i) => (
            <div key={i} className="glass-panel p-8 rounded-2xl group hover:border-indigo-500/30 transition-all">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${v.color} flex items-center justify-center text-white mb-6 shadow-lg`}>
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
            <h2 className="text-4xl font-bold font-heading mb-4 tracking-tight">Our Journey</h2>
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
        <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500/20 to-transparent" />
          <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Ready to Let Guild Handle Your Marketing?</h2>
          <p className="text-zinc-400 mb-10 text-lg font-light">Start your free trial today. No credit card required.</p>
          <Link to="/signup">
            <Button size="lg" className="bg-white text-black hover:bg-zinc-200 rounded-full px-12 py-8 text-xl font-bold transition-all hover:scale-105 active:scale-95 shadow-2xl">
              Start Your Free Trial
            </Button>
          </Link>
        </div>
      </section>
    </div>
  )
}

export default AboutUsPage
