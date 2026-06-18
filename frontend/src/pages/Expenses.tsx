import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../lib/api';
import { PlusCircle, Trash2 } from 'lucide-react';

export default function Expenses() {
    const queryClient = useQueryClient();
    const [isOpen, setIsOpen] = useState(false);
    const [formData, setFormData] = useState({ category: '', amount: '', description: '' });

    const { data: expenses, isLoading } = useQuery({
        queryKey: ['expenses'],
        queryFn: async () => (await api.get('/expenses/')).data,
    });

    const { data: categories } = useQuery({
        queryKey: ['expense-categories'],
        queryFn: async () => (await api.get('/expenses/categories')).data,
    });

    const createMutation = useMutation({
        mutationFn: (data: any) => api.post('/expenses/', data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['expenses'] });
            setIsOpen(false);
            setFormData({ category: '', amount: '', description: '' });
        },
    });

    const deleteMutation = useMutation({
        mutationFn: (id: number) => api.delete(`/expenses/${id}`),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['expenses'] }),
    });

    const totalExpenses = expenses?.reduce((sum: number, e: any) => sum + e.amount, 0) || 0;

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold text-slate-800">Expenses</h1>
                    <p className="text-slate-500 mt-1">Total: <span className="font-bold text-red-600">₹{totalExpenses.toFixed(2)}</span></p>
                </div>
                <button onClick={() => setIsOpen(true)} className="bg-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-800 transition-colors shadow flex items-center gap-2">
                    <PlusCircle className="w-4 h-4" /> Add Expense
                </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-medium text-sm">
                            <th className="p-4">Category</th>
                            <th className="p-4">Description</th>
                            <th className="p-4">Amount</th>
                            <th className="p-4">Date</th>
                            <th className="p-4 w-20">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? <tr><td colSpan={5} className="p-4 text-center text-slate-500">Loading...</td></tr> :
                            expenses?.map((e: any) => (
                                <tr key={e.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                    <td className="p-4">
                                        <span className="px-2 py-1 bg-orange-100 text-orange-700 text-xs font-medium rounded-full">{e.category}</span>
                                    </td>
                                    <td className="p-4 text-slate-600">{e.description || '-'}</td>
                                    <td className="p-4 font-bold text-red-600">₹{e.amount.toFixed(2)}</td>
                                    <td className="p-4 text-slate-500 text-sm">{new Date(e.date).toLocaleDateString()}</td>
                                    <td className="p-4">
                                        <button onClick={() => { if (confirm('Delete this expense?')) deleteMutation.mutate(e.id); }}
                                            className="text-red-500 hover:text-red-700 p-1"><Trash2 className="w-4 h-4" /></button>
                                    </td>
                                </tr>
                            ))}
                        {expenses && expenses.length === 0 && (
                            <tr><td colSpan={5} className="p-8 text-center text-slate-500">No expenses recorded.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>

            {isOpen && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-md">
                        <h2 className="text-2xl font-bold mb-4">Add Expense</h2>
                        <form onSubmit={e => { e.preventDefault(); createMutation.mutate({ ...formData, amount: parseFloat(formData.amount) }); }} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Category*</label>
                                <input required list="expense-cats" type="text" value={formData.category}
                                    onChange={e => setFormData({ ...formData, category: e.target.value })}
                                    className="w-full p-2 border border-slate-300 rounded-lg" placeholder="e.g. Rent, Utilities..." />
                                <datalist id="expense-cats">
                                    {categories?.map((c: any) => <option key={c.id} value={c.name} />)}
                                </datalist>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Amount (₹)*</label>
                                <input required type="number" step="0.01" min="0" value={formData.amount}
                                    onChange={e => setFormData({ ...formData, amount: e.target.value })}
                                    className="w-full p-2 border border-slate-300 rounded-lg" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
                                <input type="text" value={formData.description}
                                    onChange={e => setFormData({ ...formData, description: e.target.value })}
                                    className="w-full p-2 border border-slate-300 rounded-lg" />
                            </div>
                            <div className="flex justify-end gap-3 mt-6">
                                <button type="button" onClick={() => setIsOpen(false)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-100 rounded-lg">Cancel</button>
                                <button type="submit" disabled={createMutation.isPending} className="px-4 py-2 bg-primary text-white font-medium rounded-lg hover:bg-indigo-800 disabled:opacity-50">Save</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
