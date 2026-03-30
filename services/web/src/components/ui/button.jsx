import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/30 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 cursor-pointer",
    {
        variants: {
            variant: {
                default:
                    "bg-gradient-to-b from-blue-500 to-blue-600 text-white shadow-md shadow-blue-500/20 hover:from-blue-600 hover:to-blue-700 hover:shadow-lg hover:shadow-blue-600/25 active:scale-[0.98]",
                destructive:
                    "bg-red-50 text-red-700 border border-red-200/60 hover:bg-red-100 dark:bg-red-500/10 dark:text-red-400 dark:border-red-500/20 dark:hover:bg-red-500/20",
                outline:
                    "border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 hover:text-gray-900 dark:border-white/10 dark:bg-transparent dark:text-zinc-400 dark:hover:bg-white/5 dark:hover:text-zinc-200",
                secondary:
                    "bg-gray-100 text-gray-700 border border-gray-200/60 hover:bg-gray-200/80 hover:text-gray-900 dark:bg-white/5 dark:text-zinc-400 dark:border-white/5 dark:hover:bg-white/8 dark:hover:text-zinc-200",
                ghost:
                    "text-gray-600 hover:bg-gray-100 hover:text-gray-900 dark:text-zinc-500 dark:hover:bg-white/5 dark:hover:text-zinc-300",
                link: "text-blue-600 dark:text-blue-400 underline-offset-4 hover:underline",
            },
            size: {
                default: "h-10 px-5 py-2",
                sm: "h-9 rounded-lg px-3.5 text-xs",
                lg: "h-12 rounded-xl px-8 text-base",
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
