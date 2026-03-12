import { ReactNode, ButtonHTMLAttributes} from "react";

const variants = {
    primary: "bg-dark-green text-cream hover:bg-dark-green/80",
    secondary: "bg-light-green text-cream hover:bg-light-green/80",
  };

type ButtonProps = {
    children: ReactNode;
    variant?: keyof typeof variants;
} & ButtonHTMLAttributes<HTMLButtonElement>;

export default function Button({ children, variant = "primary", className="", ...props}: ButtonProps) {
  const styles = "px-4 py-2 rounded-md text-xl font-semibold transition-all";

  return (
    <button
        {...props}
        className={`${styles} ${variants[variant]} ${className}`}>
      {children}
    </button>
  );
}
