import { Navigate, Outlet } from 'react-router'

import { useAuth } from '../contexts/AuthContext'
import type { UserRole } from '../types/user'

interface RoleProtectedRouteProps {
    allowedRoles: UserRole[]
}

export default function RoleProtectedRoute({
    allowedRoles,
}: RoleProtectedRouteProps) {
    const { user } = useAuth()

    if (!user) {
        return <Navigate to="/dashboard" replace />
    }

    if (!allowedRoles.includes(user.role)) {
        return <Navigate to="/dashboard" replace />
    }

    return <Outlet />
}