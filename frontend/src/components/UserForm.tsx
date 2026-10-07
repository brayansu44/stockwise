import { useState } from 'react'
import axios from 'axios'

import { useAuth } from '../contexts/AuthContext'
import { userService } from '../services/userService'

import type {
    User,
    UserRole,
} from '../types/user'

interface UserFormProps {
    user?: User | null
    onUserSaved: () => void
}

export default function UserForm({
    user,
    onUserSaved,
}: UserFormProps) {
    const { token } = useAuth()

    const [name, setName] = useState(user?.name ?? '')
    const [email, setEmail] = useState(user?.email ?? '')
    const [password, setPassword] = useState('')
    const [role, setRole] = useState<UserRole>(
        user?.role ?? 'seller'
    )
    const [submitting, setSubmitting] = useState(false)
    const [error, setError] = useState('')

    async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()

        if (!token || submitting) return

        setSubmitting(true)
        setError('')

        try {
            if (user) {
                await userService.update(token, user.id, {
                    name,
                    email,
                    role,
                })
            } else {
                await userService.create(token, {
                    name,
                    email,
                    password,
                    role,
                })
            }

            onUserSaved()
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const detail = error.response?.data?.detail

                if (typeof detail === 'string') {
                    setError(detail)
                    return
                }
            }

            setError(
                user
                    ? 'Unable to update user.'
                    : 'Unable to create user.'
            )
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="rounded-xl border border-slate-800 bg-slate-900 p-6"
        >
            <h2 className="text-xl font-semibold text-white">
                {user ? 'Edit User' : 'Add User'}
            </h2>

            {error && (
                <p
                    role="alert"
                    className="mt-4 text-sm text-red-400"
                >
                    {error}
                </p>
            )}

            <div className="mt-6">
                <label
                    htmlFor="user-name"
                    className="mb-2 block text-sm font-medium text-slate-300"
                >
                    Full Name
                </label>

                <input
                    id="user-name"
                    type="text"
                    value={name}
                    onChange={(event) => setName(event.target.value)}
                    required
                    minLength={2}
                    maxLength={100}
                    placeholder="Enter full name"
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition placeholder:text-slate-500 focus:border-blue-500"
                />
            </div>

            <div className="mt-4">
                <label
                    htmlFor="user-email"
                    className="mb-2 block text-sm font-medium text-slate-300"
                >
                    Email
                </label>

                <input
                    id="user-email"
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    required
                    placeholder="Enter email address"
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition placeholder:text-slate-500 focus:border-blue-500"
                />
            </div>

            {!user && (
                <div className="mt-4">
                    <label
                        htmlFor="user-password"
                        className="mb-2 block text-sm font-medium text-slate-300"
                    >
                        Password
                    </label>

                    <input
                        id="user-password"
                        type="password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        required
                        minLength={8}
                        maxLength={128}
                        placeholder="Enter password"
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition placeholder:text-slate-500 focus:border-blue-500"
                    />
                </div>
            )}

            <div className="mt-4">
                <label
                    htmlFor="user-role"
                    className="mb-2 block text-sm font-medium text-slate-300"
                >
                    Role
                </label>

                <select
                    id="user-role"
                    value={role}
                    onChange={(event) =>
                        setRole(event.target.value as UserRole)
                    }
                    required
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition focus:border-blue-500"
                >
                    <option value="admin">Admin</option>
                    <option value="inventory_operator">
                        Inventory Operator
                    </option>
                    <option value="seller">Seller</option>
                </select>
            </div>

            <button
                type="submit"
                disabled={submitting}
                className="mt-6 rounded-lg bg-blue-600 px-5 py-3 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
                {submitting
                    ? 'Saving...'
                    : user
                        ? 'Update User'
                        : 'Create User'}
            </button>
        </form>
    )
}