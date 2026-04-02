import Image from "next/image";
import Button from "@/components/Button"

interface Product {
  name: string
  description: string
  price: string
  image: string
}

export default async function Menu() {
  const res = await fetch(`${process.env.BACKEND_URL}/products/`, {
    cache: "no-store"
  })
  const products: Product[] = await res.json()

  return (
    <div className="flex flex-col min-h-screen bg-background my-8 font-sans">
      <div className="px-8 pt-12 pb-6">
        <h1 className="text-5xl font-bold font-serif text-dark-green tracking-wide">Menu</h1>
        <div className="mt-4 h-px w-full bg-dark-green opacity-25" />
      </div>
      <main className="flex w-full flex-col min-h-screen py-16 bg-background">
        
        <div className="grid grid-cols-2 gap-12 w-full items-start items-stretch gap-8 px-4 py-8 bg-background-50 font-sans">
          {products.map((product) => (
            <div key={product.name} className="flex flex-col h-full items-center gap-4">
              <p className="text-2xl font-semibold text-dark-green">
                {product.name} - ${product.price}
              </p>
              <p className="text-lg text-black w-1/2">
                {product.description}
              </p>
            <Image
            className="object-cover drop-shadow-xl"
            src={product.image}
            alt={`Image of ${product.name}`}
            width={350}
            height={200}
            priority
            />
            <Button className="mt-auto my-4">
                Add to Cart
            </Button>
          </div>
            ))}
        </div>
      </main>
    </div>
  );
}
