import { describe, it, expect } from 'vitest'
import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import AddToCartButton from './AddToCartButton'
import { renderWithCart } from '@/test/helpers'

const defaultProps = { id: 1, name: 'Chocolate Cake', price: 12 }

describe('AddToCartButton', () => {
  it('shows "Add to Cart" when item is not in cart', () => {
    renderWithCart(<AddToCartButton {...defaultProps} />)
    expect(screen.getByText('Add to Cart')).toBeInTheDocument()
  })

  it('clicking "Add to Cart" adds item and shows quantity controls', async () => {
    renderWithCart(<AddToCartButton {...defaultProps} />)
    await userEvent.click(screen.getByText('Add to Cart'))
    expect(screen.queryByText('Add to Cart')).not.toBeInTheDocument()
    expect(screen.getByText('1')).toBeInTheDocument()
    expect(screen.getByText('+')).toBeInTheDocument()
    expect(screen.getByText('−')).toBeInTheDocument()
  })

  it('"+" increments quantity', async () => {
    renderWithCart(<AddToCartButton {...defaultProps} />)
    await userEvent.click(screen.getByText('Add to Cart'))
    await userEvent.click(screen.getByText('+'))
    expect(screen.getByText('2')).toBeInTheDocument()
  })

  it('"−" decrements quantity', async () => {
    renderWithCart(<AddToCartButton {...defaultProps} />)
    await userEvent.click(screen.getByText('Add to Cart'))
    await userEvent.click(screen.getByText('+'))
    await userEvent.click(screen.getByText('−'))
    expect(screen.getByText('1')).toBeInTheDocument()
  })

  it('"−" at quantity 1 removes item and returns to "Add to Cart"', async () => {
    renderWithCart(<AddToCartButton {...defaultProps} />)
    await userEvent.click(screen.getByText('Add to Cart'))
    await userEvent.click(screen.getByText('−'))
    expect(screen.getByText('Add to Cart')).toBeInTheDocument()
  })
})
