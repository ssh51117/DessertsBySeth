'use client'

import { useState } from 'react';
import {
    PaymentElement,
    useStripe,
    useElements,
    Elements
} from '@stripe/react-stripe-js'

const stripe = useStripe();
const elements = useElements();

const [message, setMessage] = useState(null);
const [isLoading, setIsLoading] = useState(false);

export default function CheckoutForm() {
    return (
        
    )
}