import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import CheckoutForm from './CheckoutForm'

const mockConfirmPayment = vi.fn()
const mockStripe = { confirmPayment: mockConfirmPayment }
const mockElements = {}

vi.mock('@stripe/react-stripe-js', () => ({
  PaymentElement: () => <div data-testid="payment-element" />,
  useStripe: vi.fn(),
  useElements: vi.fn(),
}))

import { useStripe, useElements } from '@stripe/react-stripe-js'

const mockUseStripe = vi.mocked(useStripe)
const mockUseElements = vi.mocked(useElements)

beforeEach(() => {
  mockUseStripe.mockReturnValue(mockStripe as never)
  mockUseElements.mockReturnValue(mockElements as never)
  mockConfirmPayment.mockReset()
})

describe('CheckoutForm', () => {
  it('renders the PaymentElement', () => {
    render(<CheckoutForm />)
    expect(screen.getByTestId('payment-element')).toBeInTheDocument()
  })

  it('pay button is disabled when stripe is null', () => {
    mockUseStripe.mockReturnValue(null)
    render(<CheckoutForm />)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('pay button is disabled when elements is null', () => {
    mockUseElements.mockReturnValue(null)
    render(<CheckoutForm />)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('pay button is enabled when both stripe and elements are loaded', () => {
    render(<CheckoutForm />)
    expect(screen.getByRole('button')).not.toBeDisabled()
  })

  it('shows card error message on card_error', async () => {
    mockConfirmPayment.mockResolvedValue({
      error: { type: 'card_error', message: 'Your card was declined.' },
    })
    render(<CheckoutForm />)
    await userEvent.click(screen.getByRole('button'))
    await waitFor(() =>
      expect(screen.getByText('Your card was declined.')).toBeInTheDocument()
    )
  })

  it('shows generic error message on non-card error', async () => {
    mockConfirmPayment.mockResolvedValue({
      error: { type: 'api_error', message: 'Something internal went wrong.' },
    })
    render(<CheckoutForm />)
    await userEvent.click(screen.getByRole('button'))
    await waitFor(() =>
      expect(screen.getByText('An unexpected error occured.')).toBeInTheDocument()
    )
  })

  it('re-enables the button after an error', async () => {
    mockConfirmPayment.mockResolvedValue({
      error: { type: 'card_error', message: 'Declined.' },
    })
    render(<CheckoutForm />)
    const button = screen.getByRole('button')
    await userEvent.click(button)
    await waitFor(() => expect(button).not.toBeDisabled())
  })
})
