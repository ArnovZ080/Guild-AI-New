import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { 
  ArrowLeft, DollarSign, TrendingUp, Users,
  Gift, Target, BarChart3, Zap, CheckCircle2, Award,
  Rocket, Globe, MessageSquare, Sparkles
} from 'lucide-react'
import { motion } from 'framer-motion'
import guildLogo from '@/assets/guild-logo.png'
import ZARPrice from '@/components/ui/ZARPrice'

function AffiliatesPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    website: '',
    audience: '',
    message: ''
  })

  const [isSubmitting, setIsSubmitting] = useState(false)

  const benefits = [
    {
      icon: <DollarSign className="w-6 h-6" />,
      title: '30% Recurring Commission',
      description: 'Earn 30% of every payment from customers you refer, for the entire life of their subscription. Not a one-time bounty - recurring revenue.',
      color: 'from-emerald-500 to-teal-500'
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'A Story That Converts',
      description: 'Guild closes the full loop from content to customers - a clear, specific promise that\'s easy to explain and easy to believe.',
      color: 'from-blue-500 to-indigo-500'
    },
    {
      icon: <Rocket className="w-6 h-6" />,
      title: 'Something Worth Promoting',
      description: 'Refer your audience to a platform that actually delivers results - not another AI writing tool that stops at content creation.',
      color: 'from-purple-500 to-violet-500'
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: 'Direct Partner Support',
      description: 'Marketing assets, a real-time affiliate dashboard, and direct access to Arno for any questions. Not a ticketing system.',
      color: 'from-pink-500 to-rose-500'
    }
  ]

  const commissionTiers = [
    {
      plan: 'Starter',
      price: '$39/mo',
      regularPrice: '$49/mo',
      commission: '$11.70/mo',
      annual: '$140.40/yr',
      usd: 39,
      commissionUsd: 11.70
    },
    {
      plan: 'Growth',
      price: '$119/mo',
      regularPrice: '$149/mo',
      commission: '$35.70/mo',
      annual: '$428.40/yr',
      popular: true,
      usd: 119,
      commissionUsd: 35.70
    },
    {
      plan: 'Scale',
      price: '$239/mo',
      regularPrice: '$299/mo',
      commission: '$71.70/mo',
      annual: '$860.40/yr',
      usd: 239,
      commissionUsd: 71.70
    }
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    await new Promise(resolve => setTimeout(resolve, 1500))
    alert('Application submitted! Arno will review your profile and be in touch.')
    setIsSubmitting(false)
  }

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

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
        <section className="text-center mb-24">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className="w-16 h-16 rounded-2xl glass-panel border border-white/10 flex items-center justify-center mx-auto mb-8 shadow-glow-sm">
                    <Rocket className="text-indigo-400" />
                </div>
                <h1 className="text-5xl md:text-7xl font-bold font-heading tracking-tight mb-8">
                    Earn While You <span className="text-gradient-cobalt">Refer</span>
                </h1>
                <p className="text-xl text-zinc-400 max-w-3xl mx-auto font-light leading-relaxed">
                    Introduce small business owners to a platform that closes the full loop from content to customers - and earn <strong>30% recurring commission</strong> for every month they stay.
                </p>
            </motion.div>
        </section>

        {/* Benefits */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-24">
            {benefits.map((b, i) => (
                <div key={i} className="glass-panel p-8 rounded-2xl group transition-all">
                    <div className={`w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-400/40 shadow-glow-sm flex items-center justify-center text-indigo-400 mb-6 shadow-glow-sm group-hover:scale-110 transition-transform`}>
                        {b.icon}
                    </div>
                    <h3 className="text-xl font-bold font-heading mb-3">{b.title}</h3>
                    <p className="text-sm text-zinc-400 leading-relaxed font-light">{b.description}</p>
                </div>
            ))}
        </div>

        {/* Commission Tiers */}
        <section className="mb-24">
            <div className="text-center mb-16">
                <h2 className="text-4xl font-bold font-heading tracking-tight mb-4">What You Earn</h2>
                <p className="text-zinc-400">Recurring monthly commissions based on the plan your referral subscribes to. Founding member rates shown.</p>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
                {commissionTiers.map((t, i) => (
                    <div key={i} className={`glass-panel p-10 rounded-3xl relative overflow-hidden ${t.popular ? 'border-indigo-500/30 ring-1 ring-indigo-500/20' : 'border-white/10'}`}>
                        {t.popular && <div className="absolute top-0 right-0 py-1 px-4 bg-indigo-500 text-xs font-black tracking-widest uppercase">Highest Volume</div>}
                        <h4 className="text-zinc-400 font-heading text-sm mb-1 uppercase tracking-widest">{t.plan} Referrals</h4>
                        <p className="text-zinc-600 text-xs mb-1">Subscriber pays {t.price} <span className="line-through">{t.regularPrice}</span></p>
                        <ZARPrice usd={t.usd} className="mb-4 text-zinc-300 text-xs" />
                        <div className="text-4xl font-black mb-1 text-emerald-400">{t.commission} <span className="text-zinc-700 text-lg font-normal"> /mo</span></div>
                        <ZARPrice usd={t.commissionUsd} className="mb-8 text-emerald-300 text-sm" />
                        <div className="space-y-4 pt-6 border-t border-white/5">
                            <div className="flex justify-between text-sm">
                                <span className="text-zinc-600">Annual per referral</span>
                                <span className="font-bold text-emerald-400">{t.annual}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <p className="text-center text-zinc-600 text-xs mt-6">Commission calculated on founding member rates (valid until public launch August 2026). Post-launch commissions calculated on standard pricing. Payouts bi-weekly via PayPal or bank transfer.</p>
        </section>

        {/* Form */}
        <div className="grid lg:grid-cols-2 gap-20 items-center">
            <div className="space-y-8">
                <h2 className="text-4xl font-bold font-heading tracking-tight">Apply to the <br /> <span className="text-indigo-400">Partner Program</span></h2>
                <p className="text-zinc-400 font-light text-lg">
                    We're selective. We're looking for partners who speak directly to small business owners and genuinely understand the problem Guild solves.
                </p>
                <div className="space-y-4">
                    <div className="flex gap-4 items-center">
                        <CheckCircle2 className="text-emerald-500 shrink-0" size={20} />
                        <span className="text-sm text-zinc-300">Ready-made marketing assets and copy</span>
                    </div>
                    <div className="flex gap-4 items-center">
                        <CheckCircle2 className="text-emerald-500 shrink-0" size={20} />
                        <span className="text-sm text-zinc-300">Bi-weekly commission payouts</span>
                    </div>
                    <div className="flex gap-4 items-center">
                        <CheckCircle2 className="text-emerald-500 shrink-0" size={20} />
                        <span className="text-sm text-zinc-300">Real-time tracking dashboard</span>
                    </div>
                    <div className="flex gap-4 items-center">
                        <CheckCircle2 className="text-emerald-500 shrink-0" size={20} />
                        <span className="text-sm text-zinc-300">Direct line to Arno for partner questions</span>
                    </div>
                </div>
            </div>

            <motion.div 
                initial={{ opacity: 0, scale: 0.98 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                className="glass-panel p-10 rounded-3xl"
            >
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <Label className="text-zinc-400">Full Name</Label>
                        <Input name="name" value={formData.name} onChange={handleInputChange} required className="bg-white/5 border-white/10 rounded-xl" />
                    </div>
                    <div className="space-y-2">
                        <Label className="text-zinc-400">Email Address</Label>
                        <Input type="email" name="email" value={formData.email} onChange={handleInputChange} required className="bg-white/5 border-white/10 rounded-xl" />
                    </div>
                    <div className="space-y-2">
                        <Label className="text-zinc-400">Primary Channel (Website / Social / Newsletter)</Label>
                        <Input name="website" value={formData.website} onChange={handleInputChange} required className="bg-white/5 border-white/10 rounded-xl" />
                    </div>
                    <div className="space-y-2">
                        <Label className="text-zinc-400">Tell us about your audience</Label>
                        <Textarea name="audience" value={formData.audience} onChange={handleInputChange} required className="bg-white/5 border-white/10 rounded-xl" rows={3} placeholder="Who follows you, what industry, approximate size..." />
                    </div>
                    <Button type="submit" disabled={isSubmitting} className="w-full bg-white text-black hover:bg-zinc-200 rounded-xl py-6 font-bold text-lg transition-all active:scale-95">
                        {isSubmitting ? 'Submitting...' : 'Submit Partnership Application'}
                    </Button>
                    <p className="text-xs text-center text-zinc-600 uppercase tracking-widest pt-2">Reviewed personally by Arno. Usually within 48 hours.</p>
                </form>
            </motion.div>
        </div>
      </div>
    </div>
  )
}

export default AffiliatesPage
