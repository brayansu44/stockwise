export type SaleStatus = 'completed' | 'cancelled'

export interface CreateSaleItemRequest {
    product_code: string
    quantity: number
}

export interface CreateSaleRequest {
    items: CreateSaleItemRequest[]
}

export interface SaleItem {
    product_id: number
    quantity: number
    unit_price: number
    subtotal: number
}

export interface Sale {
    id: number | null
    seller_id: number
    status: SaleStatus
    total: number
    created_at: string | null
    items: SaleItem[]
}