import api from './api'
import type { User } from '../types/user'

interface LoginCredentials {
    email: string
    password: string
}

interface LoginResponse {
    access_token: string
}

export const authService = {
    async login(credentials: LoginCredentials): Promise<LoginResponse> {
        const response = await api.post<LoginResponse>(
            '/auth/login',
            credentials
        )

        return response.data
    },

    async getMe(token: string): Promise<User> {
        const response = await api.get<User>('/auth/me', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        return response.data
    },
}