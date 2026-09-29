import api from './api'

import type {
    Category,
    CreateCategoryRequest,
    UpdateCategoryRequest,
} from '../types/category'

export const categoryService = {
    async getAll(token: string): Promise<Category[]> {
        const response = await api.get<Category[]>('/categories/', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        return response.data
    },

    async create(
        token: string,
        category: CreateCategoryRequest
    ): Promise<Category> {
        const response = await api.post<Category>(
            '/categories/',
            category,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        return response.data
    },

    async update(
        token: string,
        id: number,
        category: UpdateCategoryRequest
    ): Promise<Category> {
        const response = await api.patch<Category>(
            `/categories/${id}`,
            category,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        return response.data
    },

    async activate(
        token: string,
        id: number
    ): Promise<Category> {
        const response = await api.patch<Category>(
            `/categories/${id}/activate`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        return response.data
    },

    async deactivate(
        token: string,
        id: number
    ): Promise<Category> {
        const response = await api.patch<Category>(
            `/categories/${id}/deactivate`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        return response.data
    },
}