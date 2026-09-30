import api from './api'

import type {
    CreateSaleRequest,
    Sale,
} from '../types/sale'

export const saleService = {
    async getAll(token: string): Promise<Sale[]> {
        const response = await api.get<Sale[]>('/sales/', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        return response.data
    },

    async getById(
        token: string,
        saleId: number
    ): Promise<Sale> {
        const response = await api.get<Sale>(
            `/sales/${saleId}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        return response.data
    },

    async create(
        token: string,
        sale: CreateSaleRequest
    ): Promise<Sale> {
        const response = await api.post<Sale>(
            '/sales/',
            sale,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        return response.data
    },

    async cancel(
        token: string,
        saleId: number
    ): Promise<Sale> {
        const response = await api.patch<Sale>(
            `/sales/${saleId}/cancel`,
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