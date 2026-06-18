import { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import api from '../lib/api';

export default function POS() {
    const [cart, setCart] = useState<any[]>([]);
    const [customerPhone, setCustomerPhone] = useState('');

    const { data: items } = useQuery({
        queryKey: ['items'],
        queryFn: async () => {
            const res = await api.get('/items/');
            if (res.data && res.data.length > 0) return res.data;
            return [];
        }
    });

    const mutation = useMutation({
        mutationFn: (orderData: any) => api.post('/invoices/', orderData),
        onSuccess: () => {
            alert("Invoice Successfully Recorded!");
            setCart([]);
            setCustomerPhone('');
        },
        onError: (_err: any) => {
            alert("Failed to record invoice. Make sure customer phone exists in directory.");
        }
    });

    const addToCart = (item: any) => {
        setCart([...cart, { ...item, quantity: 1 }]);
    };

    const handleCharge = () => {
        if (!customerPhone) return alert("Please enter the customer's phone number.");
        if (cart.length === 0) return alert("Cart is empty.");

        const orderData = {
            bill_number: `INV-${Date.now()}`,
            total_amount: total,
            sub_total: total,
            status: "PAID",
            operation_type: "RETAIL",
            discount_amount: 0.0,
            customer_phone: customerPhone,
            items: cart.map(c => ({
                item_id: c.id,
                quantity: c.quantity,
                rate: c.rate,
                price: c.rate * c.quantity
            }))
        };

        mutation.mutate(orderData);
    }

    const total = cart.reduce((sum, item) => sum + (item.rate * item.quantity), 0);

    return (
        <div className="flex h-full">
            {/* Items Section */}
            <div className="flex-1 p-8 overflow-auto border-r border-slate-200 products-section">
                <h1 className="text-2xl font-bold text-slate-800 mb-6">Products & Services</h1>
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                    {items?.map((item: any) => (
                        <div
                            key={item.id}
                            onClick={() => addToCart(item)}
                            className="p-4 bg-white border border-slate-200 rounded-xl cursor-pointer hover:border-primary hover:shadow-md transition-all flex flex-col justify-between h-32"
                        >
                            <h3 className="font-semibold text-slate-800 line-clamp-2">{item.name}</h3>
                            <p className="text-primary font-bold mt-2 text-lg">${item.rate.toFixed(2)}</p>
                        </div>
                    ))}
                    {(!items || items.length === 0) && (
                        <p className="text-slate-500 col-span-full">No items found in inventory. Please add items in the Inventory screen.</p>
                    )}
                </div>
            </div>

            {/* Cart Section */}
            <div className="w-96 bg-white flex flex-col shadow-2xl z-10 cart-section">
                <div className="p-6 border-b border-slate-100">
                    <h2 className="text-xl font-bold text-slate-800 mb-4">Current Order</h2>
                    <input
                        type="text"
                        placeholder="Customer Phone No."
                        value={customerPhone}
                        onChange={(e) => setCustomerPhone(e.target.value)}
                        className="w-full p-2 border border-slate-300 rounded-lg text-sm"
                    />
                </div>
                <div className="flex-1 p-6 overflow-auto space-y-4">
                    {cart.map((item, idx) => (
                        <div key={idx} className="flex justify-between items-center p-3 bg-slate-50 rounded-lg border border-slate-100">
                            <div>
                                <p className="font-medium text-slate-800">{item.name}</p>
                                <p className="text-xs text-slate-500 mt-1">Qty: {item.quantity}</p>
                            </div>
                            <p className="font-bold text-slate-700">${(item.rate * item.quantity).toFixed(2)}</p>
                        </div>
                    ))}
                    {cart.length === 0 && (
                        <div className="h-full flex items-center justify-center">
                            <p className="text-slate-400 text-center">Select items to begin</p>
                        </div>
                    )}
                </div>
                <div className="p-6 bg-slate-50 border-t border-slate-200">
                    <div className="flex justify-between items-center mb-6">
                        <span className="text-slate-600 font-medium text-lg">Total</span>
                        <span className="text-4xl font-bold text-primary">${total.toFixed(2)}</span>
                    </div>
                    <button
                        onClick={handleCharge}
                        disabled={mutation.isPending}
                        className="w-full py-4 bg-primary text-white rounded-xl font-bold text-lg hover:bg-indigo-800 transition-colors shadow-lg active:scale-[0.98] mb-3 disabled:opacity-50"
                    >
                        {mutation.isPending ? 'Processing...' : `Charge $${total.toFixed(2)}`}
                    </button>
                    <button onClick={() => window.print()} className="w-full py-3 bg-white text-slate-800 border border-slate-200 rounded-xl font-bold hover:bg-slate-50 transition-colors shadow-sm active:scale-[0.98]">
                        Print Invoice
                    </button>
                </div>
            </div>
        </div>
    );
}
