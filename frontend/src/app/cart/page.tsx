'use client'

import StripeProvider from '@/components/StripeProvider'
import { useCart } from '@/components/CartProvider'
import { useState } from 'react'
import Button from '@/components/Button'

export default function Cart() {
  const { items } = useCart()
  const cartItems = Object.values(items)
  const total = cartItems.reduce((sum, item) => sum + item.unitPrice * item.quantity, 0)

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [clientSecret, setClientSecret] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  async function handleCheckout() {
    setError(null)
    setIsLoading(true)

    const windowRes = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/preorder-window/current/`)
    const windows = await windowRes.json()
    if (!windows.length) {
      setError('No active preorder window. Check back soon!')
      setIsLoading(false)
      return
    }

    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/preorders/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        window: windows[0].id,
        customer_name: name,
        customer_email: email,
        total: total.toFixed(2),
        items: cartItems.map(item => ({
          product_listing: item.listingId,
          quantity: item.quantity
        }))
      })
    })

    const data = await res.json()
    if (!res.ok) {
      setError(data.error ?? 'Something went wrong. Please try again.')
      // setError(data.error ?? JSON.stringify(data))
      setIsLoading(false)
      return
    }

    setClientSecret(data.client_secret)
    setIsLoading(false)
  }

  return (
    <div className="flex flex-col min-h-screen bg-background my-8 font-sans">
      <div className="px-8 pt-12 pb-6">
        <h1 className="text-5xl font-bold font-serif text-dark-green tracking-wide">Cart</h1>
        <div className="mt-4 h-px w-full bg-dark-green opacity-25" />
      </div>
      <main className="flex w-full flex-col py-4 bg-background px-8 gap-8">
        <div className="flex flex-col gap-4 w-full max-w-sm">
          {cartItems.length === 0 ?
            <p className="text-dark-green">Your cart is empty.</p> :
            <>
              {cartItems.map((item) => (
                <div key={item.listingId} className="flex w-full justify-between">
                  <p className="text-md text-dark-green">{item.quantity}x {item.name}</p>
                  <p className="text-md text-dark-green font-bold">${(item.quantity * item.unitPrice).toFixed(2)}</p>
                </div>
              ))}
              <div className="flex w-full justify-between border-t border-dark-green pt-2">
                <p className="text-md text-dark-green font-semibold">Total</p>
                <p className="text-md text-dark-green font-bold">${total.toFixed(2)}</p>
              </div>
            </>
          }
        </div>

        {cartItems.length > 0 && !clientSecret && (
          <div className="flex flex-col gap-4 w-full max-w-sm">
            <input
              className="border border-dark-green rounded px-3 py-2 text-dark-green bg-background"
              placeholder="Name"
              value={name}
              onChange={e => setName(e.target.value)}
            />
            <input
              className="border border-dark-green rounded px-3 py-2 text-dark-green bg-background"
              placeholder="Email"
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
            {error && <p className="text-red-600 text-sm">{error}</p>}
            <Button
              onClick={handleCheckout}
              disabled={isLoading || !name || !email}
            >
              {isLoading ? 'Loading...' : 'Checkout'}
            </Button>
          </div>
        )}

        {clientSecret && <StripeProvider clientSecret={clientSecret} />}
      </main>
    </div>
  )
}
