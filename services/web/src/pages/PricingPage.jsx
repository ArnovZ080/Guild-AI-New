import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Check, ArrowRight, Sparkles, Zap, Shield, TrendingUp } from 'lucide-react'

function PricingPage() {
    const [billingCycle, setBillingCycle] = useState('monthly');

    const plans = [
        {
            name: 'Starter',
            price: billingCycle === 'monthly' ? '$49' : '$39',
            period: '/month',
            description: 'Perfect for individuals and small startups.',
            features: ['5 AI Agents', '500 credits', 'Judge Layer QA', 'Core Integrations'],
            buttonText: 'Get Started',
            popular: false
        },
        {
            name: 'Growth',
            price: billingCycle === 'monthly' ? '$99' : '$79',
            period: '/month',
            description: 'For growing businesses needing more automation.',
            features: ['10 AI Agents', '1,000 credits', '36 Integrations', 'Meta KPI Tracking'],
            buttonText: 'Go Growth',
            popular: true
        },
        {
            name: 'Professional',
            price: billingCycle === 'monthly' ? '$199' : '$159',
            period: '/month',
            description: 'For power users and medium organizations.',
            features: ['25 AI Agents', '2,500 credits', 'Custom Workflows', 'Priority Support'],
            buttonText: 'Go Pro',
            popular: false
        }
    ]

    return (
        <div className="min-h-screen bg-white/[0.03] py-24">
            <div className="container mx-auto px-4 max-w-7xl">
                <div className="text-center mb-16">
                    <h1 className="text-5xl font-extrabold mb-6 tracking-tight text-slate-900">Simple, Transparent Pricing</h1>
                    <p className="text-xl text-zinc-500 mb-10 max-w-2xl mx-auto">Choose the plan that fits your business scale. No hidden fees. No complex contracts.</p>

                    <div className="flex items-center justify-center gap-4 bg-white p-2 rounded-2xl border border-slate-200 w-fit mx-auto shadow-sm">
                        <button
                            className={`px-6 py-2 rounded-xl text-sm font-bold transition-all ${billingCycle === 'monthly' ? 'glass-panel text-zinc-100 shadow-lg' : 'text-zinc-500'}`}
                            onClick={() => setBillingCycle('monthly')}
                        >
                            Monthly
                        </button>
                        <button
                            className={`px-6 py-2 rounded-xl text-sm font-bold transition-all ${billingCycle === 'yearly' ? 'glass-panel text-zinc-100 shadow-lg' : 'text-zinc-500'}`}
                            onClick={() => setBillingCycle('yearly')}
                        >
                            Yearly (Save 20%)
                        </button>
                    </div>
                </div>

                <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {plans.map((p, i) => (
                        <Card key={i} className={`relative rounded-3xl border-2 transition-all ${p.popular ? 'border-sky-500 shadow-2xl scale-105' : 'border-slate-100'}`}>
                            {p.popular && (
                                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-sky-500 text-white px-4 py-1 rounded-full text-xs font-bold shadow-lg">
                                    MOST POPULAR
                                </div>
                            )}
                            <CardHeader>
                                <CardTitle className="text-2xl font-bold">{p.name}</CardTitle>
                                <CardDescription>{p.description}</CardDescription>
                                <div className="mt-6">
                                    <span className="text-5xl font-black">{p.price}</span>
                                    <span className="text-zinc-500 font-medium">{p.period}</span>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <Button className={`w-full py-6 rounded-2xl mb-8 font-bold ${p.popular ? 'bg-sky-600' : 'bg-slate-900'}`}>{p.buttonText}</Button>
                                <ul className="space-y-4">
                                    {p.features.map((f, fi) => (
                                        <li key={fi} className="flex items-center text-sm font-medium text-zinc-400">
                                            <div className="bg-emerald-100 p-1 rounded-full mr-3">
                                                <Check className="w-3 h-3 text-emerald-600" strokeWidth={1.5} />
                                            </div>
                                            {f}
                                        </li>
                                    ))}
                                </ul>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default PricingPage
