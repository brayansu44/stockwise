import { useEffect, useState, type FormEvent } from 'react'
import axios from 'axios'
import type {
    Product,
    CreateProductRequest,
} from '../types/product'
import { useAuth } from '../contexts/AuthContext'
import { productService } from '../services/productService'
import { categoryService } from '../services/categoryService'
import type { Category } from '../types/category'

interface ProductFormProps {
    onProductCreated: () => void
    product?: Product | null
}

export default function ProductForm({
    onProductCreated,
    product = null,
}: ProductFormProps) {

    const { token } = useAuth()

    const [categories, setCategories] = useState<Category[]>([])

    useEffect(() => {
        if (!token) return

        let cancelled = false

        async function loadCategories() {
            try {
                const data = await categoryService.getAll(token!)

                if (!cancelled) {
                    setCategories(data)
                }
            } catch (error) {
                console.error('Error loading categories:', error)
            }
        }

        loadCategories()

        return () => {
            cancelled = true
        }
    }, [token])

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')

    const [form, setForm] = useState<CreateProductRequest>({
        name: product?.name ?? '',
        code: product?.code ?? '',
        description: product?.description ?? '',
        price: product?.price ?? 0,
        current_stock: product?.current_stock ?? 0,
        minimum_stock: product?.minimum_stock ?? 0,
        category_id: product?.category_id ?? 0,
    })

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault()

        if (!token) {
            setError('You must be logged in.')
            return
        }

        setLoading(true)
        setError('')
        setSuccess('')

        try {
            if (product) {
                await productService.update(token, product.code, {
                    name: form.name,
                    description: form.description,
                    price: form.price,
                    minimum_stock: form.minimum_stock,
                    category_id: form.category_id,
                })

                setSuccess('Product updated successfully.')
            } else {
                await productService.create(token, form)

                setSuccess('Product created successfully.')
            }

            onProductCreated()
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const detail = error.response?.data?.detail

                if (typeof detail === 'string') {
                    setError(detail)
                } else if (error.response?.status === 403) {
                    setError('You do not have permission to save products.')
                } else {
                    setError('Unable to save product. Please check your data.')
                }
            } else {
                setError('An unexpected error occurred.')
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-5 rounded-xl border border-slate-800 bg-slate-900 p-6"
        >
            <h2 className="text-xl font-semibold text-white">
                {product ? 'Edit Product' : 'Create Product'}
            </h2>

            <div className="grid gap-5 md:grid-cols-2">
                <div>
                    <label
                        htmlFor="product-name"
                        className="mb-2 block text-sm text-slate-300"
                    >
                        Product Name
                    </label>

                    <input
                        id="product-name"
                        type="text"
                        required
                        minLength={2}
                        maxLength={100}
                        value={form.name}
                        onChange={(event) =>
                            setForm({ ...form, name: event.target.value })
                        }
                        placeholder="Enter product name"
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
                    />
                </div>

                <div>
                    <label
                        htmlFor="product-code"
                        className="mb-2 block text-sm text-slate-300"
                    >
                        Product Code
                    </label>

                    <input
                        id="product-code"
                        type="text"
                        required
                        minLength={2}
                        maxLength={50}
                        value={form.code}
                        disabled={!!product}
                        onChange={(event) =>
                            setForm({ ...form, code: event.target.value })
                        }
                        placeholder="Enter product code"
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
                    />
                </div>
            </div>
            <div>
                <label className="mb-2 block text-sm text-slate-300">
                    Description
                </label>

                <textarea
                    value={form.description ?? ''}
                    onChange={(event) =>
                        setForm({ ...form, description: event.target.value })
                    }
                    placeholder="Enter product description"
                    rows={3}
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
                />
            </div>

            <div className="grid gap-5 md:grid-cols-2">
                {[
                    { label: 'Price', field: 'price' },
                    { label: 'Initial Stock', field: 'current_stock' },
                    { label: 'Minimum Stock', field: 'minimum_stock' },
                ].map(({ label, field }) => (
                    <div key={field}>
                        <label className="mb-2 block text-sm text-slate-300">
                            {label}
                        </label>

                        <input
                            type="number"
                            required
                            min={field === 'category_id' ? 1 : 0}
                            step={field === 'price' ? '0.01' : '1'}
                            disabled={!!product && field === 'current_stock'}
                            value={form[field as keyof Pick<
                                CreateProductRequest,
                                'price' | 'current_stock' | 'minimum_stock' | 'category_id'
                            >]}
                            onChange={(event) =>
                                setForm({
                                    ...form,
                                    [field]: Number(event.target.value),
                                })
                            }
                            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
                        />
                    </div>
                ))}
            </div>

            <div>
                <label
                    htmlFor="product-category"
                    className="mb-2 block text-sm text-slate-300"
                >
                    Category
                </label>

                <select
                    id="product-category"
                    required
                    value={form.category_id || ''}
                    onChange={(event) =>
                        setForm({
                            ...form,
                            category_id: Number(event.target.value),
                        })
                    }
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-blue-500"
                >
                    <option value="" disabled>
                        Select a category
                    </option>

                    {categories
                        .filter(
                            (category) =>
                                category.is_active ||
                                category.id === form.category_id
                        )
                        .map((category) => (
                            <option
                                key={category.id}
                                value={category.id}
                            >
                                {category.name}
                                {!category.is_active ? ' (Inactive)' : ''}
                            </option>
                        ))}
                </select>
            </div>

            {error && (
                <p className="text-sm text-red-400">{error}</p>
            )}

            {success && (
                <p className="text-sm text-emerald-400">{success}</p>
            )}

            <button
                type="submit"
                className="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700" disabled={loading}
            >
                {loading
                    ? product ? 'Saving...' : 'Creating...'
                    : product ? 'Save Changes' : 'Create Product'}
            </button>
        </form>
    )
}