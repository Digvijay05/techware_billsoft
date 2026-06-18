import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../lib/api';

export default function Inventory() {
    const queryClient = useQueryClient();
    const [isOpen, setIsOpen] = useState(false);
    const [formData, setFormData] = useState({ name: '', item_code: '', rate: '', category_id: 1 });

    const { data: items, isLoading } = useQuery({
        queryKey: ['items'],
        queryFn: async () => (await api.get('/items/')).data
    });

    const { data: categories } = useQuery({
        queryKey: ['categories'],
        queryFn: async () => (await api.get('/items/categories/all')).data
    });

    const mutation = useMutation({
        mutationFn: (newItem: any) => api.post('/items/', newItem),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['items'] });
            setIsOpen(false);
            setFormData({ name: '', item_code: '', rate: '', category_id: categories?.[0]?.id || 1 });
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        mutation.mutate({
            ...formData,
            rate: parseFloat(formData.rate)
        });
    };

    return (
        <div className="p-8 relative">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-slate-800">Inventory</h1>
                <button onClick={() => setIsOpen(true)} className="bg-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-800 transition-colors shadow flex items-center gap-2">
                    + Add Product
                </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-medium">
                            <th className="p-4">SKU / Code</th>
                            <th className="p-4">Product Name</th>
                            <th className="p-4">Sale Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? <tr><td colSpan={3} className="p-4 text-center text-slate-500">Loading catalog...</td></tr> :
                            items?.map((i: any) => (
                                <tr key={i.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                    <td className="p-4 text-slate-500 uppercase text-sm mt-1">{i.item_code || "-"}</td>
                                    <td className="p-4 font-medium text-slate-800">{i.name}</td>
                                    <td className="p-4 font-bold text-slate-700">${i.rate.toFixed(2)}</td>
                                </tr>
                            ))}
                        {items && items.length === 0 && (
                            <tr><td colSpan={3} className="p-8 text-center text-slate-500 font-medium">No items found in catalog.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>

            {isOpen && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-md">
                        <h2 className="text-2xl font-bold mb-4">Add Product</h2>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Product Name</label>
                                <input required type="text" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Item Code / SKU</label>
                                <input required type="text" value={formData.item_code} onChange={e => setFormData({ ...formData, item_code: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Rate ($)</label>
                                <input required type="number" step="0.01" value={formData.rate} onChange={e => setFormData({ ...formData, rate: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-1">Category</label>
                                <select value={formData.category_id} onChange={e => setFormData({ ...formData, category_id: parseInt(e.target.value) })} className="w-full p-2 border border-slate-300 rounded-lg bg-white">
                                    {categories?.map((c: any) => (
                                        <option key={c.id} value={c.id}>{c.name}</option>
                                    ))}
                                    {(!categories || categories.length === 0) && <option value="1">Default Category</option>}
                                </select>
                            </div>
                            <div className="flex justify-end gap-3 mt-6">
                                <button type="button" onClick={() => setIsOpen(false)} className="px-4 py-2 text-slate-600 font-medium hover:bg-slate-100 rounded-lg">Cancel</button>
                                <button type="submit" disabled={mutation.isPending} className="px-4 py-2 bg-primary text-white font-medium rounded-lg hover:bg-indigo-800 disabled:opacity-50">
                                    Save Product
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    )
}
