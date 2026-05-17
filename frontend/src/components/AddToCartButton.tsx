'use client'

import Button from "@/components/Button"
import { useCart } from "@/components/CartProvider"

type Props = {
  id: number
  name: string
  price: number
}

export default function AddToCartButton({ id, name, price }: Props) {
  const { items, setQuantity } = useCart()
  const item = items[id]
  const quantity = item?.quantity ?? 0

  if (quantity === 0) {
    return (
      <Button
        className="mt-auto my-4"
        onClick={() => setQuantity({ listingId: id, name, unitPrice: price, quantity: 1 }, 1)}
      >
        Add to Cart
      </Button>
    )
  }

  return (
    <div className="flex items-center gap-3 mt-auto my-4">
      <Button onClick={() => setQuantity(item, quantity - 1)}>−</Button>
      <span className="text-xl font-semibold text-dark-green">{quantity}</span>
      <Button onClick={() => setQuantity(item, quantity + 1)}>+</Button>
    </div>
  )
}
