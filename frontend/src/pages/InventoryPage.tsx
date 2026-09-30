import { useEffect, useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { productService } from '../services/productService'
import type { Product } from '../types/product'
import InventoryMovementForm from '../components/inventory/InventoryMovementForm'
import { inventoryService } from '../services/inventoryService'
import type { InventoryMovement } from '../types/inventory'
import InventoryMovementHistory from '../components/inventory/InventoryMovementHistory'

export default function InventoryPage() {
    const { token } = useAuth()

    const [products, setProducts] = useState<Product[]>([])
    const [selectedProduct, setSelectedProduct] = useState('')
    const [movements, setMovements] = useState<InventoryMovement[]>([])
    const [loadingMovements, setLoadingMovements] = useState(false)
    const [movementsError, setMovementsError] = useState('')
    const currentProduct = products.find(
        (product) => product.code === selectedProduct
    )

    useEffect(() => {
        if (!selectedProduct || !token) {
            setMovements([])
            setMovementsError('')
            return
        }

        let cancelled = false

        async function fetchMovements() {
            setLoadingMovements(true)
            setMovementsError('')
            setMovements([])

            try {
                const data = await inventoryService.getByProduct(
                    token!,
                    selectedProduct
                )

                if (!cancelled) {
                    setMovements(data)
                }
            } catch {
                if (!cancelled) {
                    setMovementsError('Unable to load movement history.')
                }
            } finally {
                if (!cancelled) {
                    setLoadingMovements(false)
                }
            }
        }

        fetchMovements()

        return () => {
            cancelled = true
        }
    }, [selectedProduct, token])

    async function refreshProducts() {
        if (!token) return

        try {
            const data = await productService.getAll(token)

            setProducts(data.filter((product) => product.is_active))
        } catch {
            setError('Unable to refresh product stock.')
        }
    }

    async function loadMovements(productCode: string) {
        if (!token) return

        setLoadingMovements(true)
        setMovementsError('')

        try {
            const data = await inventoryService.getByProduct(
                token,
                productCode
            )

            setMovements(data)
        } catch {
            setMovements([])
            setMovementsError('Unable to load movement history.')
        } finally {
            setLoadingMovements(false)
        }
    }

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        async function loadProducts() {
            if (!token) {
                setLoading(false)
                return
            }

            try {
                const data = await productService.getAll(token)
                setProducts(data.filter((product) => product.is_active))
            } catch {
                setError('Unable to load products.')
            } finally {
                setLoading(false)
            }
        }

        loadProducts()
    }, [token])

    return (
        <div className="p-8">
            <h1 className="text-3xl font-bold text-white">
                Inventory
            </h1>

            <p className="mt-2 text-slate-400">
                Manage stock movements and track product inventory.
            </p>

            <div className="mt-8 max-w-xl rounded-xl border border-slate-800 bg-slate-900 p-6">
                <label
                    htmlFor="inventory-product"
                    className="mb-2 block text-sm font-medium text-slate-300"
                >
                    Select product
                </label>

                <select
                    id="inventory-product"
                    value={selectedProduct}
                    onChange={(event) => setSelectedProduct(event.target.value)}
                    disabled={loading || products.length === 0}
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white"
                >
                    <option value="">Choose a product</option>

                    {products.map((product) => (
                        <option key={product.code} value={product.code}>
                            {product.name} ({product.code})
                        </option>
                    ))}
                </select>

                {currentProduct && (
                    <div className="mt-6 rounded-lg border border-slate-700 bg-slate-950 p-4">
                        <h3 className="font-semibold text-white">
                            {currentProduct.name}
                        </h3>

                        <p className="mt-2 text-sm text-slate-400">
                            Product code: {currentProduct.code}
                        </p>

                        <p className="mt-2 text-sm text-slate-400">
                            Current stock:
                            <span className="ml-2 font-semibold text-blue-400">
                                {currentProduct.current_stock}
                            </span>
                        </p>

                        <p className="mt-2 text-sm text-slate-400">
                            Minimum stock: {currentProduct.minimum_stock}
                        </p>

                        {currentProduct.current_stock <= currentProduct.minimum_stock && (
                            <div className="mt-4 rounded-lg border border-amber-500/30 bg-amber-500/10 p-3">
                                <p className="text-sm font-medium text-amber-400">
                                    Low stock warning
                                </p>

                                <p className="mt-1 text-sm text-amber-300">
                                    This product has reached or fallen below
                                    its minimum stock level.
                                </p>
                            </div>
                        )}
                    </div>
                )}

                {loading && (
                    <p className="mt-3 text-sm text-slate-400">
                        Loading products...
                    </p>
                )}

                {error && (
                    <p className="mt-3 text-sm text-red-400">
                        {error}
                    </p>
                )}

                {!loading && !error && products.length === 0 && (
                    <p className="mt-3 text-sm text-slate-400">
                        No active products available.
                    </p>
                )}
            </div>

            {currentProduct && (
                <div className="mt-6 max-w-xl">
                    <InventoryMovementForm
                        productCode={currentProduct.code}
                        onMovementCreated={() => {
                            refreshProducts()
                            loadMovements(currentProduct.code)
                        }}
                    />
                </div>
            )}

            {currentProduct && (
                <div className="mt-6">
                    {loadingMovements ? (
                        <p className="text-sm text-slate-400">
                            Loading movement history...
                        </p>
                    ) : movementsError ? (
                        <p className="text-sm text-red-400">
                            {movementsError}
                        </p>
                    ) : (
                        <InventoryMovementHistory movements={movements} />
                    )}
                </div>
            )}

        </div>
    )
}