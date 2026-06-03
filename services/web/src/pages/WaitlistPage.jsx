import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import { Input } from '@/components/ui/input'
import { ShinyButton } from '@/components/ui/shiny-button'
import { Lock, ArrowLeft, CheckCircle2, Flame } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useWaitlistStatus } from '@/hooks/useWaitlistStatus'
import { fadeUp, scaleIn, staggerContainer, springTransition } from '@/lib/transitions'

// ── Ember burst canvas overlay shown on successful submit ────────────────
function EmberBurst({ onDone }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const cx = canvas.width / 2
    const cy = canvas.height / 2
    const COLORS = ['245,158,11', '99,102,241', '139,92,246', '251,191,36', '165,180,252']

    const particles = Array.from({ length: 120 }, () => {
      const angle = Math.random() * Math.PI * 2
      const speed = Math.random() * 8 + 3
      return {
        x: cx, y: cy,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - Math.random() * 4,
        r: Math.random() * 3 + 1,
        col: COLORS[Math.floor(Math.random() * COLORS.length)],
        life: 1,
        decay: Math.random() * 0.018 + 0.01,
      }
    })

    let frame
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      let alive = 0
      particles.forEach(p => {
        if (p.life <= 0) return
        alive++
        p.x += p.vx
        p.y += p.vy
        p.vy += 0.15 // gravity
        p.vx *= 0.98
        p.life -= p.decay

        const a = Math.max(0, p.life)
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 3)
        g.addColorStop(0, `rgba(${p.col},${a * 0.6})`)
        g.addColorStop(1, `rgba(${p.col},0)`)
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r * 3, 0, Math.PI * 2)
        ctx.fillStyle = g
        ctx.fill()

        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(${p.col},${Math.min(a * 1.5, 1)})`
        ctx.shadowColor = `rgba(${p.col},0.9)`
        ctx.shadowBlur = 6
        ctx.fill()
        ctx.shadowBlur = 0
      })

      if (alive > 0) {
        frame = requestAnimationFrame(draw)
      } else {
        onDone?.()
      }
    }

    frame = requestAnimationFrame(draw)
    return () => cancelAnimationFrame(frame)
  }, [onDone])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none"
      style={{ zIndex: 100 }}
    />
  )
}

// ── Spots progress bar ────────────────────────────────────────────────────
function SpotsBar({ claimed, total }) {
  const pct = Math.min((claimed / total) * 100, 100)
  const critical = claimed >= total - 10
  const almostGone = claimed >= total - 5

  return (
    <div className="w-full max-w-sm mx-auto mb-8">
      <div className="flex justify-between items-center mb-2">
        <span className={`text-xs font-bold uppercase tracking-widest ${critical ? 'text-amber-400' : 'text-indigo-400'}`}>
          {almostGone ? '🔥 Almost gone' : `${total - claimed} spots remaining`}
        </span>
        <span className="text-xs text-zinc-600 font-mono">{claimed}/{total}</span>
      </div>
      <div className="h-1.5 rounded-full bg-white/8 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
          className="h-full rounded-full relative"
          style={{
            background: critical
              ? 'linear-gradient(90deg, #f59e0b, #ef4444)'
              : 'linear-gradient(90deg, #5E6AD2, #818CF8)',
          }}
        >
          {critical && (
            <motion.div
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{ repeat: Infinity, duration: 1.5 }}
              className="absolute inset-0 rounded-full"
              style={{ background: 'inherit', filter: 'blur(4px)' }}
            />
          )}
        </motion.div>
      </div>
    </div>
  )
}

// ── Page ──────────────────────────────────────────────────────────────────
function WaitlistPage() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [showBurst, setShowBurst] = useState(false)
  const [focused, setFocused] = useState(false)
  const { spotsClaimed, totalSpots, loading: statusLoading } = useWaitlistStatus()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email) return
    setSubmitting(true)
    try {
      await fetch('/api/waitlist/join', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })
    } catch (_) {}
    setSubmitting(false)
    setShowBurst(true)
    // submitted state set after burst finishes
  }

  return (
    <div className="min-h-screen bg-transparent flex items-center justify-center p-6 relative">

      {/* Ember burst overlay */}
      {showBurst && (
        <EmberBurst onDone={() => { setShowBurst(false); setSubmitted(true) }} />
      )}

      <div className="max-w-2xl w-full">
        <Link to="/landing">
          <button className="text-zinc-500 hover:text-white mb-12 flex items-center gap-2 text-sm transition-colors group">
            <ArrowLeft size={14} className="group-hover:-translate-x-1 transition-transform" />
            Back to Landing
          </button>
        </Link>

        <AnimatePresence mode="wait">
          {!submitted ? (
            <motion.div
              key="form"
              variants={staggerContainer}
              initial="hidden"
              animate="visible"
            >
              <motion.div
                variants={scaleIn}
                className="glass-panel p-12 md:p-16 rounded-3xl border border-white/10 relative overflow-hidden text-center"
              >
                <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-indigo-500/60 to-transparent" />

                {/* Icon */}
                <motion.div variants={fadeUp} className="flex justify-center mb-8">
                  <div className="w-20 h-20 bg-indigo-500/10 border border-indigo-400/40 rounded-3xl flex items-center justify-center">
                    <Lock className="text-indigo-400 w-10 h-10" strokeWidth={1.5} />
                  </div>
                </motion.div>

                {/* Headline */}
                <motion.h1 variants={fadeUp} className="text-4xl md:text-6xl font-bold tracking-tight mb-4">
                  Lock In Your <span className="text-gradient-cobalt">Founding Rate.</span>
                </motion.h1>

                {/* Spots bar */}
                <motion.div variants={fadeUp}>
                  {!statusLoading && (
                    <SpotsBar claimed={spotsClaimed ?? 12} total={totalSpots ?? 50} />
                  )}
                </motion.div>

                <motion.p variants={fadeUp} className="text-zinc-500 text-base mb-10 font-light leading-relaxed max-w-md mx-auto">
                  Founding members get Guild's Growth rate permanently locked in before public launch raises the price. Beta opens July 2026.
                </motion.p>

                {/* What you're locking in */}
                <motion.div
                  variants={fadeUp}
                  className="mb-10 p-6 rounded-2xl border border-white/6 bg-white/2 text-left space-y-3 max-w-sm mx-auto"
                >
                  <p className="label-eyebrow text-indigo-400/70 mb-4 text-center">What you're locking in</p>
                  {[
                    '$119/mo Growth rate — never increases',
                    'Content created, leads captured, nurtured automatically',
                    'Direct setup call before you go live',
                    'Priority access when beta opens',
                  ].map((item, i) => (
                    <div key={i} className="flex items-center gap-3 text-sm text-zinc-400">
                      <div className="w-4 h-4 rounded-full bg-indigo-500/15 border border-indigo-400/30 flex items-center justify-center shrink-0">
                        <div className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                      </div>
                      {item}
                    </div>
                  ))}
                </motion.div>

                {/* Form */}
                <motion.form variants={fadeUp} onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
                  <div className="relative">
                    <Input
                      type="email"
                      placeholder="Enter your business email"
                      className="h-14 rounded-2xl text-base px-6 transition-all duration-300"
                      style={{
                        background: 'rgba(255,255,255,0.05)',
                        border: focused ? '1px solid rgba(94,106,210,0.6)' : '1px solid rgba(255,255,255,0.08)',
                        boxShadow: focused ? '0 0 0 3px rgba(94,106,210,0.12), 0 0 20px rgba(94,106,210,0.1)' : 'none',
                        outline: 'none',
                      }}
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      onFocus={() => setFocused(true)}
                      onBlur={() => setFocused(false)}
                      required
                      disabled={submitting}
                    />
                  </div>
                  <ShinyButton type="submit" className="w-full text-base py-3.5" onClick={() => {}}>
                    {submitting ? 'Securing Your Spot…' : 'Lock In My Founding Rate'}
                  </ShinyButton>
                </motion.form>

                <motion.p variants={fadeUp} className="mt-6 text-zinc-700 text-xs">
                  No credit card required. We'll email you one week before your cohort opens.
                </motion.p>
              </motion.div>
            </motion.div>
          ) : (
            <motion.div
              key="success"
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={springTransition}
              className="glass-panel p-12 md:p-20 rounded-3xl border border-emerald-500/20 text-center relative overflow-hidden"
            >
              <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-emerald-500/50 to-transparent" />

              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 300, damping: 20, delay: 0.1 }}
                className="w-24 h-24 bg-emerald-500/10 border border-emerald-500/40 rounded-full flex items-center justify-center mx-auto mb-8"
              >
                <CheckCircle2 className="text-emerald-400 w-12 h-12" strokeWidth={1.5} />
              </motion.div>

              <motion.h2
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, ...springTransition }}
                className="text-5xl md:text-6xl font-bold tracking-tight mb-4"
              >
                You're in.
              </motion.h2>
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.35 }}
                className="text-zinc-500 text-lg mb-12 font-light"
              >
                Your founding rate is secured. Here's exactly what that means.
              </motion.p>

              <motion.div
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.45, ...springTransition }}
                className="p-8 bg-white/4 rounded-2xl border border-white/8 mb-10 text-left max-w-sm mx-auto space-y-4"
              >
                <p className="label-eyebrow text-indigo-400/70 mb-4 text-center">What you've secured</p>
                {[
                  { label: 'Founding rate', value: '$119/mo — locked permanently' },
                  { label: 'Regular price', value: '$149/mo (what others pay)' },
                  { label: 'Beta access', value: "July 2026 — you're first in" },
                  { label: 'Setup call', value: 'Direct with Arno before go-live' },
                ].map((item, i) => (
                  <div key={i} className="flex justify-between items-center text-sm border-b border-white/5 pb-3 last:border-0 last:pb-0">
                    <span className="text-zinc-500">{item.label}</span>
                    <span className="text-zinc-200 font-medium text-right max-w-[180px]">{item.value}</span>
                  </div>
                ))}
              </motion.div>

              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
                className="text-zinc-600 text-sm max-w-sm mx-auto leading-relaxed mb-10"
              >
                We'll email you one week before your cohort opens. You'll get a direct link to set up your account and book your onboarding call.
              </motion.p>

              <Link to="/landing">
                <button className="text-zinc-500 hover:text-white text-sm transition-colors">
                  ← Return to Home
                </button>
              </Link>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default WaitlistPage
