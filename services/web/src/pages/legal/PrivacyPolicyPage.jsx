import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Sparkles, ArrowLeft } from 'lucide-react'

function PrivacyPolicyPage() {
    return (
        <div className="min-h-screen bg-white/[0.03] pt-24">
            <div className="container mx-auto px-4 max-w-4xl bg-white p-12 rounded-3xl shadow-sm border border-slate-100 mb-24">
                <Link to="/"><Button variant="ghost" className="mb-8"><ArrowLeft className="w-4 h-4 mr-2" strokeWidth={1.5} /> Back to Home</Button></Link>
                <h1 className="text-4xl font-black mb-4">Privacy Policy</h1>
                <p className="text-zinc-500 mb-12">Last updated: February 2026</p>

                <section className="prose prose-slate max-w-none space-y-8 text-zinc-400 font-medium">
                    <div>
                        <h2 className="text-2xl font-bold mb-4 text-slate-900">1. Information We Collect</h2>
                        <p>We collect information you provide directly to us (name, email, business niche) and technical data (IP, browser type) to provide and improve our AI services.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold mb-4 text-slate-900">2. How We Use Your Information</h2>
                        <p>We use your data to power your AI executive team, process payments, and send platform updates. We never sell your personal data to third parties.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold mb-4 text-slate-900">3. Data Security</h2>
                        <p>We use industry-standard encryption and protocols to safeguard your business intelligence. Your data is your property.</p>
                    </div>
                </section>
            </div>
        </div>
    )
}

export default PrivacyPolicyPage
