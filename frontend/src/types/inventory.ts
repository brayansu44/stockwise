export type MovementType = 'entry' | 'exit' | 'adjustment'

export interface CreateInventoryMovementRequest {
    product_code: string
    movement_type: MovementType
    quantity: number
    reason: string | null
}

export interface InventoryMovement {
    id: number | null
    product_id: number
    movement_type: MovementType
    quantity: number
    reason: string | null
    sale_id: number | null
    created_at: string | null
}