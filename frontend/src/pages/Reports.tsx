import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';
import { TrendingUp, TrendingDown, DollarSign } from 'lucide-react';

export default function Reports() {
    const [period, setPeriod] = useState<'daily' | 'monthly' | 'yearly' | 'lifetime'>('monthly');

    const { data: report, isLoading } = useQuery({
        queryKey: ['report', period],
        queryFn: async () => (await api.get(`/reports/${period}`)).data,
    });

    const { data: dashboard } = useQuery({
        queryKey: ['dashboard'],
        queryFn: async () => (await api.get('/reports/dashboard')).data,
    });

    const cards = [
        { label: 'Total Revenue', value: report?.total_revenue || 0, icon: TrendingUp, color: 'text-emerald-600', bg: 'bg-emerald-50' },
        { label: 'Total Expenses', value: report?.total_expenses || 0, icon: TrendingDown, color: 'text-red-600', bg: 'bg-red-50' },
        { label: 'Net Profit', value: report?.net_profit || 0, icon: DollarSign, color: report?.net_profit >= 0 ? 'text-emerald-600' : 'text-red-600', bg: report?.net_profit >= 0 ? 'bg-emerald-50' : 'bg-red-50' },
    ];

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-slate-800">Reports</h1>
                <div className="flex gap-1 bg-slate-100 p-1 rounded-xl">
                    {(['daily', 'monthly', 'yearly', 'lifetime'] as const).map(p => (
                        <button key={p} onClick={() => setPeriod(p)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-colors ${period === p ? 'bg-white text-primary shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}>
                            {p}
                        </button>
                    ))}
                </div>
            </div>

            {/* Revenue Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {cards.map((card, i) => (
                    <div key={i} className={`${card.bg} p-6 rounded-xl border border-slate-200/50`}>
                        <div className="flex items-center gap-3 mb-2">
                            <card.icon className={`w-5 h-5 ${card.color}`} />
                            <h3 className="text-sm font-medium text-slate-600">{card.label}</h3>
                        </div>
                        <p className={`text-3xl font-bold ${card.color}`}>
                            {isLoading ? '...' : `₹${card.value.toFixed(2)}`}
                        </p>
                    </div>
                ))}
            </div>

            {/* Invoice Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <h3 className="text-sm font-medium text-slate-500 mb-1">Invoices</h3>
                    <p className="text-3xl font-bold text-slate-800">{isLoading ? '...' : report?.invoice_count || 0}</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <h3 className="text-sm font-medium text-slate-500 mb-1">Paid</h3>
                    <p className="text-3xl font-bold text-emerald-600">{isLoading ? '...' : report?.paid_count || 0}</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <h3 className="text-sm font-medium text-slate-500 mb-1">Unpaid</h3>
                    <p className="text-3xl font-bold text-amber-600">{isLoading ? '...' : report?.unpaid_count || 0}</p>
                </div>
            </div>

            {/* Quick Overview */}
            {dashboard && (
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">Lifetime Overview</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        <div>
                            <p className="text-sm text-slate-500">Total Sales</p>
                            <p className="text-xl font-bold text-slate-800">₹{dashboard.total_sales?.toFixed(2)}</p>
                        </div>
                        <div>
                            <p className="text-sm text-slate-500">Total Invoices</p>
                            <p className="text-xl font-bold text-slate-800">{dashboard.total_invoices}</p>
                        </div>
                        <div>
                            <p className="text-sm text-slate-500">Customers</p>
                            <p className="text-xl font-bold text-slate-800">{dashboard.total_customers}</p>
                        </div>
                        <div>
                            <p className="text-sm text-slate-500">Products</p>
                            <p className="text-xl font-bold text-slate-800">{dashboard.total_items}</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
