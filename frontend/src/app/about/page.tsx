import Image from "next/image";

export default function About() {
  return (
    <div className="flex flex-col min-h-screen bg-background my-8 font-sans">
      <div className="px-8 pt-12 pb-6">
        <h1 className="text-5xl font-bold font-serif text-dark-green tracking-wide">About</h1>
        <div className="mt-4 h-px w-full bg-dark-green opacity-25" />
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
                </div>
      </main>
    </div>
  );
}
