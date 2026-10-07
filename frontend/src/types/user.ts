export type UserRole = 'admin' | 'inventory_operator' | 'seller'

export interface CreateUserRequest {
    name: string
    email: string
    password: string
    role: UserRole
}

export interface UpdateUserRequest {
    name: string
    email: string
    role: UserRole
}

export interface User {
    id: number
    name: string
    email: string
    role: UserRole
    is_active: boolean
}