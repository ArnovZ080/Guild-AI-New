import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { ArrowRight, Lock, Mail } from 'lucide-react'

function LoginPage() {
    const navigate = useNavigate()
    const [formData, setFormData] = useState({ email: '', password: '' })

    const handleSubmit = (e) => {
        e.preventDefault()
        // Mock login success
        console.log('Logging in with:', formData)
        navigate('/')
    }

    return (
        <div className="min-h-screen bg-white/[0.03] flex items-center justify-center p-4 font-sans">
            <div className="max-w-md w-full">
                <div className="text-center mb-10">
                    <div className="w-12 h-12 bg-slate-900 rounded-xl flex items-center justify-center font-bold text-white text-2xl mx-auto mb-4 shadow-xl">E</div>
                    <h1 className="text-3xl font-black text-slate-900">Welcome Back</h1>
                    <p className="text-zinc-500 mt-2">Log in to manage your AI executive team.</p>
                </div>

                <Card className="rounded-3xl border-slate-100 shadow-2xl overflow-hidden">
                    <CardHeader className="bg-white/[0.03] border-b border-slate-100 pb-8">
                        <CardTitle className="text-xl">Login</CardTitle>
                        <CardDescription>Enter your credentials to access the suite.</CardDescription>
                    </CardHeader>
                    <CardContent className="pt-8">
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="relative">
                                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600 w-5 h-5" strokeWidth={1.5} />
                                <Input
                                    type="email"
                                    placeholder="Email Address"
                                    className="pl-12 h-12 rounded-xl bg-white/[0.03] border-slate-100 focus:bg-white transition-all shadow-inner"
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="relative">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600 w-5 h-5" strokeWidth={1.5} />
                                <Input
                                    type="password"
                                    placeholder="Password"
                                    className="pl-12 h-12 rounded-xl bg-white/[0.03] border-slate-100 focus:bg-white transition-all shadow-inner"
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    required
                                />
                            </div>
                            <Button className="w-full h-12 bg-slate-900 rounded-xl font-bold shadow-lg hover:shadow-indigo-500/20 transition-all flex items-center justify-center gap-2">
                                Log In <ArrowRight className="w-4 h-4" strokeWidth={1.5} />
                            </Button>
                        </form>

                        <div className="mt-8 text-center text-sm">
                            <span className="text-zinc-500">Don't have an account? </span>
                            <Link to="/signup" className="text-sky-600 font-bold hover:underline">Get Started</Link>
                        </div>
                    </CardContent>
                </Card>

                <p className="text-center text-xs text-zinc-600 mt-12">
                    © 2026 Guild AI. Secure, autonomous business intelligence.
                </p>
            </div>
        </div>
    )
}

export default LoginPage
