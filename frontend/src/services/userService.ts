import api from './api'
import type {
    CreateUserRequest,
    UpdateUserRequest,
    User,
} from '../types/user'

export const userService = {
    async getAll(token: string): Promise<User[]> {
        const response = await api.get<User[]>('/users/', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        return response.data
    },

    async create(
        token: string,
        data: CreateUserRequest,
    ): Promise<User> {
        const response = await api.post<User>('/users/', data, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        return response.data
    },

    async update(
        token: string,
        userId: number,
        data: UpdateUserRequest,
    ): Promise<User> {
        const response = await api.put<User>(
            `/users/${userId}`,
            data,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            },
        )

        return response.data
    },

    async deactivate(
        token: string,
        userId: number,
    ): Promise<User> {
        const response = await api.patch<User>(
            `/users/${userId}/deactivate`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            },
        )

        return response.data
    },

    async activate(
        token: string,
        userId: number,
    ): Promise<User> {
        const response = await api.patch<User>(
            `/users/${userId}/activate`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            },
        )

        return response.data
    },
}