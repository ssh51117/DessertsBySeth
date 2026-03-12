import Image from "next/image"
import Link from "next/link"

export default function Header() {
    return (
    <header className="flex items-center justify-between min-h-[60px] px-4 bg-background-50 font-sans dark:bg-grey">
        <div className="flex items-center gap-3">
            <Link href="/menu" className="font-semibold text-black">Menu</Link>
            <span className="font-semibold text-black">Custom Orders</span>
            <span className="font-semibold text-black">Pop-ups</span>
            <span className="font-semibold text-black">Guinea Pigs</span>
            <Link href="/cart" className="font-semibold text-black">Cart</Link>
        </div>
        <Link href="/" className="absolute left-1/2 -translate-x-1/2 text-dark-green font-bold">
            Desserts By Seth
        </Link>

        <div className="flex items-center gap-3">
            <span className="font-semibold text-black">About</span>
            <span className="font-semibold text-black">Contact</span>
            <Image
                className="object"
                src="/Instagram_simple_icon.png"
                alt="Instagram icon"
                width={24}
                height={24}
                />
            </div>
        </header>)
}