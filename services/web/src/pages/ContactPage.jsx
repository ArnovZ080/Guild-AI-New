import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { 
  ArrowLeft, Mail, MessageSquare, Phone, Send,
  HelpCircle, Briefcase, Users, Clock, MapPin
} from 'lucide-react'
import { motion } from 'framer-motion'

function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    subject: 'general',
    message: ''
  })

  const [isSubmitting, setIsSubmitting] = useState(false)

  const contactMethods = [
    {
      icon: <Mail className="w-6 h-6" />,
      title: 'Email Us',
      description: 'Get a response within 24 hours',
      contact: 'support@guildof1.com',
      color: 'from-blue-500 to-indigo-500'
    },
    {
      icon: <MessageSquare className="w-6 h-6" />,
      title: 'Live Chat',
      description: 'Expert support team',
      contact: 'Available 9am-6pm SAST',
      color: 'from-indigo-500 to-purple-500'
    },
    {
      icon: <Phone className="w-6 h-6" />,
      title: 'Schedule a Demo',
      description: 'Walkthrough with an expert',
      contact: 'In-app Calendar integration',
      color: 'from-purple-500 to-pink-500'
    }
  ]

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    // Simulated contact form logic
    await new Promise(resolve => setTimeout(resolve, 1500))
    alert('Thank you! Your message has been routed to our support team.')
    setFormData({ name: '', email: '', company: '', subject: 'general', message: '' })
    setIsSubmitting(false)
  }

  return (
    <div className="min-h-screen bg-transparent text-white pt-24 pb-20 px-6">
      <div className="container mx-auto max-w-6xl">
        <Link to="/landing">
          <Button variant="ghost" className="text-zinc-400 hover:text-white mb-12 group">
            <ArrowLeft className="mr-2 group-hover:-translate-x-1 transition-transform" />
            Back to Landing
          </Button>
        </Link>

        <section className="text-center mb-20">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold font-heading tracking-tight mb-8">
                Get in <span className="text-gradient-cobalt">Touch</span>
            </h1>
            <p className="text-xl text-zinc-400 max-w-2xl mx-auto font-light leading-relaxed">
                Have questions about your Guild AI tools? Our team is ready to help you scale.
            </p>
          </motion.div>
        </section>

        <div className="grid lg:grid-cols-3 gap-8 mb-20">
            {contactMethods.map((method, i) => (
                <div key={i} className="glass-panel p-8 rounded-2xl group transition-all">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${method.color} flex items-center justify-center text-white mb-6 shadow-lg group-hover:scale-110 transition-transform`}>
                        {method.icon}
                    </div>
                    <h3 className="text-xl font-bold font-heading mb-2">{method.title}</h3>
                    <p className="text-sm text-zinc-400 mb-4 font-light">{method.description}</p>
                    <p className="font-medium text-indigo-400">{method.contact}</p>
                </div>
            ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-12 items-start">
            <motion.div 
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="glass-panel p-10 rounded-3xl"
            >
                <h2 className="text-3xl font-bold font-heading mb-8">Send a Message</h2>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-6">
                        <div className="space-y-2">
                            <Label className="text-zinc-400">Full Name</Label>
                            <Input name="name" value={formData.name} onChange={handleInputChange} required className="bg-white/5 border-white/10 text-white rounded-xl focus:ring-indigo-500/50" />
                        </div>
                        <div className="space-y-2">
                            <Label className="text-zinc-400">Email Address</Label>
                            <Input type="email" name="email" value={formData.email} onChange={handleInputChange} required className="bg-white/5 border-white/10 text-white rounded-xl focus:ring-indigo-500/50" />
                        </div>
                    </div>
                    <div className="space-y-2">
                        <Label className="text-zinc-400">Subject</Label>
                        <select name="subject" value={formData.subject} onChange={handleInputChange} className="w-full bg-white/5 border border-white/10 text-white rounded-xl p-2.5 outline-none focus:ring-2 focus:ring-indigo-500/50">
                            <option value="general">General Inquiry</option>
                            <option value="support">Technical Support</option>
                            <option value="sales">Sales & Demos</option>
                            <option value="billing">Billing Question</option>
                        </select>
                    </div>
                    <div className="space-y-2">
                        <Label className="text-zinc-400">Message</Label>
                        <Textarea name="message" value={formData.message} onChange={handleInputChange} required rows={5} className="bg-white/5 border-white/10 text-white rounded-xl focus:ring-indigo-500/50" />
                    </div>
                    <Button type="submit" disabled={isSubmitting} className="w-full bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 py-6 rounded-xl font-bold text-lg shadow-xl shadow-indigo-500/20">
                        {isSubmitting ? 'Sending...' : 'Transmit Message'}
                    </Button>
                </form>
            </motion.div>

            <div className="space-y-8 text-zinc-400 font-light leading-relaxed">
                <div>
                    <h4 className="text-white font-bold font-heading text-lg mb-4 flex items-center gap-2">
                        <MapPin size={20} className="text-indigo-400" /> Headquarters
                    </h4>
                    <p>Guild AI / Arno Adaptive Holdings</p>
                    <p>Cape Town, South Africa 8001</p>
                </div>
                <div>
                    <h4 className="text-white font-bold font-heading text-lg mb-4 flex items-center gap-2">
                        <Clock size={20} className="text-indigo-400" /> Business Operations
                    </h4>
                    <p>Monday - Friday: 9am - 6pm SAST</p>
                    <p>Saturday: 10am - 2pm SAST</p>
                    <p>Agents: Operational 24/7/365</p>
                </div>
                <div className="p-8 glass-panel rounded-2xl border-indigo-500/10">
                    <h4 className="text-white font-bold font-heading mb-4 flex items-center gap-2">
                        <HelpCircle size={18} className="text-indigo-400" /> FAQ Snapshot
                    </h4>
                    <div className="space-y-4 text-sm">
                        <p><strong>Demos:</strong> We offer guided walkthroughs for Growth and Scale tiers.</p>
                        <p><strong>Support:</strong> Priority response is included for Professional plans.</p>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </div>
  )
}

export default ContactPage
