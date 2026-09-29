export interface Product {
    id: number | null
    name: string
    code: string
    description: string | null
    price: number
    current_stock: number
    minimum_stock: number
    category_id: number
    is_active: boolean
}

export interface CreateProductRequest {
    name: string
    code: string
    description: string | null
    price: number
    current_stock: number
    minimum_stock: number
    category_id: number
}

export interface UpdateProductRequest {
    name?: string | null
    description?: string | null
    price?: number | null
    minimum_stock?: number | null
    category_id?: number | null
}