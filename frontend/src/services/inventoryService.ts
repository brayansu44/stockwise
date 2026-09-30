import api from './api'

import type {
    CreateInventoryMovementRequest,
    InventoryMovement,
} from '../types/inventory'

export const inventoryService = {
    async create(
        token: string,
        movement: CreateInventoryMovementRequest
    ): Promise<InventoryMovement> {
        const response = await api.post<InventoryMovement>(
            '/inventory-movements/',
            movement,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        return response.data
    },

    async getByProduct(
        token: string,
        productCode: string
    ): Promise<InventoryMovement[]> {
        const response = await api.get<InventoryMovement[]>(
            `/inventory-movements/product/${encodeURIComponent(productCode)}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )

        return response.data
    },
}