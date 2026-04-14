import { useState, useEffect } from 'react';

/**
 * Fetches the current USD → ZAR exchange rate.
 * Uses a free public API. Caches the rate for 1 hour.
 * Falls back to a reasonable estimate if the API fails.
 */

const CACHE_KEY = 'guild_exchange_rate';
const CACHE_DURATION = 60 * 60 * 1000; // 1 hour
const FALLBACK_RATE = 18.5;

export function useExchangeRate() {
  const [rate, setRate] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchRate() {
      // Check cache first
      try {
        const cached = localStorage.getItem(CACHE_KEY);
        if (cached) {
          const { rate: cachedRate, timestamp } = JSON.parse(cached);
          if (Date.now() - timestamp < CACHE_DURATION) {
            setRate(cachedRate);
            setLoading(false);
            return;
          }
        }
      } catch (e) {
        // Cache read failed — continue to fetch
      }

      // Fetch live rate
      try {
        const response = await fetch(
          'https://api.exchangerate-api.com/v4/latest/USD'
        );
        const data = await response.json();
        const zarRate = data.rates?.ZAR;

        if (zarRate) {
          setRate(zarRate);
          try {
            localStorage.setItem(CACHE_KEY, JSON.stringify({
              rate: zarRate,
              timestamp: Date.now(),
            }));
          } catch (e) {
            // localStorage not available
          }
        } else {
          setRate(FALLBACK_RATE);
        }
      } catch (error) {
        console.warn('Exchange rate fetch failed, using fallback:', error);
        setRate(FALLBACK_RATE);
      }

      setLoading(false);
    }

    fetchRate();
  }, []);

  /**
   * Convert a USD amount to ZAR.
   * Returns formatted string like "R2,765"
   */
  function toZAR(usdAmount) {
    if (!rate) return null;
    const zarAmount = Math.round(usdAmount * rate);
    return `R${zarAmount.toLocaleString('en-ZA')}`;
  }

  return { rate, loading, toZAR };
}
