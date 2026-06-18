import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import api from '../lib/api';

export default function Login({ onLogin }: { onLogin: (user: any) => void }) {
    const [employeeCode, setEmployeeCode] = useState('');
    const [password, setPassword] = useState('');
    const [isRegister, setIsRegister] = useState(false);
    const [firstName, setFirstName] = useState('');
    const [error, setError] = useState('');

    const loginMutation = useMutation({
        mutationFn: (data: any) => api.post('/auth/login', data),
        onSuccess: (res) => {
            localStorage.setItem('token', res.data.access_token);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            onLogin(res.data.user);
        },
        onError: () => setError('Invalid credentials'),
    });

    const registerMutation = useMutation({
        mutationFn: (data: any) => api.post('/auth/register', data),
        onSuccess: () => {
            setIsRegister(false);
            setError('');
            setEmployeeCode('');
            setPassword('');
        },
        onError: () => setError('Registration failed. User may already exist.'),
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        if (isRegister) {
            registerMutation.mutate({ first_name: firstName, employee_code: employeeCode, password, role: 'admin' });
        } else {
            loginMutation.mutate({ employee_code: employeeCode, password });
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-950 via-indigo-900 to-slate-900">
            <div className="w-full max-w-md">
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-white tracking-tight">Techware BillSoft</h1>
                    <p className="text-indigo-300 mt-2">Billing & Inventory Management</p>
                </div>
                <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-8 shadow-2xl">
                    <h2 className="text-xl font-semibold text-white mb-6">{isRegister ? 'Create Account' : 'Sign In'}</h2>
                    {error && <div className="mb-4 p-3 bg-red-500/20 border border-red-500/30 rounded-lg text-red-200 text-sm">{error}</div>}
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {isRegister && (
                            <div>
                                <label className="block text-sm font-medium text-indigo-200 mb-1">Full Name</label>
                                <input required type="text" value={firstName} onChange={e => setFirstName(e.target.value)}
                                    className="w-full p-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                                    placeholder="John Doe" />
                            </div>
                        )}
                        <div>
                            <label className="block text-sm font-medium text-indigo-200 mb-1">Employee Code</label>
                            <input required type="text" value={employeeCode} onChange={e => setEmployeeCode(e.target.value)}
                                className="w-full p-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                                placeholder="EMP001" autoFocus />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-indigo-200 mb-1">Password</label>
                            <input required type="password" value={password} onChange={e => setPassword(e.target.value)}
                                className="w-full p-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                                placeholder="••••••••" />
                        </div>
                        <button type="submit" disabled={loginMutation.isPending || registerMutation.isPending}
                            className="w-full py-3 bg-indigo-500 hover:bg-indigo-400 text-white font-bold rounded-xl transition-colors shadow-lg disabled:opacity-50 mt-2">
                            {loginMutation.isPending || registerMutation.isPending ? 'Please wait...' : (isRegister ? 'Create Account' : 'Sign In')}
                        </button>
                    </form>
                    <button onClick={() => { setIsRegister(!isRegister); setError(''); }}
                        className="w-full mt-4 text-sm text-indigo-300 hover:text-white transition-colors">
                        {isRegister ? '← Back to Sign In' : 'First time? Create an account'}
                    </button>
                </div>
            </div>
        </div>
    );
}
