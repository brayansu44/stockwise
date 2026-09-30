import { useState } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { inventoryService } from '../../services/inventoryService'
import axios from 'axios'
import type { MovementType } from '../../types/inventory'

interface InventoryMovementFormProps {
    productCode: string
    onMovementCreated: () => void
}

export default function InventoryMovementForm({
    productCode,
    onMovementCreated,
}: InventoryMovementFormProps) {
    const [movementType, setMovementType] =
        useState<MovementType>('entry')

    const [quantity, setQuantity] = useState('')
    const [reason, setReason] = useState('')

    const { token } = useAuth()

    const [submitting, setSubmitting] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')

    async function handleSubmit(
        event: React.SubmitEvent<HTMLFormElement>
    ) {
        event.preventDefault()

        setError('')
        setSuccess('')

        if (!token) {
            setError('Your session has expired. Please sign in again.')
            return
        }

        if (quantity.trim() === '') {
            setError('Please enter a quantity.')
            return
        }

        const parsedQuantity = Number(quantity)

        if (
            !Number.isSafeInteger(parsedQuantity) ||
            parsedQuantity < 0
        ) {
            setError('Please enter a valid non-negative integer.')
            return
        }

        setSubmitting(true)

        try {
            await inventoryService.create(token, {
                product_code: productCode,
                movement_type: movementType,
                quantity: parsedQuantity,
                reason: reason.trim() || null,
            })

            setSuccess('Stock movement registered successfully.')
            onMovementCreated()
            setQuantity('')
            setReason('')
        } catch (err) {
            if (axios.isAxiosError(err)) {
                const detail = err.response?.data?.detail

                setError(
                    typeof detail === 'string'
                        ? detail
                        : 'Unable to register stock movement.'
                )
            } else {
                setError('An unexpected error occurred.')
            }
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold text-white">
                Register stock movement
            </h2>

            <form onSubmit={handleSubmit} className="mt-6 space-y-4">
                <div>
                    <label className="mb-2 block text-sm text-slate-300">
                        Movement type
                    </label>

                    <select
                        value={movementType}
                        onChange={(event) =>
                            setMovementType(event.target.value as MovementType)
                        }
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white"
                    >
                        <option value="entry">Entry</option>
                        <option value="exit">Exit</option>
                        <option value="adjustment">Adjustment</option>
                    </select>
                </div>

                <div>
                    <label className="mb-2 block text-sm text-slate-300">
                        {movementType === 'adjustment'
                            ? 'New stock quantity'
                            : 'Quantity'}
                    </label>

                    <input
                        type="number"
                        min="0"
                        step="1"
                        value={quantity}
                        onChange={(event) => setQuantity(event.target.value)}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white"
                    />
                </div>

                <div>
                    <label className="mb-2 block text-sm text-slate-300">
                        Reason (optional)
                    </label>

                    <textarea
                        value={reason}
                        onChange={(event) => setReason(event.target.value)}
                        maxLength={255}
                        rows={3}
                        className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white"
                    />
                </div>

                {movementType === 'adjustment' && (
                    <p className="text-sm text-amber-400">
                        Adjustment replaces the current stock with the
                        specified quantity.
                    </p>
                )}

                {error && (
                    <p className="text-sm text-red-400">
                        {error}
                    </p>
                )}

                {success && (
                    <p className="text-sm text-green-400">
                        {success}
                    </p>
                )}

                <button
                    type="submit"
                    disabled={submitting}
                    className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
                >
                    {submitting ? 'Registering...' : 'Register movement'}
                </button>
            </form>
        </div >
    )
}