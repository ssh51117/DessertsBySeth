'use client'

import { createContext, useContext, useState } from 'react'

type CartItem = {
    listingId: number
    name: string
    unitPrice: number
    quantity: number
}

type CartState = {
    items: Record<number, CartItem>
    setQuantity: (item: CartItem, quantity: number) => void
    clear: () => void
}

export const CartContext = createContext<CartState | null>(null)

export function useCart() {
    const context = useContext(CartContext)
    if (!context) throw new Error('useCart must be used within CartProvider')
        return context
}

export default function CartProvider({children}: {children: React.ReactNode}) {
    const [items, setItems] = useState<Record<number, CartItem>>({})

    function setQuantity(item: CartItem, quantity: number) {
        if (quantity <= 0) {
            setItems(prev => {
                const next = {...prev}
                delete next[item.listingId]
                return next
            })
        } else {
            setItems(prev => ({
                ...prev,
                [item.listingId]: { ...item, quantity }
            }))
        }
    }

    function clear() {
        setItems({})
    }

    return (
        <CartContext.Provider value={{items, setQuantity, clear}}>
            {children}
        </CartContext.Provider>
    )
}