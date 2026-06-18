import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../lib/api';

export default function Customers() {
    const queryClient = useQueryClient();
    const [isOpen, setIsOpen] = useState(false);
    const [formData, setFormData] = useState({ name: '', phone: '', email: '', address: '' });

    const { data: customers, isLoading } = useQuery({
        queryKey: ['customers'],
        queryFn: async () => (await api.get('/customers/')).data
    });

    const mutation = useMutation({
        mutationFn: (newCustomer: any) => api.post('/customers/', newCustomer),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['customers'] });
            setIsOpen(false);
            setFormData({ name: '', phone: '', email: '', address: '' });
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        mutation.mutate(formData);
    };

    return (
        <div className="p-8 relative">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-slate-800">Customers</h1>
                <button onClick={() => setIsOpen(true)} className="bg-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-800 transition-colors shadow flex items-center gap-2">
                    + New Customer
                </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-medium">
                            <th className="p-4">Name</th>
                            <th className="p-4">Phone</th>
                            <th className="p-4">Address</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? <tr><td colSpan={3} className="p-4 text-center text-slate-500">Loading directory...</td></tr> :
                            customers?.map((c: any) => (
                                <tr key={c.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                    <td className="p-4 font-medium text-slate-800">{c.name}</td>
                                    <td className="p-4 text-slate-600">{c.phone}</td>
                                    <td className="p-4 text-slate-600">{c.address || "-"}</td>
                                </tr>
                            ))}
                        {customers && customers.length === 0 && (
                            <tr><td colSpan={3} className="p-8 text-center text-slate-500 font-medium">No customers found.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>

            {isOpen && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-md">
                        <h2 className="text-2xl font-bold mb-4">Add Customer</h2>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Name</label>
                                <input required type="text" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Phone</label>
                                <input required type="text" value={formData.phone} onChange={e => setFormData({ ...formData, phone: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                                <input type="email" value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Address</label>
                                <input type="text" value={formData.address} onChange={e => setFormData({ ...formData, address: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                            </div>
                            <div className="flex justify-end gap-3 mt-6">
                                <button type="button" onClick={() => setIsOpen(false)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-100 rounded-lg">Cancel</button>
                                <button type="submit" disabled={mutation.isPending} className="px-4 py-2 bg-primary text-white font-medium rounded-lg hover:bg-indigo-800 disabled:opacity-50">
                                    Save Customer
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    )
}
