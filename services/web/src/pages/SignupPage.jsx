import { useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Sparkles, ArrowRight, ShieldCheck, Lock, Loader2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';
import ZARPrice from '@/components/ui/ZARPrice';
import guildLogo from '../assets/guild-logo.png';

function SignupPage() {
  const [params] = useSearchParams();
  const selectedPlan = params.get('plan') || 'growth';
  const navigate = useNavigate();
  const { signup, loginWithGoogle } = useAuth();

  const [formData, setFormData] = useState({ name: '', email: '', password: '', businessName: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await signup(formData.email, formData.password);
      navigate('/onboarding');
    } catch (err) {
      toast.error(err.message || 'Signup failed');
    }
    setLoading(false);
  };

  const handleGoogle = async () => {
    try {
      await loginWithGoogle();
      navigate('/onboarding');
    } catch (err) {
      toast.error(err.message || 'Google signup failed');
    }
  };

  const planLabels = {
    starter: { label: 'Starter', foundingPrice: '$39/mo', regularPrice: '$49/mo', usd: 39 },
    growth: { label: 'Growth', foundingPrice: '$119/mo', regularPrice: '$149/mo', usd: 119 },
    scale: { label: 'Scale', foundingPrice: '$239/mo', regularPrice: '$299/mo', usd: 239 },
  };

  const currentPlan = planLabels[selectedPlan] || planLabels.growth;

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-4xl w-full grid md:grid-cols-2 glass-panel rounded-3xl overflow-hidden">

        {/* Left panel - founding member context */}
        <div className="p-8 md:p-12 flex flex-col justify-between bg-gradient-to-br from-indigo-500/10 to-emerald-500/5 border-r border-white/[0.06]">
          <div>
            <div className="flex items-center gap-2 mb-10">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center">
                <img src={guildLogo} alt="Guild Logo" className="w-full h-full object-contain" />
              </div>
              <span className="text-xl font-heading font-bold text-gradient-cobalt">Guild AI</span>
            </div>
            <h2 className="text-3xl font-heading font-bold text-zinc-200 mb-3 leading-tight">
              You're locking in<br />your founding rate.
            </h2>
            <p className="text-zinc-400 text-sm mb-8 font-light leading-relaxed">
              Complete your account and your {currentPlan.label} rate is secured permanently - it never increases, even when public pricing does.
            </p>

            {/* Plan rate summary */}
            <div className="p-4 rounded-xl bg-white/5 border border-white/10 mb-8">
              <p className="text-xs text-indigo-400 font-bold uppercase tracking-widest mb-2">{currentPlan.label} - Founding Rate</p>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-black text-white">{currentPlan.foundingPrice}</span>
                <span className="text-zinc-600 text-sm line-through">{currentPlan.regularPrice}</span>
              </div>
              <ZARPrice usd={currentPlan.usd} className="mb-1" />
              <p className="text-zinc-600 text-xs mt-1">Locked permanently from today</p>
            </div>

            <div className="space-y-5">
              <div className="flex items-start gap-3">
                <div className="border border-white/10 glass-panel shadow-glow-sm p-2 rounded-lg flex-shrink-0">
                  <Sparkles className="text-indigo-400" size={18} strokeWidth={1.5} />
                </div>
                <div>
                  <p className="font-medium text-zinc-200 text-sm">Content That Finds You Customers</p>
                  <p className="text-xs text-zinc-400">Created, published, leads captured, nurtured to purchase - without you doing any of it manually.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="border border-white/10 glass-panel shadow-glow-sm p-2 rounded-lg flex-shrink-0">
                  <ShieldCheck className="text-indigo-400" size={18} strokeWidth={1.5} />
                </div>
                <div>
                  <p className="font-medium text-zinc-200 text-sm">Quality Checked Before You See It</p>
                  <p className="text-xs text-zinc-400">Every piece checked against your brand voice and ideal customer before it reaches your queue.</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="border border-white/10 glass-panel shadow-glow-sm p-2 rounded-lg flex-shrink-0">
                  <Lock className="text-indigo-400" size={18} strokeWidth={1.5} />
                </div>
                <div>
                  <p className="font-medium text-zinc-200 text-sm">Your Data Is Yours</p>
                  <p className="text-xs text-zinc-400">Never shared. Never used to train public models. Export everything. Cancel anytime.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-8 border-t border-white/[0.06] mt-8">
            <p className="text-xs text-zinc-600">After signup, you'll complete a short business conversation with Guild - your first week of content will be ready for review the same day.</p>
          </div>
        </div>

        {/* Right panel - form */}
        <div className="p-8 md:p-12">
          <div className="mb-6">
            <h1 className="text-2xl font-heading font-bold text-zinc-200 mb-1">Create Your Account</h1>
            <p className="text-sm text-zinc-400">
              Plan: <span className="text-indigo-400 font-medium capitalize">{currentPlan.label}</span>
              <span className="text-zinc-600 ml-2">· {currentPlan.foundingPrice} founding rate</span>
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-3">
            {[
              { key: 'name', label: 'Full Name', type: 'text', placeholder: 'Jane Smith' },
              { key: 'email', label: 'Business Email', type: 'email', placeholder: 'jane@company.com' },
              { key: 'businessName', label: 'Business Name', type: 'text', placeholder: 'Acme Corp', hint: 'Used to personalise your onboarding' },
              { key: 'password', label: 'Password', type: 'password', placeholder: '••••••••' },
            ].map(({ key, label, type, placeholder, hint }) => (
              <div key={key}>
                <label className="text-xs text-zinc-400 mb-1 block">{label}</label>
                <input
                  type={type}
                  placeholder={placeholder}
                  className="w-full px-3 py-2.5 rounded-xl bg-white/5 border border-white/[0.06] text-sm text-zinc-200 placeholder-zinc-500 outline-none focus:border-indigo-500/30 transition-colors"
                  onChange={(e) => setFormData({ ...formData, [key]: e.target.value })}
                  required={key !== 'businessName'}
                />
                {hint && <p className="text-xs text-zinc-600 mt-1">{hint}</p>}
              </div>
            ))}

            <button type="submit" disabled={loading} className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-indigo-500 text-white text-sm font-bold hover:bg-indigo-600 disabled:opacity-40 transition-colors mt-2">
              {loading ? <Loader2 size={16} className="animate-spin" /> : <>Create My Account <ArrowRight size={16} strokeWidth={1.5} /></>}
            </button>
            <p className="text-center text-xs text-zinc-500 mt-2">Billing details on the next step - takes 60 seconds.</p>
          </form>

          <div className="relative my-4">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-white/[0.06]" /></div>
            <div className="relative flex justify-center"><span className="bg-surface-raised px-3 text-xs text-zinc-500">or</span></div>
          </div>

          <button onClick={handleGoogle} className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-white/5 border border-white/[0.06] text-sm text-zinc-300 hover:bg-white/10 transition-colors">
            <svg className="w-4 h-4" viewBox="0 0 24 24"><path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18A10.96 10.96 0 0 0 1 12c0 1.77.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            Continue with Google
          </button>

          <p className="text-center text-sm text-zinc-400 mt-4">
            Already have an account? <Link to="/login" className="text-indigo-400 font-medium hover:text-indigo-300">Log In</Link>
          </p>

          <p className="text-center text-xs text-zinc-600 mt-4 leading-relaxed">
            By creating an account you agree to our <Link to="/terms" className="underline hover:text-zinc-400">Terms</Link> and <Link to="/privacy" className="underline hover:text-zinc-400">Privacy Policy</Link>.
          </p>
        </div>
      </div>
    </div>
  );
}

export default SignupPage;
