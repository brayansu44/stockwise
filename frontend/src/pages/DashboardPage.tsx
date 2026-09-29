import { useEffect, useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { dashboardService } from '../services/dashboardService'
import type { DashboardSummary } from '../types/dashboard'
import {
    Package,
    TriangleAlert,
    ShoppingCart,
    Wallet,
} from 'lucide-react'

export default function DashboardPage() {
    const { token } = useAuth()

    const [summary, setSummary] =
        useState<DashboardSummary | null>(null)

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        if (!token) return

        let cancelled = false

        async function loadDashboard() {
            try {
                const data = await dashboardService.getSummary(token!)

                if (!cancelled) {
                    setSummary(data)
                }
            } catch {
                if (!cancelled) {
                    setError('Unable to load dashboard statistics.')
                }
            } finally {
                if (!cancelled) {
                    setLoading(false)
                }
            }
        }

        loadDashboard()

        return () => {
            cancelled = true
        }
    }, [token])

    return (
        <main className="p-8">

            <section className="mx-auto mt-12 max-w-6xl">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold tracking-tight text-white">
                        Dashboard Overview
                    </h2>

                    <p className="mt-2 text-sm text-slate-400">
                        Monitor your inventory and sales performance.
                    </p>
                </div>

                {loading && (
                    <p className="mt-6 text-slate-400">
                        Loading dashboard...
                    </p>
                )}

                {error && (
                    <p className="mt-6 text-red-400">
                        {error}
                    </p>
                )}

                {summary && (
                    <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
                        {[
                            {
                                title: 'Active Products',
                                value: summary.active_products,
                                icon: Package,
                                color: 'text-blue-400',
                            },
                            {
                                title: 'Low Stock Products',
                                value: summary.low_stock_products,
                                icon: TriangleAlert,
                                color: 'text-amber-400',
                            },
                            {
                                title: 'Completed Sales',
                                value: summary.completed_sales,
                                icon: ShoppingCart,
                                color: 'text-emerald-400',
                            },
                            {
                                title: 'Total Sales',
                                value: summary.total_sales_amount.toLocaleString('en-US', {
                                    style: 'currency',
                                    currency: 'USD',
                                }),
                                icon: Wallet,
                                color: 'text-violet-400',
                            },
                        ].map((card) => (
                            <div
                                key={card.title}
                                className="min-w-0 rounded-xl border border-slate-800 bg-slate-900 p-6"
                            >
                                <div className="flex items-center justify-between gap-3">
                                    <p className="text-sm text-slate-400">
                                        {card.title}
                                    </p>

                                    <card.icon
                                        size={22}
                                        className={`shrink-0 ${card.color}`}
                                    />
                                </div>

                                <p className="mt-4 break-words text-2xl font-bold text-white">
                                    {card.value}
                                </p>
                            </div>
                        ))}
                    </div>
                )}

            </section>
        </main>
    )
}