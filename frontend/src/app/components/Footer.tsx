export default function Footer() {
    return (
    <footer className="flex items-start pt-8 justify-between min-h-[300px] px-8 bg-background-50 font-sans">
        <div className="flex gap-8">
            <div className="flex flex-col gap-3">
                <span className="font-semibold text-black">Hours</span>
                <p className="text-black">Pickup every Monday between 6-8pm </p>
                <span className="font-semibold text-black">Location</span>
                <p className="text-black">Baking at 401 16th St NW</p>
                <p className="text-black">Pickup at Tech Green</p>
            </div>
        </div>
        
        <div className="flex flex-col gap-3 items-center">
            <div className="text-dark-green text-2xl font-bold font-serif tracking-wide">
            Desserts By Seth
            </div>
            <p className="text-black">A home bakery </p>
        </div>

         <div className="flex gap-8">
            <div className="flex flex-col gap-3">
                <span className="font-semibold text-black">Contact</span>
                <p className="text-black">Questions, comments, or just want to say hi?</p>
                <p className="text-black">Email me at sshi51117@gmail.com</p>
            </div>
        </div>
        </footer>)
}