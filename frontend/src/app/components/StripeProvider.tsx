'use client'

import { CheckoutForm } from '@/app/components/CheckoutForm'
import {
    PaymentElement,
    useStripe,
    useElements,
    Elements
} from '@stripe/react-stripe-js'
import { loadStripe } from '@stripe/stripe-js'

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!)

export default function StripeProvider({clientSecret}) {
    const appearance = {
        theme: 'stripe',
    };
    return (
        <Elements stripe={stripePromise} options={{appearance, clientSecret}}>
            <CheckoutForm/>
        </Elements>
    )
}