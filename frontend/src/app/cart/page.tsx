const cartItems = [
  {
    id: 1,
    name: "Rose Chocolate Chip Cookie",
    price: 3,
    count: 2
  },
  {
    id: 2,
    name: "Basque Cheesecake",
    price: 4,
    count: 1
  }
]
export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-background my-8 font-sans">
      <div className="px-8 pt-12 pb-6">
        <h1 className="text-5xl font-bold font-serif text-dark-green tracking-wide">Cart</h1>
        <div className="mt-4 h-px w-full bg-dark-green opacity-25" />
      </div>
      <main className="flex w-full flex-col min-h-screen py-4 bg-background">
        <div className="flex flex-col gap-4 w-1/4 max-w-3xl px-8 py-4">
          {cartItems.map((item) => (
            <div className="flex w-full justify-between">
              <p className="text-md text-dark-green justify-left">{item.count}x {item.name}</p>
              <p className="text-md text-dark-green font-bold justify-right">${item.price}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
