import { useState, type FormEvent } from 'react'

import { useAuth } from '../contexts/AuthContext'
import { categoryService } from '../services/categoryService'

import type {
    Category,
    CreateCategoryRequest,
} from '../types/category'

interface CategoryFormProps {
    onCategorySaved: () => void
    category?: Category | null
}

export default function CategoryForm({
    onCategorySaved,
    category = null,
}: CategoryFormProps) {
    const { token } = useAuth()

    const [form, setForm] = useState<CreateCategoryRequest>({
        name: category?.name ?? '',
        description: category?.description ?? '',
    })

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault()

        if (!token) {
            setError('You must be logged in.')
            return
        }

        setLoading(true)
        setError('')

        try {
            if (category) {
                await categoryService.update(token, category.id, form)
            } else {
                await categoryService.create(token, form)
            }

            onCategorySaved()
        } catch {
            setError('Unable to save category.')
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
                {category ? 'Edit Category' : 'Create Category'}
            </h2>

            <div>
                <label className="mb-2 block text-sm text-slate-300">
                    Category Name
                </label>

                <input
                    type="text"
                    required
                    minLength={2}
                    maxLength={100}
                    value={form.name}
                    onChange={(event) =>
                        setForm({ ...form, name: event.target.value })
                    }
                    className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 text-white"
                    placeholder="Enter category name"
                />
            </div>

            <div>
                <label className="mb-2 block text-sm text-slate-300">
                    Description
                </label>

                <textarea
                    rows={3}
                    value={form.description ?? ''}
                    onChange={(event) =>
                        setForm({ ...form, description: event.target.value })
                    }
                    className="w-full rounded-lg border border-slate-700 bg-slate-800 p-3 text-white"
                    placeholder="Enter category description"
                />
            </div>

            {error && (
                <p role="alert" className="text-sm text-red-400">
                    {error}
                </p>
            )}

            <button
                type="submit"
                disabled={loading}
                className="rounded-lg bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-700 disabled:opacity-50"
            >
                {loading
                    ? 'Saving...'
                    : category
                        ? 'Save Changes'
                        : 'Create Category'}
            </button>
        </form>
    )
}