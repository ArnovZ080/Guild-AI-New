import { useState, useEffect } from 'react';

const TOTAL_SPOTS = 50;
const FALLBACK_CLAIMED = 12;

export function useWaitlistStatus() {
    const [spotsClaimed, setSpotsClaimed] = useState(FALLBACK_CLAIMED);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchWaitlistStatus() {
            try {
                // Try to fetch dynamic waitlist count from API
                const res = await fetch('/api/waitlist/count');
                if (res.ok) {
                    const data = await res.json();
                    if (data && typeof data.count === 'number') {
                        setSpotsClaimed(data.count);
                    }
                }
            } catch (err) {
                // Silent fail to fallback if endpoint doesn't exist yet
                console.warn('Waitlist count API not available. Using fallback.');
            } finally {
                setLoading(false);
            }
        }

        fetchWaitlistStatus();
    }, []);

    return {
        totalSpots: TOTAL_SPOTS,
        spotsClaimed,
        spotsRemaining: Math.max(0, TOTAL_SPOTS - spotsClaimed),
        loading
    };
}
