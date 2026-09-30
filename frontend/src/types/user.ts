export type UserRole = 'admin' | 'inventory_operator' | 'seller'

export interface User {
    id: number
    name: string
    email: string
    role: UserRole
    is_active: boolean
}