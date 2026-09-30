import { useState } from 'react'
import type { Product } from '../../types/product'

import { useAuth } from '../../contexts/AuthContext'
import { saleService } from '../../services/saleService'
import axios from 'axios'

interface SaleFormProps {
    products: Product[]
    onSaleCreated: () => void
}

export default function SaleForm({
    products,
    onSaleCreated,
}: SaleFormProps) {

    const { token } = useAuth()

    const [productCode, setProductCode] = useState('')
    const [quantity, setQuantity] = useState('')

    const [submitting, setSubmitting] = useState(false)
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')

    const [items, setItems] = useState<
        { product: Product; quantity: number }[]
    >([])

    const selectedProduct = products.find(
        (product) => product.code === productCode
    )

    const total = items.reduce(
        (sum, item) => sum + item.product.price * item.quantity,
        0
    )

    function handleAddProduct() {
        setSuccess('')
        setError('')

        if (!selectedProduct) {
            setError('Please select a product.')
            return
        }

        if (quantity.trim() === '') {
            setError('Please enter a quantity.')
            return
        }

        const parsedQuantity = Number(quantity)

        if (
            !Number.isSafeInteger(parsedQuantity) ||
            parsedQuantity <= 0
        ) {
            setError('Quantity must be a positive whole number.')
            return
        }

        if (parsedQuantity > selectedProduct.current_stock) {
            setError('Quantity cannot exceed the available stock.')
            return
        }

        const productAlreadyAdded = items.some(
            (item) => item.product.code === selectedProduct.code
        )

        if (productAlreadyAdded) {
            setError('This product is already in the sale.')
            return
        }

        setItems((currentItems) => [
            ...currentItems,
            {
                product: selectedProduct,
                quantity: parsedQuantity,
            },
        ])

        setError('')
        setProductCode('')
        setQuantity('')
    }

    function handleRemoveProduct(productCode: string) {
        setError('')

        setItems((currentItems) =>
            currentItems.filter(
                (item) => item.product.code !== productCode
            )
        )
    }

    async function handleSubmitSale() {
        if (!token || items.length === 0 || submitting) {
            return
        }

        setSubmitting(true)
        setError('')
        setSuccess('')

        try {
            await saleService.create(token, {
                items: items.map((item) => ({
                    product_code: item.product.code,
                    quantity: item.quantity,
                })),
            })

            setItems([])
            setProductCode('')
            setQuantity('')
            setSuccess('Sale registered successfully.')
            onSaleCreated()
        } catch (err) {
            if (axios.isAxiosError(err)) {
                const detail = err.response?.data?.detail

                setError(
                    typeof detail === 'string'
                        ? detail
                        : 'Could not register the sale.'
                )
            } else {
                setError('Could not register the sale.')
            }
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <h2 className="text-xl font-semibold text-white">
                Register new sale
            </h2>

            <p className="mt-2 text-sm text-slate-400">
                Select products and quantities to create a sale.
            </p>

            {success && (
                <div className="mt-4 rounded-lg border border-green-500/30 bg-green-500/10 px-4 py-3 text-sm text-green-400">
                    {success}
                </div>
            )}

            {error && (
                <div className="mt-4 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                    {error}
                </div>
            )}

            <div className="mt-6">
                <label
                    htmlFor="sale-product"
                    className="mb-2 block text-sm font-medium text-slate-300"
                >
                    Product
                </label>

                <select
                    id="sale-product"
                    value={productCode}
                    onChange={(event) => setProductCode(event.target.value)}
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white"
                >
                    <option value="">Choose a product</option>

                    {products.map((product) => (
                        <option key={product.code} value={product.code}>
                            {product.name} ({product.code}) - Stock: {product.current_stock}
                        </option>
                    ))}
                </select>
            </div>

            <div className="mt-4">
                <label
                    htmlFor="sale-quantity"
                    className="mb-2 block text-sm font-medium text-slate-300"
                >
                    Quantity
                </label>

                <input
                    id="sale-quantity"
                    type="number"
                    min="1"
                    step="1"
                    value={quantity}
                    onChange={(event) => setQuantity(event.target.value)}
                    placeholder="Enter quantity"
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white"
                />
            </div>

            {selectedProduct && (
                <div className="mt-4 rounded-lg border border-slate-700 bg-slate-950 p-4">
                    <p className="font-medium text-white">
                        {selectedProduct.name}
                    </p>

                    <p className="mt-2 text-sm text-slate-400">
                        Available stock: {selectedProduct.current_stock}
                    </p>

                    <p className="mt-2 text-sm text-slate-400">
                        Unit price:{' '}
                        {selectedProduct.price.toLocaleString('es-CO', {
                            style: 'currency',
                            currency: 'COP',
                        })}
                    </p>
                </div>
            )}

            <button
                type="button"
                onClick={handleAddProduct}
                className="mt-4 w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700"
            >
                Add product
            </button>

            {items.length > 0 && (
                <div className="mt-6">
                    <h3 className="text-lg font-semibold text-white">
                        Sale items
                    </h3>

                    <div className="mt-3 space-y-3">
                        {items.map((item) => (
                            <div
                                key={item.product.code}
                                className="flex items-center justify-between rounded-lg border border-slate-700 bg-slate-950 p-4"
                            >
                                <div>
                                    <p className="font-medium text-white">
                                        {item.product.name}
                                    </p>

                                    <p className="mt-1 text-sm text-slate-400">
                                        {item.quantity} ×{' '}
                                        {item.product.price.toLocaleString('es-CO', {
                                            style: 'currency',
                                            currency: 'COP',
                                        })}
                                    </p>
                                </div>

                                <div className="flex items-center gap-4">
                                    <p className="font-semibold text-white">
                                        {(item.product.price * item.quantity).toLocaleString(
                                            'es-CO',
                                            {
                                                style: 'currency',
                                                currency: 'COP',
                                            }
                                        )}
                                    </p>

                                    <button
                                        type="button"
                                        onClick={() => handleRemoveProduct(item.product.code)}
                                        className="rounded-lg border border-red-500/30 px-3 py-2 text-sm font-medium text-red-400 transition hover:bg-red-500/10"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="mt-4 flex items-center justify-between border-t border-slate-700 pt-4">
                        <span className="text-lg font-semibold text-slate-300">
                            Total
                        </span>

                        <span className="text-xl font-bold text-white">
                            {total.toLocaleString('es-CO', {
                                style: 'currency',
                                currency: 'COP',
                            })}
                        </span>
                    </div>

                    <button
                        type="button"
                        onClick={handleSubmitSale}
                        disabled={submitting}
                        className="mt-4 w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {submitting ? 'Registering sale...' : 'Register sale'}
                    </button>
                </div>
            )}
        </div>
    )
}