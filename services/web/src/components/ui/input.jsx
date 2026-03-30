import * as React from "react"
import { cn } from "@/lib/utils"

const Input = React.forwardRef(({ className, type, ...props }, ref) => {
    return (
        <input
            type={type}
            className={cn(
                "flex h-10 w-full rounded-xl border border-gray-200 bg-white px-4 py-2 text-sm text-gray-900 ring-offset-white placeholder:text-gray-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/30 focus-visible:border-blue-300 disabled:cursor-not-allowed disabled:opacity-50 transition-all dark:border-white/10 dark:bg-white/5 dark:text-zinc-200 dark:ring-offset-transparent dark:placeholder:text-zinc-600 dark:focus-visible:border-blue-500/40",
                className
            )}
            ref={ref}
            {...props}
        />
    )
})
Input.displayName = "Input"

export { Input }
