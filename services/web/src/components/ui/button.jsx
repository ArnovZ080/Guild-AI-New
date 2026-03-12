import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-cobalt/40 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0",
    {
        variants: {
            variant: {
                default:
                    "bg-[#1a6fff] text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.2)] hover:bg-[#4d8fff] rounded-md",
                destructive:
                    "bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20",
                outline:
                    "border border-white/5 bg-transparent hover:bg-white/5 hover:border-white/5 text-zinc-400 hover:text-zinc-200",
                secondary:
                    "bg-white/5 text-zinc-400 border border-white/5 hover:bg-white/8 hover:text-zinc-200",
                ghost: "hover:bg-white/5 text-zinc-500 hover:text-zinc-300",
                link: "text-cobalt underline-offset-4 hover:underline",
            },
            size: {
                default: "h-10 px-4 py-2",
                sm: "h-9 rounded-md px-3",
                lg: "h-11 rounded-md px-8",
                icon: "h-10 w-10",
            },
        },
        defaultVariants: {
            variant: "default",
            size: "default",
        },
    }
)

const Button = React.forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
        <Comp
            className={cn(buttonVariants({ variant, size, className }))}
            ref={ref}
            {...props}
        />
    )
})
Button.displayName = "Button"

export { Button, buttonVariants }
