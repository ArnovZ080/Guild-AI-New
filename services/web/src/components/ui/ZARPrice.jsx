import { useExchangeRate } from '../../hooks/useExchangeRate';

/**
 * Displays the ZAR equivalent beneath a USD price.
 *
 * Usage:
 *   <ZARPrice usd={149} />
 *   Renders: "≈ R2,765/mo" in smaller, muted text
 */
export default function ZARPrice({ usd, period = '/mo', className = '' }) {
  const { toZAR, loading } = useExchangeRate();

  if (loading || !toZAR(usd)) return null;

  return (
    <span className={`block text-sm text-zinc-500 font-normal mt-1 ${className}`}>
      ≈ {toZAR(usd)}{period}
    </span>
  );
}
