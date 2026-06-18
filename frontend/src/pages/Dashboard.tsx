import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';
import { TrendingUp, Users, Package, FileText, AlertCircle, DollarSign } from 'lucide-react';

export default function Dashboard() {
    const { data: stats, isLoading } = useQuery({
        queryKey: ['dashboard'],
        queryFn: async () => (await api.get('/reports/dashboard')).data,
    });

    const { data: recentInvoices } = useQuery({
        queryKey: ['invoices-recent'],
        queryFn: async () => (await api.get('/invoices/?limit=5')).data,
    });

    const cards = [
        { label: 'Total Sales', value: stats?.total_sales, prefix: '₹', icon: TrendingUp, color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-200' },
        { label: 'Total Invoices', value: stats?.total_invoices, prefix: '', icon: FileText, color: 'text-indigo-600', bg: 'bg-indigo-50', border: 'border-indigo-200' },
        { label: 'Customers', value: stats?.total_customers, prefix: '', icon: Users, color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-200' },
        { label: 'Products', value: stats?.total_items, prefix: '', icon: Package, color: 'text-purple-600', bg: 'bg-purple-50', border: 'border-purple-200' },
        { label: 'Unpaid Invoices', value: stats?.unpaid_invoices, prefix: '', icon: AlertCircle, color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-200' },
        { label: 'Total Expenses', value: stats?.total_expenses, prefix: '₹', icon: DollarSign, color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' },
    ];

    const statusColor = (s: string) => {
        if (s === 'PAID') return 'bg-emerald-100 text-emerald-700';
        if (s === 'DELIVERED') return 'bg-blue-100 text-blue-700';
        return 'bg-amber-100 text-amber-700';
    };

    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold mb-6 text-slate-800">Command Center</h1>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-8">
                {cards.map((card, i) => (
                    <div key={i} className={`${card.bg} p-5 rounded-xl border ${card.border} transition-shadow hover:shadow-md`}>
                        <div className="flex items-center gap-2 mb-2">
                            <card.icon className={`w-4 h-4 ${card.color}`} />
                            <h2 className="text-xs font-medium text-slate-500 uppercase">{card.label}</h2>
                        </div>
                        <p className={`text-2xl font-bold ${card.color}`}>
                            {isLoading ? '...' : `${card.prefix}${typeof card.value === 'number' ? (card.prefix === '₹' ? card.value.toFixed(2) : card.value) : 0}`}
                        </p>
                    </div>
                ))}
            </div>

            {/* Recent Invoices */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="p-5 border-b border-slate-100">
                    <h2 className="text-lg font-bold text-slate-800">Recent Invoices</h2>
                </div>
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-slate-50 border-b border-slate-200 text-slate-500 font-medium text-xs uppercase">
                            <th className="p-4">Bill No.</th>
                            <th className="p-4">Amount</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {recentInvoices?.map((inv: any) => (
                            <tr key={inv.id} className="border-b border-slate-50 hover:bg-slate-50 transition-colors">
                                <td className="p-4 font-medium text-slate-800">{inv.bill_number}</td>
                                <td className="p-4 font-bold text-slate-700">₹{inv.total_amount.toFixed(2)}</td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColor(inv.status)}`}>{inv.status}</span>
                                </td>
                                <td className="p-4 text-slate-500 text-sm">{new Date(inv.created_at).toLocaleDateString()}</td>
                            </tr>
                        ))}
                        {(!recentInvoices || recentInvoices.length === 0) && (
                            <tr><td colSpan={4} className="p-8 text-center text-slate-400">No invoices yet. Create one from the POS screen.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
