'use client'

import CheckoutForm from '@/components/CheckoutForm'
import {
    PaymentElement,
    useStripe,
    useElements,
    Elements
} from '@stripe/react-stripe-js'
import { loadStripe,Appearance } from '@stripe/stripe-js'

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!)

export default function StripeProvider({clientSecret}: {clientSecret: string}) {
    const appearance: Appearance = {
            theme: 'stripe',
            variables: {
                colorPrimary: 'var(--dark-green)',
                colorText: 'var(--cream)'
            }
        }
    return (
        <Elements stripe={stripePromise} options={{appearance, clientSecret}}>
            <CheckoutForm/>
        </Elements>
    )
}