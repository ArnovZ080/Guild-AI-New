import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { ArrowLeft, Shield } from 'lucide-react'
import { motion } from 'framer-motion'

function PrivacyPolicyPage() {
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
              <Shield size={24} />
            </div>
            <div>
              <h1 className="text-4xl font-bold font-heading">Privacy Policy</h1>
              <p className="text-zinc-500 text-sm">Last updated: March 30, 2026</p>
            </div>
          </div>

          <div className="prose prose-invert prose-zinc max-w-none">
            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">1. Introduction</h2>
              <p className="text-zinc-400 leading-relaxed mb-4">
                At Guild AI, we take your privacy seriously. This Privacy Policy explains how we collect, use, disclose, 
                and safeguard your information when you use our platform. Our "Source of Truth" architecture is designed 
                to protect your business identity while enabling our agents to serve you effectively.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">2. Information We Collect</h2>
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-bold mb-2">A. Personal Information</h3>
                  <p className="text-zinc-400 leading-relaxed">
                    We collect personal information that you voluntarily provide to us when you register on the platform, 
                    express an interest in obtaining information about us or our products and services, or otherwise when 
                    you contact us. This includes your name, email address, and billing information (processed securely through Paystack).
                  </p>
                </div>
                <div>
                  <h3 className="text-lg font-bold mb-2">B. Business Identity (Source of Truth)</h3>
                  <p className="text-zinc-400 leading-relaxed">
                    To automate your business growth, our agents learn about your company niche, industry, products, brand voice, 
                    target audience (ICP), and goals. This data is user-scoped and stored in encrypted PostgreSQL databases.
                  </p>
                </div>
                <div>
                  <h3 className="text-lg font-bold mb-2">C. Connected Accounts</h3>
                  <p className="text-zinc-400 leading-relaxed">
                    When you integrate third-party platforms (LinkedIn, Facebook, HubSpot, etc.), we store OAuth tokens securely 
                    to allow our agents to perform actions on your behalf.
                  </p>
                </div>
              </div>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">3. How We Use Your Information</h2>
              <ul className="list-disc pl-6 space-y-4 text-zinc-400 mb-6">
                <li>To facilitate account creation and logon process through Firebase.</li>
                <li>To enable our AI Orchestrator and specialized agents to generate on-brand content.</li>
                <li>To fulfill and manage your subscriptions and payments via Paystack.</li>
                <li>To improve our "Recursive Learning Engine" (using anonymized, aggregated engagement data).</li>
                <li>To send you administrative information and service updates.</li>
              </ul>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">4. Sharing of Information</h2>
              <p className="text-zinc-400 leading-relaxed mb-4">
                We only share information with your consent, to comply with laws, to provide you with services, to protect your rights, 
                or to fulfill business obligations. Primary service providers include:
              </p>
              <ul className="list-disc pl-6 space-y-2 text-zinc-400">
                <li>Google Cloud Platform (Hosting and Vertex AI)</li>
                <li>Firebase Authentication</li>
                <li>Paystack (Payment processing)</li>
              </ul>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">5. Data Security</h2>
              <p className="text-zinc-400 leading-relaxed mb-4">
                We have implemented appropriate technical and organizational security measures, including PII detection and redaction 
                in logs, end-to-end encryption for sensitive data, and secure JWT-based authentication. However, please remember 
                that no electronic transmission over the internet or information storage technology can be guaranteed to be 100% secure.
              </p>
            </section>

            <section className="mb-12">
              <h2 className="text-2xl font-bold font-heading mb-4">6. Your Rights</h2>
              <p className="text-zinc-400 leading-relaxed">
                Depending on your location, you may have rights under GDPR, CCPA, or other regional privacy laws. You can access, 
                correct, or delete your "Source of Truth" data at any time via the Settings page.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold font-heading mb-4">7. Contact Us</h2>
              <p className="text-zinc-400">
                If you have questions or comments about this policy, you may email us at:
              </p>
              <p className="text-indigo-400 font-bold mt-2">support@guildof1.com</p>
            </section>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default PrivacyPolicyPage
