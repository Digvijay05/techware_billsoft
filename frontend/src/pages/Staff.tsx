import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../lib/api';
import { UserPlus, Search, Trash2 } from 'lucide-react';

export default function Staff() {
    const queryClient = useQueryClient();
    const [isOpen, setIsOpen] = useState(false);
    const [search, setSearch] = useState('');
    const [formData, setFormData] = useState({
        full_name: '', contact: '', email: '', employee_code: '', designation: '', address: '', dob: '', gender: '', join_date: '',
    });

    const { data: staff, isLoading } = useQuery({
        queryKey: ['staff', search],
        queryFn: async () => (await api.get(`/staff/?search=${search}`)).data,
    });

    const createMutation = useMutation({
        mutationFn: (data: any) => api.post('/staff/', data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['staff'] });
            setIsOpen(false);
            setFormData({ full_name: '', contact: '', email: '', employee_code: '', designation: '', address: '', dob: '', gender: '', join_date: '' });
        },
    });

    const deleteMutation = useMutation({
        mutationFn: (id: number) => api.delete(`/staff/${id}`),
        onSuccess: () => queryClient.invalidateQueries({ queryKey: ['staff'] }),
    });

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold text-slate-800">Staff Directory</h1>
                <button onClick={() => setIsOpen(true)} className="bg-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-800 transition-colors shadow flex items-center gap-2">
                    <UserPlus className="w-4 h-4" /> Add Staff
                </button>
            </div>

            <div className="mb-4 relative">
                <Search className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
                <input type="text" placeholder="Search by name, code, or phone..." value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="w-full pl-10 p-2.5 border border-slate-300 rounded-lg bg-white" />
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-medium text-sm">
                            <th className="p-4">Name</th>
                            <th className="p-4">Code</th>
                            <th className="p-4">Contact</th>
                            <th className="p-4">Designation</th>
                            <th className="p-4 w-20">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ? <tr><td colSpan={5} className="p-4 text-center text-slate-500">Loading...</td></tr> :
                            staff?.map((s: any) => (
                                <tr key={s.id} className="border-b border-slate-100 hover:bg-slate-50 transition-colors">
                                    <td className="p-4 font-medium text-slate-800">{s.full_name}</td>
                                    <td className="p-4 text-slate-500 text-sm uppercase">{s.employee_code || '-'}</td>
                                    <td className="p-4 text-slate-600">{s.contact || '-'}</td>
                                    <td className="p-4 text-slate-600">{s.designation || '-'}</td>
                                    <td className="p-4">
                                        <button onClick={() => { if (confirm('Delete this staff member?')) deleteMutation.mutate(s.id); }}
                                            className="text-red-500 hover:text-red-700 p-1"><Trash2 className="w-4 h-4" /></button>
                                    </td>
                                </tr>
                            ))}
                        {staff && staff.length === 0 && (
                            <tr><td colSpan={5} className="p-8 text-center text-slate-500">No staff found.</td></tr>
                        )}
                    </tbody>
                </table>
            </div>

            {isOpen && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white p-8 rounded-xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-auto">
                        <h2 className="text-2xl font-bold mb-4">Add Staff Member</h2>
                        <form onSubmit={e => { e.preventDefault(); createMutation.mutate(formData); }} className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="col-span-2">
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Full Name *</label>
                                    <input required type="text" value={formData.full_name} onChange={e => setFormData({ ...formData, full_name: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Employee Code</label>
                                    <input type="text" value={formData.employee_code} onChange={e => setFormData({ ...formData, employee_code: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Designation</label>
                                    <input type="text" value={formData.designation} onChange={e => setFormData({ ...formData, designation: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Contact</label>
                                    <input type="text" value={formData.contact} onChange={e => setFormData({ ...formData, contact: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                                    <input type="email" value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                                </div>
                                <div className="col-span-2">
                                    <label className="block text-sm font-medium text-slate-700 mb-1">Address</label>
                                    <input type="text" value={formData.address} onChange={e => setFormData({ ...formData, address: e.target.value })} className="w-full p-2 border border-slate-300 rounded-lg" />
                                </div>
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
