import { Link } from 'react-router-dom'
import { Flame } from 'lucide-react'

const nav = [
  {
    label: 'Product',
    links: [
      { to: '/features', text: 'Features' },
      { to: '/how-it-works', text: 'How It Works' },
      { to: '/pricing', text: 'Pricing' },
      { to: '/integrations', text: 'Integrations' },
    ],
  },
  {
    label: 'Company',
    links: [
      { to: '/about', text: 'About' },
      { to: '/contact', text: 'Contact' },
      { to: '/affiliates', text: 'Affiliates' },
    ],
  },
  {
    label: 'Legal',
    links: [
      { to: '/privacy', text: 'Privacy Policy' },
      { to: '/terms', text: 'Terms of Service' },
      { to: '/refund', text: 'Refund Policy' },
    ],
  },
]

export default function Footer() {
  return (
    <footer className="relative border-t border-white/[0.06] mt-24 overflow-hidden">
      {/* Subtle ember glow at top edge */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-px bg-gradient-to-r from-transparent via-indigo-500/30 to-transparent" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-64 h-16 bg-indigo-500/5 blur-2xl pointer-events-none" />

      <div className="container mx-auto max-w-6xl px-6 py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-10 mb-14">
          {/* Brand column */}
          <div className="col-span-2 md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-600 to-blue-600 flex items-center justify-center">
                <span className="text-white font-bold text-xs">G</span>
              </div>
              <span className="font-bold text-sm text-white tracking-tight">Guild <span className="text-indigo-400">AI</span></span>
            </div>
            <p className="text-xs text-zinc-600 leading-relaxed max-w-[180px]">
              One system that creates your content, captures leads, and nurtures them into customers.
            </p>
            <div className="flex items-center gap-1.5 mt-5">
              <Flame size={11} className="text-amber-500/70" />
              <span className="text-[10px] text-zinc-700 tracking-wide">Built by The AI Crucible</span>
            </div>
          </div>

          {/* Nav columns */}
          {nav.map((col) => (
            <div key={col.label}>
              <p className="label-eyebrow text-zinc-600 mb-4">{col.label}</p>
              <ul className="space-y-2.5">
                {col.links.map((l) => (
                  <li key={l.to}>
                    <Link
                      to={l.to}
                      className="text-xs text-zinc-500 hover:text-zinc-300 transition-colors duration-200"
                    >
                      {l.text}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-8 border-t border-white/[0.04]">
          <p className="text-[11px] text-zinc-700">
            © {new Date().getFullYear()} Guild AI. All rights reserved.
          </p>
          <p className="text-[11px] text-zinc-700">
            Founding cohort open - <Link to="/waitlist" className="text-indigo-500/70 hover:text-indigo-400 transition-colors">claim your spot</Link>
          </p>
        </div>
      </div>
    </footer>
  )
}
