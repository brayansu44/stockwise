import { useEffect, useState } from 'react'
import { Pencil, Power } from 'lucide-react'

import { useAuth } from '../contexts/AuthContext'
import { userService } from '../services/userService'

import type { User } from '../types/user'

import UserForm from '../components/UserForm'

export default function UsersPage() {
    const { token } = useAuth()

    const [users, setUsers] = useState<User[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [actionError, setActionError] = useState('')
    const [showForm, setShowForm] = useState(false)
    const [editingUser, setEditingUser] = useState<User | null>(null)
    const [updatingId, setUpdatingId] = useState<number | null>(null)
    const [refreshKey, setRefreshKey] = useState(0)

    function handleUserSaved() {
        setShowForm(false)
        setEditingUser(null)
        setRefreshKey((previous) => previous + 1)
    }

    function handleAddUser() {
        setEditingUser(null)
        setShowForm((previous) => !previous)
    }

    function handleEdit(user: User) {
        setEditingUser(user)
        setShowForm(true)
    }

    async function handleToggleStatus(user: User) {
        if (!token || updatingId !== null) return

        const action = user.is_active ? 'deactivate' : 'activate'

        const confirmed = window.confirm(
            `Are you sure you want to ${action} ${user.name}?`
        )

        if (!confirmed) return

        setUpdatingId(user.id)
        setActionError('')

        try {
            if (user.is_active) {
                await userService.deactivate(token, user.id)
            } else {
                await userService.activate(token, user.id)
            }

            setRefreshKey((previous) => previous + 1)
        } catch {
            setActionError(`Unable to ${action} user.`)
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

        async function loadUsers() {
            setLoading(true)
            setError('')

            try {
                const data = await userService.getAll(token!)

                if (!cancelled) {
                    setUsers(data)
                }
            } catch {
                if (!cancelled) {
                    setError('Unable to load users.')
                }
            } finally {
                if (!cancelled) {
                    setLoading(false)
                }
            }
        }

        loadUsers()

        return () => {
            cancelled = true
        }
    }, [token, refreshKey])

    function formatRole(role: User['role']) {
        if (role === 'admin') return 'Admin'
        if (role === 'inventory_operator') return 'Inventory Operator'
        return 'Seller'
    }

    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold text-white">
                Users
            </h1>

            <p className="mt-2 text-slate-400">
                Manage system users and their roles.
            </p>

            <div className="mt-6">
                <button
                    type="button"
                    onClick={handleAddUser}
                    className="rounded-lg bg-blue-600 px-5 py-3 font-medium text-white hover:bg-blue-700"
                >
                    {showForm && !editingUser ? 'Cancel' : 'Add User'}
                </button>

                {showForm && (
                    <div className="mt-6 max-w-3xl">
                        <UserForm
                            key={editingUser?.id ?? 'new'}
                            user={editingUser}
                            onUserSaved={handleUserSaved}
                        />
                    </div>
                )}
            </div>

            {loading && (
                <p className="mt-6 text-slate-400">
                    Loading users...
                </p>
            )}

            {error && (
                <p role="alert" className="mt-6 text-red-400">
                    {error}
                </p>
            )}

            {actionError && (
                <p role="alert" className="mt-6 text-red-400">
                    {actionError}
                </p>
            )}

            {!loading && !error && (
                <div className="mt-6">
                    <p className="mb-4 text-sm text-slate-400">
                        Total users: {users.length}
                    </p>

                    <div className="overflow-hidden rounded-xl border border-slate-800">
                        <table className="w-full text-left">
                            <thead className="bg-slate-900 text-sm text-slate-400">
                                <tr>
                                    <th className="px-6 py-4">Name</th>
                                    <th className="px-6 py-4">Email</th>
                                    <th className="px-6 py-4">Role</th>
                                    <th className="px-6 py-4">Status</th>
                                    <th className="px-6 py-4">Actions</th>
                                </tr>
                            </thead>

                            <tbody className="divide-y divide-slate-800">
                                {users.map((user) => (
                                    <tr
                                        key={user.id}
                                        className="text-slate-300"
                                    >
                                        <td className="px-6 py-4 font-medium">
                                            {user.name}
                                        </td>

                                        <td className="px-6 py-4">
                                            {user.email}
                                        </td>

                                        <td className="px-6 py-4">
                                            {formatRole(user.role)}
                                        </td>

                                        <td className="px-6 py-4">
                                            <span
                                                className={
                                                    user.is_active
                                                        ? 'text-emerald-400'
                                                        : 'text-red-400'
                                                }
                                            >
                                                {user.is_active
                                                    ? 'Active'
                                                    : 'Inactive'}
                                            </span>
                                        </td>

                                        <td className="px-6 py-4">
                                            <button
                                                type="button"
                                                onClick={() => handleEdit(user)}
                                                title="Edit user"
                                                aria-label={`Edit ${user.name}`}
                                                className="rounded-lg p-2 text-blue-400 transition hover:bg-blue-500/10"
                                            >
                                                <Pencil size={18} />
                                            </button>

                                            <button
                                                type="button"
                                                onClick={() =>
                                                    handleToggleStatus(user)
                                                }
                                                disabled={updatingId !== null}
                                                title={
                                                    user.is_active
                                                        ? 'Deactivate user'
                                                        : 'Activate user'
                                                }
                                                aria-label={
                                                    user.is_active
                                                        ? `Deactivate ${user.name}`
                                                        : `Activate ${user.name}`
                                                }
                                                className={`rounded-lg p-2 transition disabled:cursor-not-allowed disabled:opacity-50 ${user.is_active
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