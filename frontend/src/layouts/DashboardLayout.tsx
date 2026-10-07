import {
    LayoutDashboard,
    Package,
    Boxes,
    ShoppingCart,
    Users,
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { NavLink, Outlet } from 'react-router'

export default function DashboardLayout() {
    const { user, logout } = useAuth()

    return (
        <div className="min-h-screen bg-slate-950 text-white">
            <aside className="fixed inset-y-0 left-0 w-64 border-r border-slate-800 bg-slate-900">
                <div className="flex h-20 items-center border-b border-slate-800 px-6">
                    <h1 className="text-2xl font-bold text-blue-400">
                        StockWise
                    </h1>
                </div>

                <nav className="space-y-2 p-4">
                    <NavLink
                        to="/dashboard"
                        className={({ isActive }) =>
                            `flex w-full items-center gap-3 rounded-lg px-4 py-3 transition ${isActive
                                ? 'bg-blue-600 text-white'
                                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                            }`
                        }
                    >
                        <LayoutDashboard size={20} />
                        Dashboard
                    </NavLink>

                    <NavLink
                        to="/products"
                        className={({ isActive }) =>
                            `flex w-full items-center gap-3 rounded-lg px-4 py-3 transition ${isActive
                                ? 'bg-blue-600 text-white'
                                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                            }`
                        }
                    >
                        <Package size={20} />
                        Products
                    </NavLink>

                    <NavLink
                        to="/categories"
                        className={({ isActive }) =>
                            `flex items-center gap-3 rounded-lg px-4 py-3 transition ${isActive
                                ? 'bg-blue-600 text-white'
                                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                            }`
                        }
                    >
                        Categories
                    </NavLink>

                    <NavLink
                        to="/inventory"
                        className={({ isActive }) =>
                            `flex w-full items-center gap-3 rounded-lg px-4 py-3 transition ${isActive
                                ? 'bg-blue-600 text-white'
                                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                            }`
                        }
                    >
                        <Boxes size={20} />
                        Inventory
                    </NavLink>

                    <NavLink
                        to="/sales"
                        className={({ isActive }) =>
                            `flex w-full items-center gap-3 rounded-lg px-4 py-3 transition ${isActive
                                ? 'bg-blue-600 text-white'
                                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                            }`
                        }
                    >
                        <ShoppingCart size={20} />
                        Sales
                    </NavLink>

                    {user?.role === 'admin' && (
                        <NavLink
                            to="/users"
                            className={({ isActive }) =>
                                `flex w-full items-center gap-3 rounded-lg px-4 py-3 transition ${isActive
                                    ? 'bg-blue-600 text-white'
                                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                }`
                            }
                        >
                            <Users size={20} />
                            Users
                        </NavLink>
                    )}
                </nav>

                <div className="absolute bottom-0 w-full border-t border-slate-800 p-4">
                    <button
                        onClick={logout}
                        className="w-full rounded-lg border border-slate-700 px-4 py-3 text-slate-300 transition hover:bg-slate-800 hover:text-white"
                    >
                        Sign Out
                    </button>
                </div>
            </aside>

            <main className="ml-64 min-h-screen">
                <Outlet />
            </main>
        </div>
    )
}