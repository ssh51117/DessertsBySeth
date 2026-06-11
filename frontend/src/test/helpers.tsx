import { render, RenderOptions } from '@testing-library/react'
import CartProvider from '@/components/CartProvider'

export function renderWithCart(ui: React.ReactElement, options?: RenderOptions) {
  return render(ui, {
    wrapper: ({ children }) => <CartProvider>{children}</CartProvider>,
    ...options,
  })
}
