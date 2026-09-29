import { useEffect, useState } from 'react'
import { Pencil, Power } from 'lucide-react'

import { useAuth } from '../contexts/AuthContext'
import { categoryService } from '../services/categoryService'

import type { Category } from '../types/category'

import CategoryForm from '../components/CategoryForm'

export default function CategoriesPage() {
    const { token } = useAuth()

    const [categories, setCategories] = useState<Category[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [showForm, setShowForm] = useState(false)
    const [editingCategory, setEditingCategory] = useState<Category | null>(null)
    const [refreshKey, setRefreshKey] = useState(0)

    function handleCategorySaved() {
        setShowForm(false)
        setEditingCategory(null)
        setRefreshKey((previous) => previous + 1)
    }

    function handleEdit(category: Category) {
        setEditingCategory(category)
        setShowForm(true)
    }

    const [updatingId, setUpdatingId] = useState<number | null>(null)
    const [actionError, setActionError] = useState('')

    async function handleToggleStatus(category: Category) {
        if (!token || updatingId !== null) return

        const action = category.is_active ? 'deactivate' : 'activate'

        const confirmed = window.confirm(
            `Are you sure you want to ${action} ${category.name}?`
        )

        if (!confirmed) return

        setUpdatingId(category.id)
        setActionError('')

        try {
            if (category.is_active) {
                await categoryService.deactivate(token, category.id)
            } else {
                await categoryService.activate(token, category.id)
            }

            setRefreshKey((previous) => previous + 1)
        } catch {
            setActionError(`Unable to ${action} category.`)
        } finally {
            setUpdatingId(null)
        }
    }

    useEffect(() => {
        if (!token) {
            setLoading(false)
            return
        }

        let cancelled = false

        async function loadCategories() {
            try {
                const data = await categoryService.getAll(token!)

                if (!cancelled) {
                    setCategories(data)
                }
            } catch {
                if (!cancelled) {
                    setError('Unable to load categories.')
                }
            } finally {
                if (!cancelled) {
                    setLoading(false)
                }
            }
        }

        loadCategories()

        return () => {
            cancelled = true
        }
    }, [token, refreshKey])

    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold text-white">
                Categories
            </h1>

            <p className="mt-2 text-slate-400">
                Manage your product categories.
            </p>

            <div className="mt-6">
                <button
                    type="button"
                    onClick={() => setShowForm(!showForm)}
                    className="rounded-lg bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-700"
                >
                    {showForm ? 'Cancel' : 'Add Category'}
                </button>

                {showForm && (
                    <div className="mt-6 max-w-3xl">
                        <CategoryForm
                            key={editingCategory?.id ?? 'new'}
                            category={editingCategory}
                            onCategorySaved={handleCategorySaved}
                        />
                    </div>
                )}
            </div>

            {loading && (
                <p className="mt-6 text-slate-400">
                    Loading categories...
                </p>
            )}

            {error && (
                <p role="alert" className="mt-6 text-red-400">
                    {actionError}
                </p>
            )}

            {!loading && !error && (
                <div className="mt-6">
                    <p className="mb-4 text-sm text-slate-400">
                        Total categories: {categories.length}
                    </p>

                    <div className="overflow-hidden rounded-xl border border-slate-800">
                        <table className="w-full text-left">
                            <thead className="bg-slate-900 text-sm text-slate-400">
                                <tr>
                                    <th className="px-6 py-4">Name</th>
                                    <th className="px-6 py-4">Description</th>
                                    <th className="px-6 py-4">Status</th>
                                    <th className="px-6 py-4">Actions</th>
                                </tr>
                            </thead>

                            <tbody className="divide-y divide-slate-800">
                                {categories.map((category) => (
                                    <tr key={category.id} className="text-slate-300">
                                        <td className="px-6 py-4 font-medium">
                                            {category.name}
                                        </td>

                                        <td className="px-6 py-4">
                                            {category.description || 'No description'}
                                        </td>

                                        <td className="px-6 py-4">
                                            <span
                                                className={
                                                    category.is_active
                                                        ? 'text-emerald-400'
                                                        : 'text-red-400'
                                                }
                                            >
                                                {category.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                        </td>

                                        <td className="px-6 py-4">
                                            <button
                                                type="button"
                                                onClick={() => handleEdit(category)}
                                                title="Edit category"
                                                aria-label={`Edit ${category.name}`}
                                                className="rounded-lg p-2 text-blue-400 transition hover:bg-blue-500/10"
                                            >
                                                <Pencil size={18} />
                                            </button>
                                            <button
                                                type="button"
                                                onClick={() => handleToggleStatus(category)}
                                                disabled={updatingId !== null}
                                                title={
                                                    category.is_active
                                                        ? 'Deactivate category'
                                                        : 'Activate category'
                                                }
                                                aria-label={
                                                    category.is_active
                                                        ? `Deactivate ${category.name}`
                                                        : `Activate ${category.name}`
                                                }
                                                className={`rounded-lg p-2 transition disabled:cursor-not-allowed disabled:opacity-50 ${category.is_active
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
                    </div>
                </div>
            )}
        </div>
    )
}