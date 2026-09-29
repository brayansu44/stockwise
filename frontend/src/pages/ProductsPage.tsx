import axios from 'axios'

import { useEffect, useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { productService } from '../services/productService'
import type { Product } from '../types/product'
import ProductForm from '../components/ProductForm'
import { Pencil, Power } from 'lucide-react'

export default function ProductsPage() {
    const { token } = useAuth()

    const [products, setProducts] = useState<Product[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [search, setSearch] = useState('')
    const [statusFilter, setStatusFilter] = useState('all')
    const [showForm, setShowForm] = useState(false)
    const [editingProduct, setEditingProduct] =
        useState<Product | null>(null)

    function handleEdit(product: Product) {
        setEditingProduct(product)
        setShowForm(true)
    }

    const [updatingCode, setUpdatingCode] = useState<string | null>(null)
    const [actionError, setActionError] = useState('')

    async function handleToggleStatus(product: Product) {
        if (!token || updatingCode) return

        const action = product.is_active ? 'deactivate' : 'activate'

        const confirmed = window.confirm(
            `Are you sure you want to ${action} ${product.name}?`
        )

        if (!confirmed) return

        setUpdatingCode(product.code)
        setActionError('')

        try {
            if (product.is_active) {
                await productService.deactivate(token, product.code)
            } else {
                await productService.activate(token, product.code)
            }

            setRefreshKey((previous) => previous + 1)
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const detail = error.response?.data?.detail

                if (error.response?.status === 403) {
                    setActionError(
                        'You do not have permission to change product status.'
                    )
                } else if (typeof detail === 'string') {
                    setActionError(detail)
                } else {
                    setActionError(`Unable to ${action} product.`)
                }
            } else {
                setActionError('An unexpected error occurred.')
            }
        } finally {
            setUpdatingCode(null)
        }
    }

    const [refreshKey, setRefreshKey] = useState(0)

    function handleProductCreated() {
        setRefreshKey((previous) => previous + 1)
        setShowForm(false)
        setEditingProduct(null)
    }

    useEffect(() => {
        if (!token) {
            setLoading(false)
            return
        }

        let cancelled = false

        async function loadProducts() {
            try {
                const data = await productService.getAll(token!)

                if (!cancelled) {
                    setProducts(data)
                }
            } catch {
                if (!cancelled) {
                    setError('Unable to load products.')
                }
            } finally {
                if (!cancelled) {
                    setLoading(false)
                }
            }
        }

        loadProducts()

        return () => {
            cancelled = true
        }
    }, [token, refreshKey])

    const filteredProducts = products.filter((product) => {
        const query = search.toLowerCase().trim()

        const matchesSearch =
            product.name.toLowerCase().includes(query) ||
            product.code.toLowerCase().includes(query)

        const matchesStatus =
            statusFilter === 'all' ||
            (statusFilter === 'active' && product.is_active) ||
            (statusFilter === 'inactive' && !product.is_active)

        return matchesSearch && matchesStatus
    })

    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold text-white">
                Products
            </h1>

            <p className="mt-2 text-sm text-slate-400">
                Manage and monitor your product catalog.
            </p>

            <div className="mt-6">
                <button
                    type="button"
                    onClick={() => {
                        setEditingProduct(null)
                        setShowForm(!showForm)

                        if (!showForm) {
                            setShowForm(true)
                        }
                    }}
                    className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-blue-700"
                >
                    {showForm ? 'Cancel' : 'Add Product'}
                </button>

                {showForm && (
                    <div className="mt-6 max-w-3xl">
                        <ProductForm
                            key={editingProduct?.code ?? 'new'}
                            product={editingProduct}
                            onProductCreated={handleProductCreated}
                        />
                    </div>
                )}
            </div>

            <div className="mt-8">
                <input
                    type="search"
                    value={search}
                    onChange={(event) => setSearch(event.target.value)}
                    placeholder="Search by name or code..."
                    className="w-full max-w-sm rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-500 focus:border-blue-500"
                />
            </div>

            <select
                value={statusFilter}
                onChange={(event) => setStatusFilter(event.target.value)}
                className="mt-4 rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white outline-none focus:border-blue-500"
            >
                <option value="all">All Products</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
            </select>

            <div className="mt-6 flex items-center justify-between">
                <p className="text-sm text-slate-400">
                    Showing{' '}
                    <span className="font-semibold text-white">
                        {filteredProducts.length}
                    </span>{' '}
                    of{' '}
                    <span className="font-semibold text-white">
                        {products.length}
                    </span>{' '}
                    products
                </p>
            </div>

            {actionError && (
                <p role="alert" className="mt-6 text-sm text-red-400">
                    {actionError}
                </p>
            )}

            {loading && (
                <p className="mt-8 text-slate-400">
                    Loading products...
                </p>
            )}

            {error && (
                <p className="mt-8 text-red-400">
                    {error}
                </p>
            )}

            {!loading && !error && (
                <div className="mt-8 overflow-x-auto rounded-xl border border-slate-800 bg-slate-900">
                    <table className="w-full text-left text-sm">
                        <thead className="border-b border-slate-800 bg-slate-800/50 text-slate-400">
                            <tr>
                                <th className="px-6 py-4">Product</th>
                                <th className="px-6 py-4">Code</th>
                                <th className="px-6 py-4">Price</th>
                                <th className="px-6 py-4">Stock</th>
                                <th className="px-6 py-4">Status</th>
                                <th className="px-6 py-4">Actions</th>
                            </tr>
                        </thead>

                        <tbody className="divide-y divide-slate-800">
                            {filteredProducts.map((product) => (
                                <tr
                                    key={product.code}
                                    className="transition hover:bg-slate-800/50"
                                >
                                    <td className="px-6 py-4 font-medium text-white">
                                        {product.name}
                                    </td>

                                    <td className="px-6 py-4 text-slate-400">
                                        {product.code}
                                    </td>

                                    <td className="px-6 py-4 text-white">
                                        {product.price.toLocaleString('en-US', {
                                            minimumFractionDigits: 2,
                                            maximumFractionDigits: 2,
                                        })}
                                    </td>

                                    <td className="px-6 py-4">
                                        <span
                                            className={
                                                product.current_stock <= product.minimum_stock
                                                    ? 'text-amber-400'
                                                    : 'text-slate-300'
                                            }
                                        >
                                            {product.current_stock}
                                        </span>
                                    </td>

                                    <td className="px-6 py-4">
                                        <span
                                            className={`rounded-full px-3 py-1 text-xs font-medium ${product.is_active
                                                ? 'bg-emerald-500/10 text-emerald-400'
                                                : 'bg-red-500/10 text-red-400'
                                                }`}
                                        >
                                            {product.is_active ? 'Active' : 'Inactive'}
                                        </span>
                                    </td>

                                    <td className="px-6 py-4">
                                        <button
                                            type="button"
                                            onClick={() => handleEdit(product)}
                                            className="rounded-lg p-2 text-blue-400 transition hover:bg-slate-800"
                                            title="Edit product"
                                            aria-label={`Edit ${product.name}`}
                                        >
                                            <Pencil size={18} />
                                        </button>

                                        <button
                                            type="button"
                                            onClick={() => handleToggleStatus(product)}
                                            disabled={updatingCode !== null}
                                            title={
                                                product.is_active
                                                    ? 'Deactivate product'
                                                    : 'Activate product'
                                            }
                                            aria-label={
                                                product.is_active
                                                    ? `Deactivate ${product.name}`
                                                    : `Activate ${product.name}`
                                            }
                                            className={`rounded-lg p-2 transition disabled:cursor-not-allowed disabled:opacity-50 ${product.is_active
                                                ? 'text-red-400 hover:bg-red-500/10'
                                                : 'text-emerald-400 hover:bg-emerald-500/10'
                                                }`}
                                        >
                                            <Power size={18} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    {filteredProducts.length === 0 && (
                        <p className="p-8 text-center text-slate-400">
                            No products found.
                        </p>
                    )}
                </div>
            )}
        </div>
    )
}