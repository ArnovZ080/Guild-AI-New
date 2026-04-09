import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, Lock, Mail, Loader2 } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-toastify';

function LoginPage() {
  const navigate = useNavigate();
  const { login, loginWithGoogle } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(formData.email, formData.password);
      navigate('/');
    } catch (err) {
      toast.error(err.message || 'Login failed');
    }
    setLoading(false);
  };

  const handleGoogle = async () => {
    try {
      await loginWithGoogle();
      navigate('/');
    } catch (err) {
      toast.error(err.message || 'Google login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="w-12 h-12 gradient-cobalt rounded-xl flex items-center justify-center font-bold text-white text-lg mx-auto mb-4 shadow-lg shadow-blue-500/20">
            G
          </div>
          <h1 className="text-3xl font-heading font-bold text-zinc-200">Welcome Back</h1>
          <p className="text-zinc-400 mt-2">Log in to your Guild AI growth engine.</p>
        </div>

        <div className="glass-panel rounded-2xl p-8 space-y-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-600 w-4 h-4" strokeWidth={1.5} />
              <input
                type="email"
                placeholder="Email Address"
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-white/5 border border-white/[0.06] text-sm text-zinc-200 placeholder-zinc-500 outline-none focus:border-indigo-500/30 transition-colors"
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
              />
            </div>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500 w-4 h-4" strokeWidth={1.5} />
              <input
                type="password"
                placeholder="Password"
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-white/5 border border-white/[0.06] text-sm text-zinc-200 placeholder-zinc-500 outline-none focus:border-indigo-500/30 transition-colors"
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-indigo-500 text-white text-sm font-bold hover:bg-indigo-600 disabled:opacity-40 transition-colors"
            >
              {loading ? <Loader2 size={16} className="animate-spin" /> : <>Log In <ArrowRight size={16} strokeWidth={1.5} /></>}
            </button>
          </form>

          <div className="relative">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-white/[0.06]" /></div>
            <div className="relative flex justify-center"><span className="bg-surface-base px-3 text-xs text-zinc-500">or</span></div>
          </div>

          <button onClick={handleGoogle} className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-white/5 border border-white/[0.06] text-sm text-zinc-300 hover:bg-white/10 transition-colors">
            <svg className="w-4 h-4" viewBox="0 0 24 24"><path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18A10.96 10.96 0 0 0 1 12c0 1.77.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            Continue with Google
          </button>

          <p className="text-center text-sm text-zinc-400">
            Don't have an account? <Link to="/signup" className="text-indigo-400 font-medium hover:text-indigo-300">Get Started</Link>
          </p>
        </div>

        <p className="text-center text-xs text-zinc-600">© 2026 Guild AI. Your growth partner.</p>
      </div>
    </div>
  );
}

export default LoginPage;
