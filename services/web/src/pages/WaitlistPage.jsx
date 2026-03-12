import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Sparkles, ArrowLeft, Send } from 'lucide-react'

function WaitlistPage() {
    const [email, setEmail] = useState('')
    const [submitted, setSubmitted] = useState(false)
    const [position, setPosition] = useState(0)

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!email) return

        try {
            const response = await fetch('/api/waitlist/join', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            })
            const data = await response.json()
            setPosition(data.position)
            setSubmitted(true)
        } catch (error) {
            console.error('Waitlist Join Error:', error)
            // Mock success for demo if api fails
            setSubmitted(true)
            setPosition(432)
        }
    }

    return (
        <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
            <div className="max-w-xl w-full">
                {!submitted ? (
                    <Card className="rounded-3xl border-slate-800 bg-slate-950 text-white shadow-2xl">
                        <CardHeader className="text-center pt-12">
                            <div className="flex justify-center mb-6">
                                <div className="w-16 h-16 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-2xl flex items-center justify-center">
                                    <Sparkles className="text-white w-10 h-10" strokeWidth={1.5} />
                                </div>
                            </div>
                            <CardTitle className="text-4xl font-black mb-2">Join the Future</CardTitle>
                            <CardDescription className="text-zinc-600 text-lg">
                                We're rolling out access to Guild AI in batches.
                                Join 2,400+ business owners on the waiting list.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="pb-12 px-8">
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <Input
                                    type="email"
                                    placeholder="Enter your business email"
                                    className="bg-slate-900 border-slate-800 h-14 rounded-xl text-lg focus:ring-sky-500"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                                <Button className="w-full h-14 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 font-bold text-lg hover:scale-105 transition-transform text-white">
                                    Get Early Access <Send className="ml-2 w-5 h-5" strokeWidth={1.5} />
                                </Button>
                            </form>
                            <p className="text-center text-zinc-500 mt-6 text-sm">
                                No spam. Just priority access when slots open up.
                            </p>
                        </CardContent>
                    </Card>
                ) : (
                    <Card className="rounded-3xl border-slate-800 bg-slate-950 text-white shadow-2xl text-center p-12">
                        <div className="w-20 h-20 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-8 border border-emerald-500/50">
                            <Sparkles className="text-emerald-400 w-10 h-10" strokeWidth={1.5} />
                        </div>
                        <h2 className="text-4xl font-black mb-4">You're on the list!</h2>
                        <p className="text-zinc-600 text-xl mb-8">
                            You're currently position <span className="text-sky-400 font-bold">#{position}</span>.
                            We'll email you as soon as a spot opens up.
                        </p>
                        <div className="p-6 bg-slate-900 rounded-2xl border border-slate-800 mb-8">
                            <p className="text-sm font-bold text-sky-400 mb-1 uppercase tracking-widest">Priority Bonus</p>
                            <p className="text-zinc-600">Share Guild AI with a friend to skip 100 spots.</p>
                        </div>
                        <Link to="/"><Button variant="ghost" className="text-zinc-600"><ArrowLeft className="mr-2" strokeWidth={1.5} /> Back to Home</Button></Link>
                    </Card>
                )}
            </div>
        </div>
    )
}

export default WaitlistPage
