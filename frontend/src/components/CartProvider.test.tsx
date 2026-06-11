import { describe, it, expect } from 'vitest'
import { render, screen, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import CartProvider, { useCart } from './CartProvider'

function CartDisplay() {
  const { items } = useCart()
  const keys = Object.keys(items)
  return (
    <div>
      <span data-testid="count">{keys.length}</span>
      {keys.map(k => (
        <span key={k} data-testid={`item-${k}`}>
          {items[Number(k)].name}:{items[Number(k)].quantity}
        </span>
      ))}
    </div>
  )
}

function CartActions() {
  const { setQuantity, clear } = useCart()
  return (
    <>
      <button onClick={() => setQuantity({ listingId: 1, name: 'Cake', unitPrice: 10, quantity: 1 }, 1)}>
        add-1
      </button>
      <button onClick={() => setQuantity({ listingId: 1, name: 'Cake', unitPrice: 10, quantity: 2 }, 2)}>
        update-1
      </button>
      <button onClick={() => setQuantity({ listingId: 1, name: 'Cake', unitPrice: 10, quantity: 1 }, 0)}>
        remove-1
      </button>
      <button onClick={() => setQuantity({ listingId: 2, name: 'Pie', unitPrice: 8, quantity: 1 }, 1)}>
        add-2
      </button>
      <button onClick={clear}>clear</button>
    </>
  )
}

function WrappedCart() {
  return (
    <CartProvider>
      <CartDisplay />
      <CartActions />
    </CartProvider>
  )
}

function OutsideCart() {
  useCart()
  return null
}

describe('CartProvider', () => {
  it('throws when useCart is used outside CartProvider', () => {
    const err = console.error
    console.error = () => {}
    expect(() => render(<OutsideCart />)).toThrow('useCart must be used within CartProvider')
    console.error = err
  })

  it('starts with an empty cart', () => {
    render(<WrappedCart />)
    expect(screen.getByTestId('count').textContent).toBe('0')
  })

  it('setQuantity adds a new item', async () => {
    render(<WrappedCart />)
    await userEvent.click(screen.getByText('add-1'))
    expect(screen.getByTestId('count').textContent).toBe('1')
    expect(screen.getByTestId('item-1').textContent).toBe('Cake:1')
  })

  it('setQuantity updates quantity of existing item', async () => {
    render(<WrappedCart />)
    await userEvent.click(screen.getByText('add-1'))
    await userEvent.click(screen.getByText('update-1'))
    expect(screen.getByTestId('item-1').textContent).toBe('Cake:2')
    expect(screen.getByTestId('count').textContent).toBe('1')
  })

  it('setQuantity with quantity 0 removes the item', async () => {
    render(<WrappedCart />)
    await userEvent.click(screen.getByText('add-1'))
    await userEvent.click(screen.getByText('remove-1'))
    expect(screen.getByTestId('count').textContent).toBe('0')
  })

  it('clear empties all items', async () => {
    render(<WrappedCart />)
    await userEvent.click(screen.getByText('add-1'))
    await userEvent.click(screen.getByText('add-2'))
    expect(screen.getByTestId('count').textContent).toBe('2')
    await userEvent.click(screen.getByText('clear'))
    expect(screen.getByTestId('count').textContent).toBe('0')
  })

  it('modifying one item does not affect others', async () => {
    render(<WrappedCart />)
    await userEvent.click(screen.getByText('add-1'))
    await userEvent.click(screen.getByText('add-2'))
    await userEvent.click(screen.getByText('update-1'))
    expect(screen.getByTestId('item-1').textContent).toBe('Cake:2')
    expect(screen.getByTestId('item-2').textContent).toBe('Pie:1')
  })
})
