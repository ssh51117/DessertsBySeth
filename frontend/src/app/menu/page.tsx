import Image from "next/image";
import Button from "@/app/components/Button"

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-background my-8 font-sans">
      <div className="px-8 pt-12 pb-6">
        <h1 className="text-5xl font-bold font-serif text-dark-green tracking-wide">Menu</h1>
        <div className="mt-4 h-px w-full bg-dark-green opacity-25" />
      </div>
      <main className="flex w-full flex-col min-h-screen py-16 bg-background">
        
        <div className="grid grid-cols-2 gap-12 w-full items-start items-stretch gap-8 px-4 py-8 bg-background-50 font-sans">
          <div className="flex flex-col h-full items-center gap-4">
            <p className="text-2xl font-semibold text-dark-green">
              Mini Basque Cheesecake - $4
            </p>
            <Image
            className="object-cover drop-shadow-xl"
            src="/basque.png"
            alt="Image of Mini Basque Cheesecake"
            width={350}
            height={200}
            priority
            />
            <Button className="mt-auto my-4">
                Add to Cart
            </Button>
          </div>
          <div className="flex flex-col h-full items-center gap-4">
            <p className="text-2xl font-semibold text-dark-green">
              Rose Chocolate Chip Cookie - $3
            </p>
            <Image
            className="object-cover drop-shadow-md"
            src="/cookie.png"
            alt="Image of Rose CCC"
            width={350}
            height={200}
            priority
            />
            <Button className="mt-auto my-4">
                Add to Cart
            </Button>
          </div>

          <div className="flex flex-col h-full items-center gap-4">
            <p className="text-2xl font-semibold text-dark-green">
              Black Sesame Raspberry Tart - $5
            </p>
            <Image
            className="object-cover drop-shadow-md"
            src="/onesesametart.png"
            alt="Image of Black Sesame Tart"
            width={350}
            height={200}
            priority
            />
            <Button className="mt-auto my-4">
                Add to Cart
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}
