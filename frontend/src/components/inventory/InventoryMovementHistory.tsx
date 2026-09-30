import type { InventoryMovement } from '../../types/inventory'

interface InventoryMovementHistoryProps {
    movements: InventoryMovement[]
}

export default function InventoryMovementHistory({
    movements,
}: InventoryMovementHistoryProps) {
    return (
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold text-white">
                Movement history
            </h2>

            {movements.length === 0 ? (
                <p className="mt-4 text-sm text-slate-400">
                    No inventory movements found.
                </p>
            ) : (
                <div className="mt-6 overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead className="border-b border-slate-700 text-slate-400">
                            <tr>
                                <th className="pb-3">Type</th>
                                <th className="pb-3">Quantity</th>
                                <th className="pb-3">Reason</th>
                                <th className="pb-3">Date</th>
                            </tr>
                        </thead>

                        <tbody>
                            {movements.map((movement) => (
                                <tr
                                    key={movement.id}
                                    className="border-b border-slate-800"
                                >
                                    <td className="py-3">
                                        <span
                                            className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold capitalize ${movement.movement_type === 'entry'
                                                    ? 'bg-green-500/10 text-green-400'
                                                    : movement.movement_type === 'exit'
                                                        ? 'bg-red-500/10 text-red-400'
                                                        : 'bg-amber-500/10 text-amber-400'
                                                }`}
                                        >
                                            {movement.movement_type}
                                        </span>
                                    </td>

                                    <td className="py-3">
                                        {movement.quantity}
                                    </td>

                                    <td className="py-3">
                                        {movement.reason || '—'}
                                    </td>

                                    <td className="py-3">
                                        {movement.created_at
                                            ? new Date(movement.created_at).toLocaleString()
                                            : '—'}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    )
}