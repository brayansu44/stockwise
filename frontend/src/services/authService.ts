import api from './api'

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
}