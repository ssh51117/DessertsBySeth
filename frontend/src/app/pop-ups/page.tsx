
import Image from "next/image"

const pastPopUps = [
  {
    id: 1,
    date: "January 15, 2025",
    location: "Some Venue, City, ST",
    recap: "A wonderful evening of seasonal desserts. Guests enjoyed a variety of treats featuring winter flavors and locally sourced ingredients.",
    photos: ["/basque.png", "/cookie.png"],
  },
  {
    id: 2,
    date: "March 8, 2025",
    location: "Another Spot, City, ST",
    recap: "A spring-themed pop-up celebrating fresh flavors. It was a great turnout and we sold out within the first hour!",
    photos: ["/onesesametart.png"],
  },
];

export default function PopUps() {
  return (
    <div className="flex flex-col min-h-screen bg-background my-8 font-sans">
      <div className="px-8 pt-12 pb-6">
        <h1 className="text-5xl font-bold font-serif text-dark-green tracking-wide">Pop-ups</h1>
        <div className="mt-4 h-px w-full bg-dark-green opacity-25" />
      </div>
      <main className="flex w-full flex-col min-h-screen py-16 bg-background items-center">
        <div className="w-full px-8 mb-6">
          <h2 className="text-3xl font-bold font-serif text-dark-green tracking-wide">Future Pop-Ups</h2>
          <div className="mt-3 h-px w-full bg-dark-green opacity-25" />
        </div>
        <p className="px-8 pb-10 text-left w-full">Nothing planned at the moment! Please check back later, or contact me here if you want to set up a pop-up!</p>
        <div className="w-full px-8 mb-6">
          <h2 className="text-3xl font-bold font-serif text-dark-green tracking-wide">Past Pop-Ups</h2>
          <div className="mt-3 h-px w-full bg-dark-green opacity-25" />
        </div>
        <div className="flex flex-col gap-12 w-3/4 max-w-3xl py-12">
          {pastPopUps.map((popup) => (
            <div key={popup.id} className="flex flex-col gap-4 bg-background-50 p-6 rounded-lg shadow-md">
              <div className="flex flex-col gap-1">
                <p className="text-xl font-semibold text-dark-green">{popup.date}</p>
                <p className="text-md text-dark-green opacity-75">{popup.location}</p>
              </div>
              <p className="text-dark-green">{popup.recap}</p>
              <div className="flex flex-row gap-4 flex-wrap">
                {popup.photos.map((photo, i) => (
                  <Image
                    key={i}
                    src={photo}
                    alt={`Photo from ${popup.date} pop-up`}
                    width={280}
                    height={200}
                    className="object-cover rounded-md drop-shadow-md"
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
