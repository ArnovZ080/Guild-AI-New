import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { 
  ArrowLeft, Target, Lightbulb, Heart, Users,
  TrendingUp, Shield, Zap, Globe, Award, Rocket, Sparkles
} from 'lucide-react'
import { motion } from 'framer-motion'
import guildLogo from '@/assets/guild-logo.png'

function AboutUsPage() {
  const values = [
    {
      icon: <Shield className="w-6 h-6" />,
      title: 'Quality First',
      description: 'We built the Judge Layer because AI outputs should be guaranteed, not hoped for. Quality is non-negotiable.',
      color: 'from-blue-500 to-indigo-500'
    },
    {
      icon: <Lightbulb className="w-6 h-6" />,
      title: 'Educational Transparency',
      description: 'AI should teach, not just execute. Every action includes reasoning so you build business expertise while automating.',
      color: 'from-indigo-500 to-purple-500'
    },
    {
      icon: <Heart className="w-6 h-6" />,
      title: 'Solopreneur Focus',
      description: 'Built for lean teams and solo founders who need enterprise capabilities without enterprise complexity or cost.',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'True Autonomy',
      description: 'AI agents that actually work autonomously, not just glorified chatbots. Set goals and let them execute.',
      color: 'from-pink-500 to-rose-500'
    }
  ]

  const milestones = [
    {
      year: 'MAY 2025',
      title: 'THE SPARK',
      description: 'Guild AI was founded with a mission to democratize enterprise-grade automation for the solo-founder.'
    },
    {
      year: 'SEPT 2025',
      title: 'AGENT ECOSYSTEM',
      description: 'Reached 114 specialized AI agents and 123 platform integrations, creating a comprehensive workforce.'
    },
    {
      year: 'MARCH 2026',
      title: 'V2 FLYWHEEL',
      description: 'Transitioned to the Content-to-Customer Flywheel architecture, powered by Vertex AI Gemini 2.0.'
    }
  ]

  return (
    <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
      {/* Nav Link */}
      <div className="container mx-auto max-w-6xl mb-12">
        <Link to="/landing">
          <Button variant="ghost" className="text-zinc-500 hover:text-white group">
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
            Democratizing <br />
            <span className="text-gradient-cobalt">Autonomous Growth</span>
          </h1>
          <p className="text-xl text-zinc-400 max-w-3xl mx-auto leading-relaxed font-light">
            We believe every solopreneur deserves an elite workforce. Guild AI makes that possible with specialized agents, 
            built-in quality assurance, and a recursive learning engine that turns business identity into revenue.
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
              Guild AI was born from a simple observation: AI tools were getting powerful, but they weren't getting reliable. 
              Solopreneurs were promised "automation" but delivered chatbots that required constant supervision.
            </p>
            <p>
              We asked ourselves: What if AI could validate its own work? What if it could coordinate like a real marketing team? 
              These questions led to our three core innovations: the <strong>Judge Layer</strong>, the <strong>Source of Truth</strong>, 
              and the <strong>Agent Activity Theater</strong>.
            </p>
            <p>
              Today, Guild is one of the world's most comprehensive AI workforce ecosystems, powering the content-to-customer 
              flywheel for thousands of founders globally.
            </p>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="container mx-auto max-w-6xl mb-32">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold font-heading mb-4 tracking-tight">Core Values</h2>
          <p className="text-zinc-500">The principles that guide every line of code we write.</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {values.map((v, i) => (
            <div key={i} className="glass-panel p-8 rounded-2xl group hover:border-indigo-500/30 transition-all">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${v.color} flex items-center justify-center text-white mb-6 shadow-lg`}>
                {v.icon}
              </div>
              <h3 className="text-xl font-bold font-heading mb-3">{v.title}</h3>
              <p className="text-sm text-zinc-500 leading-relaxed font-light">{v.description}</p>
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
              <div className="w-20 h-20 rounded-full glass-panel flex items-center justify-center shrink-0 border border-white/10 shadow-glow-sm bg-zinc-900 font-heading font-black text-[10px] tracking-tighter text-indigo-400">
                {m.year}
              </div>
              <div className="glass-panel p-8 rounded-2xl flex-1 border border-white/10">
                <h4 className="text-xl font-bold font-heading mb-2">{m.title}</h4>
                <p className="text-zinc-500 leading-relaxed font-light">{m.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto max-w-4xl">
        <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow">
          <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Ready to build the future?</h2>
          <p className="text-zinc-500 mb-10 text-lg font-light">Join the thousands of founders automating their growth with Guild.</p>
          <Link to="/signup">
            <Button size="lg" className="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white rounded-full px-12 py-8 text-xl font-bold shadow-2xl shadow-indigo-500/20 border-t border-white/20">
              Get Started Now
            </Button>
          </Link>
        </div>
      </section>
    </div>
  )
}

export default AboutUsPage
