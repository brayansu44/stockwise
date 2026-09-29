export interface Category {
    id: number
    name: string
    description: string | null
    is_active: boolean
}

export interface CreateCategoryRequest {
    name: string
    description: string | null
}

export interface UpdateCategoryRequest {
    name: string
    description: string | null
}