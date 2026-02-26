import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Sparkles, ArrowRight, ShieldCheck } from 'lucide-react'

function SignupPage() {
    const [params] = useSearchParams()
    const selectedPlan = params.get('plan') || 'free'
    const navigate = useNavigate()

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        businessName: ''
    })

    const handleSubmit = (e) => {
        e.preventDefault()
        // Mock signup success
        console.log('Signing up with:', formData, 'Plan:', selectedPlan)
        navigate('/onboarding')
    }

    return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
            <div className="max-w-4xl w-full grid md:grid-cols-2 bg-white rounded-3xl shadow-2xl overflow-hidden border border-slate-100">
                <div className="p-12 bg-slate-900 text-white flex flex-col justify-between">
                    <div>
                        <div className="flex items-center gap-2 mb-12">
                            <div className="w-10 h-10 bg-sky-500 rounded-lg flex items-center justify-center font-bold text-xl">E</div>
                            <span className="text-2xl font-bold">Guild AI</span>
                        </div>
                        <h2 className="text-4xl font-extrabold mb-6 leading-tight">Start Building Your AI Workforce.</h2>
                        <div className="space-y-6">
                            <div className="flex items-start gap-4">
                                <div className="bg-sky-500/20 p-2 rounded-lg"><Sparkles className="text-sky-400" /></div>
                                <div>
                                    <p className="font-bold">115+ Agents Included</p>
                                    <p className="text-slate-400 text-sm">Full access to the entire executive suite.</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-4">
                                <div className="bg-emerald-500/20 p-2 rounded-lg"><ShieldCheck className="text-emerald-400" /></div>
                                <div>
                                    <p className="font-bold">Judge Layer Protection</p>
                                    <p className="text-slate-400 text-sm">Professional quality guaranteed natively.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="pt-12 border-t border-slate-800 mt-12">
                        <p className="text-slate-400 italic">"The only platform that doesn't just give you tools, but a team that works for you."</p>
                    </div>
                </div>

                <div className="p-12">
                    <div className="mb-8">
                        <h1 className="text-3xl font-bold mb-2">Create Account</h1>
                        <p className="text-slate-500">You've selected the <span className="text-sky-600 font-bold uppercase">{selectedPlan}</span> plan.</p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="text-sm font-bold text-slate-700 block mb-1">Full Name</label>
                            <Input
                                className="h-12 rounded-xl"
                                placeholder="John Doe"
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                required
                            />
                        </div>
                        <div>
                            <label className="text-sm font-bold text-slate-700 block mb-1">Business Email</label>
                            <Input
                                type="email"
                                className="h-12 rounded-xl"
                                placeholder="john@company.com"
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                required
                            />
                        </div>
                        <div>
                            <label className="text-sm font-bold text-slate-700 block mb-1">Company Name</label>
                            <Input
                                className="h-12 rounded-xl"
                                placeholder="Acme Corp"
                                onChange={(e) => setFormData({ ...formData, businessName: e.target.value })}
                                required
                            />
                        </div>
                        <div>
                            <label className="text-sm font-bold text-slate-700 block mb-1">Password</label>
                            <Input
                                type="password"
                                className="h-12 rounded-xl"
                                placeholder="••••••••"
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                required
                            />
                        </div>

                        <Button className="w-full h-12 bg-slate-900 rounded-xl font-bold mt-4">
                            Create My Account <ArrowRight className="ml-2 w-4 h-4" />
                        </Button>
                    </form>

                    <p className="text-center text-sm text-slate-500 mt-8">
                        Already have an account? <Link to="/login" className="text-sky-600 font-bold">Login</Link>
                    </p>
                </div>
            </div>
        </div>
    )
}

export default SignupPage
