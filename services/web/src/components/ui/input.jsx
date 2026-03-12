import * as React from "react"
import { cn } from "@/lib/utils"

const Input = React.forwardRef(({ className, type, ...props }, ref) => {
    return (
        <input
            type={type}
            className={cn(
                "flex h-10 w-full rounded-lg border border-white/5 bg-white/5 px-4 py-2 text-sm text-zinc-300 ring-offset-transparent placeholder:text-zinc-600 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-cobalt/40 focus-visible:border-cobalt/30 disabled:cursor-not-allowed disabled:opacity-50 transition-all",
                className
            )}
            ref={ref}
            {...props}
        />
    )
})
Input.displayName = "Input"

export { Input }
