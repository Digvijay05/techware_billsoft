import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../lib/api';
import { Search, Trash2, Eye, CheckCircle } from 'lucide-react';

export default function Invoices() {
    const queryClient = useQueryClient();
    const [search, setSearch] = useState('');
    const [statusFilter, setStatusFilter] = useState('');
    const [selectedInvoice, setSelectedInvoice] = useState<any>(null);

    const { data: invoices, isLoading } = useQuery({
        queryKey: ['invoices', search, statusFilter],
        queryFn: async () => {
            const params = new URLSearchParams();
            if (search) params.set('search', search);
            if (statusFilter) params.set('status', statusFilter);
            return (await api.get(`/invoices/?${params}`)).data;
        },
    });

    const deleteMutation = useMutation({
        mutationFn: (id: number) => api.delete(`/invoices/${id}`),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['invoices'] }),
    });

    const statusMutation = useMutation({
        mutationFn: ({ id, status }: { id: number; status: string }) =>
            api.put(`/invoices/${id}/status?status=${status}`),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['invoices'] });
            setSelectedInvoice(null);
        },
    });

    const statusColor = (s: string) => {
        if (s === 'PAID') return 'bg-emerald-100 text-emerald-700';
        if (s === 'DELIVERED') return 'bg-blue-100 text-blue-700';
        return 'bg-amber-100 text-amber-700';
    };

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-slate-800">Invoices</h1>
                <div className="flex items-center gap-3">
                    <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}
                        className="p-2.5 border border-slate-300 rounded-lg bg-white text-sm">
                        <option value="">All Status</option>
                        <option value="UNPAID">Unpaid</option>
                        <option value="PAID">Paid</option>
                        <option value="DELIVERED">Delivered</option>
                    </select>
                </div>
            </div>

            <div className="mb-4 relative">
                <Search className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
                <input type="text" placeholder="Search by bill number..." value={search}
                    onChange={e => setSearch(e.target.value)}
                    className="w-full pl-10 p-2.5 border border-slate-300 rounded-lg bg-white" />
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-medium text-sm">
                            <th className="p-4">Bill No.</th>
                            <th className="p-4">Type</th>
                            <th className="p-4">Amount</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Date</th>
                            <th className="p-4 w-24">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? <tr><td colSpan={6} className="p-4 text-center text-slate-500">Loading...</td></tr> :
                            invoices?.map((inv: any) => (
                                <tr key={inv.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                    <td className="p-4 font-medium text-slate-800">{inv.bill_number}</td>
                                    <td className="p-4 text-slate-500 text-sm">{inv.operation_type}</td>
                                    <td className="p-4 font-bold text-slate-700">₹{inv.total_amount.toFixed(2)}</td>
                                    <td className="p-4">
                                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColor(inv.status)}`}>{inv.status}</span>
                                    </td>
                                    <td className="p-4 text-slate-500 text-sm">{new Date(inv.created_at).toLocaleDateString()}</td>
                                    <td className="p-4 flex gap-1">
                                        <button onClick={() => setSelectedInvoice(inv)} className="text-indigo-500 hover:text-indigo-700 p-1">
                                            <Eye className="w-4 h-4" />
                                        </button>
                                        {inv.status === 'UNPAID' && (
                                            <button onClick={() => statusMutation.mutate({ id: inv.id, status: 'PAID' })}
                                                className="text-emerald-500 hover:text-emerald-700 p-1" title="Mark Paid">
                                                <CheckCircle className="w-4 h-4" />
                                            </button>
                                        )}
                                        <button onClick={() => { if (confirm('Delete this invoice?')) deleteMutation.mutate(inv.id); }}
                                            className="text-red-500 hover:text-red-700 p-1"><Trash2 className="w-4 h-4" /></button>
                                    </td>
                                </tr>
                            ))}
                        {invoices && invoices.length === 0 && (
                            <tr><td colSpan={6} className="p-8 text-center text-slate-500">No invoices found.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>

            {/* Invoice Detail Modal */}
            {selectedInvoice && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-lg max-h-[80vh] overflow-auto">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-2xl font-bold">Invoice #{selectedInvoice.bill_number}</h2>
                            <span className={`px-3 py-1 text-sm font-medium rounded-full ${statusColor(selectedInvoice.status)}`}>{selectedInvoice.status}</span>
                        </div>
                        <div className="space-y-3 text-sm">
                            <div className="flex justify-between"><span className="text-slate-500">Type</span><span className="font-medium">{selectedInvoice.invoice_type}</span></div>
                            <div className="flex justify-between"><span className="text-slate-500">Operation</span><span className="font-medium">{selectedInvoice.operation_type}</span></div>
                            <div className="flex justify-between"><span className="text-slate-500">Payment Mode</span><span className="font-medium">{selectedInvoice.payment_mode}</span></div>
                            <div className="flex justify-between"><span className="text-slate-500">Sub Total</span><span className="font-medium">₹{selectedInvoice.sub_total?.toFixed(2)}</span></div>
                            <div className="flex justify-between"><span className="text-slate-500">Discount</span><span className="font-medium text-emerald-600">-₹{selectedInvoice.discount_amount?.toFixed(2)}</span></div>
                            <div className="flex justify-between"><span className="text-slate-500">GST</span><span className="font-medium">₹{selectedInvoice.gst_amount?.toFixed(2)}</span></div>
                            <div className="flex justify-between"><span className="text-slate-500">Shipping</span><span className="font-medium">₹{selectedInvoice.shipping_amount?.toFixed(2)}</span></div>
                            <div className="flex justify-between text-lg font-bold border-t pt-3"><span>Total</span><span className="text-primary">₹{selectedInvoice.total_amount.toFixed(2)}</span></div>
                        </div>

                        {selectedInvoice.items?.length > 0 && (
                            <div className="mt-6">
                                <h3 className="font-semibold text-slate-700 mb-2">Line Items</h3>
                                <div className="space-y-2">
                                    {selectedInvoice.items.map((item: any, idx: number) => (
                                        <div key={idx} className="flex justify-between p-2 bg-slate-50 rounded-lg text-sm">
                                            <span>Item #{item.item_id} × {item.quantity}</span>
                                            <span className="font-medium">₹{item.price.toFixed(2)}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        <div className="flex justify-end gap-3 mt-6">
                            <button onClick={() => setSelectedInvoice(null)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-100 rounded-lg">Close</button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
