import api from './api'
import type {
    Product,
    CreateProductRequest,
    UpdateProductRequest,
} from '../types/product'

export const productService = {
    async getAll(token: string): Promise<Product[]> {
        const response = await api.get<Product[]>('/products/', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        return response.data
    },

    async create(
        token: string,
        product: CreateProductRequest
    ): Promise<Product> {
        const response = await api.post<Product>(
            '/products/',
            product,
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
        code: string,
        product: UpdateProductRequest
    ): Promise<Product> {
        const response = await api.patch<Product>(
            `/products/${encodeURIComponent(code)}`,
            product,
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
        code: string
    ): Promise<Product> {
        const response = await api.patch<Product>(
            `/products/${encodeURIComponent(code)}/activate`,
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
        code: string
    ): Promise<Product> {
        const response = await api.patch<Product>(
            `/products/${encodeURIComponent(code)}/deactivate`,
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