import { redirect } from 'next/navigation'
import { stripe } from '@/lib/stripe'
import Link from 'next/link'

  const STATUS_MAP = {
      succeeded: {
          text: "Order confirmed! We'll see you at pickup.",
          bgColor: "bg-dark-green",
          icon: "✓"
      },
      processing: {
          text: "Your payment is processing.",
          bgColor: "bg-gray-500",
          icon: "i"
      },
      requires_payment_method: {
          text: "Payment unsuccessful — please try again.",
          bgColor: "bg-red-600",
          icon: "✕"
      },
      default: {
          text: "Something went wrong — please try again.",
          bgColor: "bg-red-600",
          icon: "✕"
      }
  }

  export default async function SuccessPage({ searchParams }: { searchParams: Promise<{ payment_intent?: string }> }) {
      const { payment_intent: paymentIntentId } = await searchParams

      if (!paymentIntentId) redirect('/')

      const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId)

      if (!paymentIntent) redirect('/')

      const status = paymentIntent.status as keyof typeof STATUS_MAP
      const content = STATUS_MAP[status] ?? STATUS_MAP.default

      return (
          <div className="flex flex-col min-h-screen bg-background font-sans items-center justify-center gap-6">
              <div className={`${content.bgColor} rounded-full w-12 h-12 flex items-center justify-center text-cream text-xl font-bold`}>
                  {content.icon}
              </div>
              <h1 className="text-3xl font-bold font-serif text-dark-green">{content.text}</h1>
              <div className="text-sm text-gray-500">
                  <p>Order ID: {paymentIntent.metadata.order_id}</p>
                  <p>Status: {status}</p>
              </div>
              <Link href="/menu" className="mt-4 py-2 px-6 bg-dark-green text-cream rounded font-semibold">
                  Place another order
              </Link>
          </div>
      )
  }