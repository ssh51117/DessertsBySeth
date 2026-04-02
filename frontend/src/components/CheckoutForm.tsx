'use client'

import { useState } from 'react';
import {
    PaymentElement,
    useStripe,
    useElements,
} from '@stripe/react-stripe-js'

const paymentElementOptions = {
    layout: "accordion" as const
}

export default function CheckoutForm() {
    const stripe = useStripe();
    const elements = useElements();

    const [message, setMessage] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.SubmitEvent) => {
        e.preventDefault();

        if (!stripe || !elements) {
            // Stripe.js hasn't loaded, disable form submission
            return;
        }

        setIsLoading(true);
    
        const {error} = await stripe.confirmPayment({
            elements,
            confirmParams: {
                // payment completion page
                return_url: "http://localhost:3000/success"
            },
        });

        // only reached if there is an immediate error when confirming payment
        if (error.type === "card_error" || error.type === "validation_error") {
            setMessage(error.message ?? "An unexpected error occured.");
        } else {
            setMessage("An unexpected error occured.")
        }

        setIsLoading(false);
    }

    return (
        <form onSubmit = {handleSubmit}>
            <PaymentElement options={paymentElementOptions}/>
            <button disabled={isLoading || !stripe || !elements}
                    className="w-full mt-4 py-2 px-4 bg-dark-green text-cream rounded disabled:opacity-50">
                <span>
                    {isLoading ? <span className="inline-block w-4 h-4 border-2 border-cream border-t-transparent rounded-full animate-spin"/> : "Pay now"}
                </span>
            </button>
            {message && <div className="mt-2 text-sm text-red-600">{message}</div>}
        </form>
    );
}