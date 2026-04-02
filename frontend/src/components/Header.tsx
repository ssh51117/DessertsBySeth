import Image from "next/image"
import Link from "next/link"

export default function Header() {
    return (
    <header className="flex flex-col">
    <div className="flex items-center justify-between h-[60px] px-4 bg-background-50 font-sans dark:bg-grey">
        <div className="flex items-center gap-3">
            <Link href="/menu" className="font-semibold text-black">Menu</Link>
            <Link href="pop-ups" className="font-semibold text-black">Pop-ups</Link>
            <Link href="guinea-pigs" className="font-semibold text-black">Guinea Pigs</Link>
            <Link href="/cart" className="font-semibold text-black">Cart</Link>
            <Link href="/custom-orders" className="font-semibold text-black">Custom Orders</Link>
        </div>
        <Link href="/" className="absolute left-1/2 -translate-x-1/2 text-dark-green font-bold font-serif text-lg tracking-wide">
            Desserts By Seth
        </Link>

        <div className="flex items-center gap-3">
            <Link href="/about" className="font-semibold text-black">About</Link>
            <Image
                className="object"
                src="/Instagram_simple_icon.png"
                alt="Instagram icon"
                width={24}
                height={24}
                />
            </div>
        </div>
        <div className="h-px w-full bg-dark-green opacity-25" />
        </header>
    )
}