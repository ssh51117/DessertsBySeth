import Image from "next/image";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-background my-8 font-sans">
      <div className="px-8 pt-12 pb-6">
        <h1 className="text-5xl font-bold font-serif text-dark-green tracking-wide">Guinea Pigs</h1>
        <div className="mt-4 h-px w-full bg-dark-green opacity-25" />
      </div>
      <main className="flex w-full flex-col min-h-screen gap-4 bg-background px-8">
        Want to try more from me? Become a Guinea Pig and get dessert for free!

        Sometimes I also just make too much for one person, and I need to just get rid of it. Other times, I'm workshopping a dessert and need as much feedback as I can get.
        Either way, Guinea Pigs get desserts for free!
        <div className="flex w-full py-8 gap-16 bg-background">
          <Image
          className="object-cover"
          src="/milkbarcarrotcake.png"
          alt="carrot cake"
          width={200}
          height={200}
          />
          <Image
          className="object-cover"
          src="/milkbarcarrotcake.png"
          alt="carrot cake"
          width={200}
          height={200}
          />
        </div>
      </main>
    </div>
  );
}
