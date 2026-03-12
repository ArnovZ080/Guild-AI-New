import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { ArrowLeft } from 'lucide-react'

function RefundPolicyPage() {
    return (
        <div className="min-h-screen bg-white/[0.03] pt-24">
            <div className="container mx-auto px-4 max-w-4xl bg-white p-12 rounded-3xl shadow-sm border border-slate-100 mb-24">
                <Link to="/"><Button variant="ghost" className="mb-8"><ArrowLeft className="w-4 h-4 mr-2" strokeWidth={1.5} /> Back to Home</Button></Link>
                <h1 className="text-4xl font-black mb-4">Refund Policy</h1>
                <p className="text-zinc-500 mb-12">Last updated: February 2026</p>

                <section className="prose prose-slate max-w-none space-y-8 text-zinc-400 font-medium">
                    <div>
                        <h2 className="text-2xl font-bold mb-4 text-slate-900">1. Satisfaction Guarantee</h2>
                        <p>We want you to be thrilled with your AI executive team. If you're not satisfied within the first 14 days of your first paid month, we offer a full refund.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold mb-4 text-slate-900">2. Trial Period</h2>
                        <p>Our 21-day free trial allows you to explore all premium features risk-free. No charges are made during the trial period.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold mb-4 text-slate-900">3. Cancellation</h2>
                        <p>You can cancel your subscription at any time through the settings panel. Access will continue until the end of your current billing period.</p>
                    </div>
                </section>
            </div>
        </div>
    )
}

export default RefundPolicyPage
