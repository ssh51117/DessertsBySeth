import Button from "@/components/Button"

// allow selection of delivery or pickup, with extra fee for delivery and instruction details
// delivery add location and mention that certains days work better
// add blurb at top that custom orders are fulfilled by availability require 2 weeks advance notice, and they will hear back in 2-3 business days
// delivery flat within 30 minutes of Midtown Atlanta, increasing rate further it goes

export default function CustomOrders() {
  return (
    <div className="flex flex-col min-h-screen bg-background my-8 font-sans">
      <div className="px-8 pt-12 pb-6">
        <h1 className="text-5xl font-bold font-serif text-dark-green tracking-wide">Custom Orders</h1>
        <div className="mt-4 h-px w-full bg-dark-green opacity-25" />
      </div>
      <main className="flex w-full flex-col min-h-screen py-16 bg-background items-center">
        <div className="grid grid-cols-1 gap-x-6 gap-y-8 w-1/2">
            <p className="text-dark-green font-semibold text-lg justify-left">
              Do you have a special occasion or want something off the menu? Submit a request here and I'll get back to you within 2-3 business days. You must submit your request at least 2 weeks before pickup date.
            </p>
            <div className="flex w-1/3 flex-col gap-y-2">
                <label htmlFor="username" className="block text-lg font-semibold text-dark-green"> Name</label>
                <input id="full_name" type="text" name="full_name" placeholder="Full Name" className="block box-border border-foreground border-2 min-w-0 grow bg-transparent py-1.5 pr-3 pl-1 text-base text-dark-green placeholder:text-gray-500 focus:outline-none"/>
            </div>
            <div className="flex w-1/2 flex-col gap-y-2">
                <label htmlFor="username" className="block text-lg font-semibold text-dark-green"> Email</label>
                <input id="full_name" type="email" name="full_name" placeholder="example@gmail.com" className="block box-border border-foreground border-2 min-w-0 grow bg-transparent py-1.5 pr-3 pl-1 text-base text-dark-green placeholder:text-gray-500 focus:outline-none"/>
            </div>
            <div className="flex w-full flex-col gap-y-2">
                <label htmlFor="username" className="block text-lg font-semibold text-dark-green"> Request</label>
                <textarea id="full_name" rows={3} name="full_name" placeholder="Request Details" className="block box-border w-md border-foreground border-2 min-w-0 grow bg-transparent py-1.5 pr-3 pl-1 text-base text-dark-green placeholder:text-gray-500 focus:outline-none"/>
            </div>
            <div className="flex w-1/3 flex-col gap-y-2">
                <label htmlFor="username" className="block text-lg font-semibold text-dark-green"> Pickup Time</label>
                <input id="full_name" type="date" name="full_name" placeholder="example@gmail.com" className="block box-border border-foreground border-2 min-w-0 grow bg-transparent py-1.5 pr-3 pl-1 text-base text-dark-green placeholder:text-gray-500 focus:outline-none"/>
                <input id="full_name" type="time" name="full_name" placeholder="example@gmail.com" className="block box-border border-foreground border-2 min-w-0 grow bg-transparent py-1.5 pr-3 pl-1 text-base text-dark-green placeholder:text-gray-500 focus:outline-none"/>
            </div>
            <div className="flex w-full flex-col gap-y-2">
                <label htmlFor="username" className="block text-lg font-semibold text-dark-green"> Delivery</label>
                <input id="full_name" type="text" name="full_name" placeholder="Delivery Details" className="block box-border border-foreground border-2 min-w-0 grow bg-transparent py-1.5 pr-3 pl-1 text-base text-dark-green placeholder:text-gray-500 focus:outline-none"/>
            </div>
            <Button className="mt-auto w-1/3 justify-self-center">
                Submit
            </Button>
        </div>
      </main>
    </div>
  );
}
