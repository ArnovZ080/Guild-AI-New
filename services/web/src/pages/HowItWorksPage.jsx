import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { 
  Sparkles, ArrowLeft, Users, TrendingUp, DollarSign,
  FileText, Briefcase, Shield, Brain, Zap, Globe, Target, Layers,
  Rocket, MessageSquare, CheckCircle2, Clock
} from 'lucide-react'
import { motion } from 'framer-motion'

function HowItWorksPage() {
  const steps = [
    {
        step: '01',
        title: 'You tell Guild about your business',
        description: 'A friendly conversation - not a form. Guild asks about what you do, who your customers are, what your brand sounds like, and what your goals are. Takes about 10 minutes. You can come back and add more anytime.',
        detail: 'Upload your product catalog, brand guidelines, or any business documents. Guild reads them and gets smarter about your business instantly.'
    },
    {
        step: '02',
        title: 'Guild creates a week of content',
        description: 'Blog posts, social media updates, Instagram reels, email newsletters, ad creatives - all in your brand voice, targeted at your ideal customer. Different formats and messages for each platform.',
        detail: 'Every piece is checked for brand consistency, accuracy, and quality before you see it.'
    },
    {
        step: '03',
        title: 'You review and approve',
        description: 'Scroll through your content queue. Approve with one tap, edit anything you want to tweak, or ask Guild to regenerate a piece with feedback. You are always in control.',
        detail: 'Most users spend 5-10 minutes reviewing a full week of content.'
    },
    {
        step: '04',
        title: 'Content publishes automatically',
        description: 'Approved content goes live on the right platform, at the right time, without you lifting a finger. Guild learns when your audience is most active and adjusts the schedule.',
        detail: 'Instagram at 6pm, LinkedIn at 12pm, email at 8am - Guild figures out the best times for your specific audience.'
    },
    {
        step: '05',
        title: 'Leads come to you',
        description: 'When someone comments, likes, clicks, or subscribes because of your content, Guild captures them. Each person is scored on how closely they match your ideal customer profile.',
        detail: 'High-scoring leads are flagged for immediate attention. You get notified when a great prospect engages.'
    },
    {
        step: '06',
        title: 'Guild follows up for you',
        description: 'Personalised email sequences go out automatically - welcoming new subscribers, sharing helpful content, building trust, and making the offer when the timing is right.',
        detail: 'Every message is on-brand and approved by you. Guild handles the follow-up. You close the deal.'
    }
  ]

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
                    <Clock size={14} /> From signup to first customers
                </div>
                <h1 className="text-5xl md:text-8xl font-bold font-heading tracking-tight mb-8">
                    Here's How <span className="text-gradient-cobalt">Guild Works</span>
                </h1>
                <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
                    You sign up, tell Guild about your business, and it handles your marketing from there. 
                    Here's what happens behind the scenes.
                </p>
            </motion.div>
        </section>

        {/* Step-by-Step Journey */}
        <section className="mb-32">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {steps.map((s, i) => (
                    <motion.div 
                        key={i} 
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1 }}
                        viewport={{ once: true }}
                        className="glass-panel p-8 rounded-3xl group border-white/10 hover:border-indigo-500/30 transition-all flex flex-col"
                    >
                        <div className="flex justify-between items-start mb-6">
                            <span className="text-5xl font-black text-indigo-500/10 group-hover:text-indigo-500/20 transition-colors uppercase font-heading">{s.step}</span>
                            <div className="p-3 rounded-2xl bg-indigo-500/5 text-indigo-400">
                                {i === 0 && <Brain size={24} />}
                                {i === 1 && <Sparkles size={24} />}
                                {i === 2 && <CheckCircle2 size={24} />}
                                {i === 3 && <Globe size={24} />}
                                {i === 4 && <Target size={24} />}
                                {i === 5 && <Users size={24} />}
                            </div>
                        </div>
                        <h3 className="text-2xl font-bold font-heading mb-4 leading-tight">{s.title}</h3>
                        <p className="text-base text-zinc-400 mb-6 font-light leading-relaxed flex-grow">{s.description}</p>
                        <div className="pt-6 border-t border-white/5">
                            <p className="text-xs uppercase tracking-widest font-black text-indigo-400/50 mb-2">Deep Capability</p>
                            <p className="text-xs text-zinc-600 font-medium leading-relaxed italic">{s.detail}</p>
                        </div>
                    </motion.div>
                ))}
            </div>
        </section>

        {/* Future Signal */}
        <section className="mb-32 text-center">
            <p className="text-zinc-600 text-sm font-medium tracking-widest uppercase">
                More capabilities coming soon. We're just getting started.
            </p>
        </section>

        {/* CTA */}
        <section className="container mx-auto max-w-4xl">
            <div className="glass-panel p-16 rounded-3xl text-center border border-indigo-500/20 shadow-glow relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500/20 to-transparent" />
                <h2 className="text-4xl font-bold font-heading mb-6 tracking-tight">Let Guild Handle Your Marketing</h2>
                <p className="text-zinc-400 mb-10 text-lg font-light">From content to customers - in one system that gets smarter every week.</p>
                <Link to="/signup">
                    <Button size="lg" className="bg-white text-black hover:bg-zinc-200 rounded-full px-12 py-8 text-xl font-bold transition-all hover:scale-105 active:scale-95 shadow-2xl">
                        Start Your Free Trial
                    </Button>
                </Link>
            </div>
        </section>
      </div>
    </div>
  )
}

export default HowItWorksPage
