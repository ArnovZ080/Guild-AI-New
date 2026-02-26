import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { ArrowLeft } from 'lucide-react'

function TermsPage() {
    return (
        <div className="min-h-screen bg-slate-50 pt-24">
            <div className="container mx-auto px-4 max-w-4xl bg-white p-12 rounded-3xl shadow-sm border border-slate-100 mb-24">
                <Link to="/"><Button variant="ghost" className="mb-8"><ArrowLeft className="w-4 h-4 mr-2" /> Back to Home</Button></Link>
                <h1 className="text-4xl font-black mb-4">Terms & Conditions</h1>
                <p className="text-slate-500 mb-12">Last updated: February 2026</p>

                <section className="prose prose-slate max-w-none space-y-8 text-slate-700 font-medium">
                    <div>
                        <h2 className="text-2xl font-bold mb-4 text-slate-900">1. Acceptance of Terms</h2>
                        <p>By using Guild AI, you agree to these terms. Our software provides AI-driven business assistance; results depend on your input and market conditions.</p>
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold mb-4 text-slate-900">2. Use License</h2>
                        <p>Permission is granted to use Guild AI for your business operations. This is a license, not a transfer of title.</p>
                    </div>
                </section>
            </div>
        </div>
    )
}

export default TermsPage
