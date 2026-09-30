import { useEffect, useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { saleService } from '../services/saleService'
import type { Sale } from '../types/sale'
import SaleForm from '../components/sales/SaleForm'
import { productService } from '../services/productService'
import type { Product } from '../types/product'

export default function SalesPage() {

    const { token, user } = useAuth()

    const [sales, setSales] = useState<Sale[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')
    const [cancellingSaleId, setCancellingSaleId] = useState<number | null>(null)
    const [products, setProducts] = useState<Product[]>([])

    async function loadSales() {
        if (!token) {
            return
        }

        try {
            const data = await saleService.getAll(token)
            setSales(data)
            setError('')
        } catch {
            setError('Could not load sales.')
        }
    }

    async function loadProducts() {
        if (!token) {
            return
        }

        try {
            const data = await productService.getAll(token)

            setProducts(
                data.filter(
                    (product) =>
                        product.is_active && product.current_stock > 0
                )
            )
        } catch {
            setError('Could not load products.')
        }
    }

    async function handleCancelSale(saleId: number) {
        if (!token) {
            return
        }

        const confirmed = window.confirm(
            `Are you sure you want to cancel sale #${saleId}?`
        )

        if (!confirmed) {
            return
        }

        setError('')
        setSuccess('')
        setCancellingSaleId(saleId)

        try {
            await saleService.cancel(token, saleId)

            await loadSales()
            await loadProducts()

            setError('')
            setSuccess(`Sale #${saleId} cancelled successfully.`)
        } catch {
            setError('Could not cancel the sale.')
        } finally {
            setCancellingSaleId(null)
        }
    }

    useEffect(() => {
        let cancelled = false

        async function loadInitialSales() {
            if (!token) {
                setLoading(false)
                return
            }

            setLoading(true)
            setError('')

            try {
                const data = await saleService.getAll(token)

                if (!cancelled) {
                    setSales(data)
                }
            } catch {
                if (!cancelled) {
                    setError('Unable to load sales.')
                }
            } finally {
                if (!cancelled) {
                    setLoading(false)
                }
            }
        }

        loadInitialSales()

        return () => {
            cancelled = true
        }
    }, [token])

    useEffect(() => {
        let cancelled = false

        async function loadInitialProducts() {
            if (!token) return

            try {
                const data = await productService.getAll(token)

                if (!cancelled) {
                    setProducts(
                        data.filter(
                            (product) =>
                                product.is_active && product.current_stock > 0
                        )
                    )
                }
            } catch {
                if (!cancelled) {
                    setProducts([])
                }
            }
        }

        loadInitialProducts()

        return () => {
            cancelled = true
        }
    }, [token])

    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold text-white">
                Sales
            </h1>

            <p className="mt-2 text-slate-400">
                Manage sales and view transaction history.
            </p>

            {success && (
                <div className="mt-4 rounded-lg border border-green-500/30 bg-green-500/10 px-4 py-3 text-sm text-green-400">
                    {success}
                </div>
            )}

            {error && (
                <div className="mt-4 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                    {error}
                </div>
            )}

            <SaleForm
                products={products}
                onSaleCreated={() => {
                    loadSales()
                    loadProducts()
                }}
            />

            <div className="mt-8 overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
                {loading ? (
                    <p className="p-6 text-slate-400">
                        Loading sales...
                    </p>
                ) : error ? (
                    <p className="p-6 text-red-400">
                        {error}
                    </p>
                ) : sales.length === 0 ? (
                    <p className="p-6 text-slate-400">
                        No sales registered yet.
                    </p>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="border-b border-slate-700 text-slate-400">
                                <tr>
                                    <th className="p-4">Sale ID</th>
                                    <th className="p-4">Seller ID</th>
                                    <th className="p-4">Total</th>
                                    <th className="p-4">Status</th>
                                    <th className="p-4">Date</th>
                                    <th className="px-4 py-3 text-left">
                                        Actions
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                {sales.map((sale) => (
                                    <tr
                                        key={sale.id}
                                        className="border-b border-slate-800"
                                    >
                                        <td className="p-4">{sale.id}</td>

                                        <td className="p-4">{sale.seller_id}</td>

                                        <td className="p-4">
                                            {sale.total.toLocaleString('es-CO', {
                                                style: 'currency',
                                                currency: 'COP',
                                            })}
                                        </td>

                                        <td className="p-4 capitalize">
                                            {sale.status}
                                        </td>

                                        <td className="p-4">
                                            {sale.created_at
                                                ? new Date(sale.created_at).toLocaleString('es-CO')
                                                : '—'}
                                        </td>

                                        <td className="px-4 py-3">
                                            {user?.role === 'admin' &&
                                                sale.status === 'completed' && (
                                                    <button
                                                        type="button"
                                                        onClick={() => {
                                                            if (sale.id !== null) {
                                                                handleCancelSale(sale.id)
                                                            }
                                                        }}
                                                        disabled={cancellingSaleId !== null}
                                                        className="rounded-lg border border-red-500/30 px-3 py-2 text-sm font-medium text-red-400 transition hover:bg-red-500/10"
                                                    >
                                                        Cancel sale
                                                    </button>
                                                )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    )
}