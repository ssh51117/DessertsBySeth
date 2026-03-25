import Image from "next/image";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-background font-sans">
        <div className="relative w-full h-[400px]">
        <Image
          className="object-cover"
          src="/croissants.jpg"
          alt="Image of Croissants"
          fill
          priority
        />
        
        <div className="absolute inset-0 flex items-center justify-center text-cream text-6xl font-bold font-serif tracking-wide drop-shadow-lg">
          Desserts By Seth
        </div>
      </div>
      <main className="flex w-full flex-col min-h-screen py-16 bg-background">
        <div className="flex w-full justify-between gap-8 bg-dark-green font-sans">
          <div className="flex w-1/2 gap-4 py-4 px-4 ">
            
              <Image
            className="object-cover"
            src="/me.JPG"
            alt="me!"
            width={200}
            height={200}
            />
            <div className="flex flex-col">
            <h1 className="max-w text-2xl font-semibold leading-10 tracking-tight text-cream font-serif">
              About
            </h1>
            <p className="text-cream font-semibold text-lg justify-left">
              Desserts By Seth is a home bakery ran out of my apartment in West Midtown Atlanta creating desserts that make me (and hopefuly you) happy.
            </p>
            <p className="text-cream mt-4 font-semibold text-sm justify-left">
              I'm also a computer science student at Georgia Tech, so sometimes I get busy and can't bake as either of us want me to.
              If you want me to bake more, keep buying from me and help me drop out!
            </p>
            <p className="text-cream font-semibold text-sm justify-left">
              (If you're a recruiter reading this I was kidding about dropping out, feel free to reach out and give me a job)
            </p>
            </div>
          </div>
          <div className="flex flex-col gap-4 py-4 px-4">
            <h1 className="max-w text-2xl font-semibold leading-10 tracking-tight text-cream font-serif">
              Schedule
            </h1>
            <p className="text-cream text-xs font-semibold">Please note that availability may change on a week to week basis</p>
            <p className="text-cream font-semibold text-lg">Monday 6-8pm: Pickup at Tech Green</p>
            <p className="text-cream font-semibold text-lg">Monday Evening: Preorders open for the next week</p>
            <p className="text-cream font-semibold text-lg">Thursday Evening: Preorders Due for following Monday</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-12 w-full items-start gap-8 px-4 py-8 bg-background-50 font-sans">
          <div className="flex flex-col items-center gap-4">
            <p className="text-2xl font-semibold text-dark-green font-serif">
              Menu
            </p>
            <p className="font-semibold text-dark-green">
              View the menu and place your order!
            </p>
            <Image
            className="object-cover"
            src="/basque.png"
            alt="Mini Basque Cheesecake"
            width={350}
            height={200}
            priority
            />
          </div>
          <div className="flex flex-col items-center gap-4">
            <p className="text-2xl font-semibold text-dark-green font-serif">
              Custom Orders
            </p>
            <p className="font-semibold text-dark-green">
              Have a custom request?
            </p>
            <Image
            className="object-cover"
            src="/milkbarcoffeecake.png"
            alt="Image of Croissants"
            width={350}
            height={200}
            priority
            />
          </div>

          <div className="flex flex-col items-center gap-4">
            <p className="text-2xl font-semibold text-dark-green font-serif">
              Pop-ups
            </p>
            <p className="font-semibold text-dark-green">
              Check out if Desserts By Seth will be anywhere special!
            </p>
            <Image
            className="object-cover"
            src="/strawberrytart.png"
            alt="Image of Strawberry Tarts"
            width={350}
            height={200}
            priority
            />
          </div>

          <div className="flex flex-col items-center gap-4">
            <p className="text-2xl font-semibold text-dark-green font-serif">
              Guinea Pigs
            </p>
            <p className="font-semibold text-dark-green">
              Only for the brave
            </p>
            <Image
            className="object-cover"
            src="/almond_croissant3.png"
            alt="Image of an Almond Croissant"
            width={350}
            height={200}
            priority
            />
          </div>
        </div>
      </main>
    </div>
  );
}
