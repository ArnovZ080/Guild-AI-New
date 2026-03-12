import * as React from "react"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
    "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors",
    {
        variants: {
            variant: {
                default:
                    "bg-blue-500/10 text-blue-400 border border-blue-500/20",
                secondary:
                    "bg-white/5 text-zinc-500 border border-white/5",
                destructive:
                    "bg-red-500/10 text-red-400 border border-red-500/20",
                outline:
                    "text-zinc-500 border border-white/5",
                success:
                    "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20",
                warning:
                    "bg-amber-500/10 text-amber-400 border border-amber-500/20",
                intelligence:
                    "bg-blue-500/10 text-blue-400 border border-blue-500/20",
            },
        },
        defaultVariants: {
            variant: "default",
        },
    }
)

function Badge({ className, variant, ...props }) {
    return (
        <div className={cn(badgeVariants({ variant }), className)} {...props} />
    )
}

export { Badge, badgeVariants }
