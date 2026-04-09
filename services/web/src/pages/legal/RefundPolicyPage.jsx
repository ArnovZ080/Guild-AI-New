import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { ArrowLeft, RefreshCw } from 'lucide-react'
import { motion } from 'framer-motion'

function RefundPolicyPage() {
  return (
    <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
      <div className="container mx-auto max-w-4xl">
        <Link to="/landing">
          <Button variant="ghost" className="text-zinc-500 hover:text-white mb-12 group">
            <ArrowLeft className="mr-2 group-hover:-translate-x-1 transition-transform" />
            Back to Landing
          </Button>
        </Link>
        
        <motion.div
           initial={{ opacity: 0, y: 20 }}
           animate={{ opacity: 1, y: 0 }}
           transition={{ duration: 0.5 }}
           className="glass-panel p-12 rounded-3xl"
        >
          <div className="flex items-center gap-4 mb-8">
            <div className="w-12 h-12 rounded-xl gradient-cobalt flex items-center justify-center text-white shadow-lg shadow-indigo-500/20">
              <RefreshCw size={24} />
            </div>
            <div>
              <h1 className="text-4xl font-bold font-heading">Refund Policy</h1>
              <p className="text-zinc-500 text-sm">Last updated: March 30, 2026</p>
            </div>
          </div>

          <div className="prose prose-invert prose-zinc max-w-none">
            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">1. Our Promise</h2>
              <p className="text-zinc-400 leading-relaxed mb-4">
                At Guild AI, we stand behind the transformative power of our autonomous growth engine. 
                We want you to feel confident and empowered while building your business identity.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">2. 21-Day "No Slop" Guarantee</h2>
              <p className="text-zinc-400 leading-relaxed mb-4">
                We offer a <strong>21-day full refund guarantee</strong> for all new subscribers on our 
                Starter, Growth, or Scale plans. If you find that the content generated does not meet 
                our quality standards after completing the Source of Truth onboarding, you are entitled 
                to a 100% refund.
              </p>
              <ul className="list-disc pl-6 space-y-2 text-zinc-400">
                <li>Applies to the first 21 days of your initial subscription.</li>
                <li>Requires completion of the primary onboarding conversation.</li>
                <li>Refunds are processed to the original payment method via Paystack.</li>
              </ul>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">3. Monthly Renewals</h2>
              <p className="text-zinc-400 leading-relaxed mb-4">
                Subscriptions can be canceled at any time via the Settings dashboard. Once a renewal 
                has been processed, we generally do not offer refunds for that month unless technical 
                failures prevented use of the platform.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">4. Usage-Based Charges</h2>
              <p className="text-zinc-400 leading-relaxed mb-4">
                Charges for extra AI Video generation (Veo 3) or custom agent development are non-refundable 
                once the generation process has successfully completed.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">5. Processing</h2>
              <p className="text-zinc-400 leading-relaxed">
                Approved refunds are typically processed within 5-10 business days. Upon refund completion, 
                your account will revert to the Waitlist state and your Business Identity data will be 
                archived.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold font-heading mb-4">6. Contact Support</h2>
              <p className="text-zinc-400">
                To request a refund or discuss your account billing, please reach out to us:
              </p>
              <p className="text-indigo-400 font-bold mt-2">billing@guildof1.com</p>
            </section>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default RefundPolicyPage
