// Shared Framer Motion variants — Modern Dark Cinema spring system
// All transitions use cubic-bezier(0.16, 1, 0.3, 1) — the "expo out" spring feel

const SPRING = { ease: [0.16, 1, 0.3, 1], duration: 0.7 };
const SPRING_FAST = { ease: [0.16, 1, 0.3, 1], duration: 0.45 };
const SPRING_SLOW = { ease: [0.16, 1, 0.3, 1], duration: 1.0 };

// Respects prefers-reduced-motion
const reducedMotion = typeof window !== 'undefined'
  ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
  : false;

const noMotion = { opacity: [0, 1], transition: { duration: 0.01 } };

export const fadeUp = reducedMotion ? noMotion : {
  hidden:  { opacity: 0, y: 32 },
  visible: { opacity: 1, y: 0, transition: SPRING },
};

export const fadeDown = reducedMotion ? noMotion : {
  hidden:  { opacity: 0, y: -24 },
  visible: { opacity: 1, y: 0, transition: SPRING },
};

export const fadeIn = reducedMotion ? noMotion : {
  hidden:  { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
};

export const scaleIn = reducedMotion ? noMotion : {
  hidden:  { opacity: 0, scale: 0.92 },
  visible: { opacity: 1, scale: 1, transition: SPRING },
};

export const scaleInBounce = reducedMotion ? noMotion : {
  hidden:  { opacity: 0, scale: 0.8 },
  visible: { opacity: 1, scale: 1, transition: { ...SPRING_FAST, type: 'spring', stiffness: 300, damping: 20 } },
};

export const slideInLeft = reducedMotion ? noMotion : {
  hidden:  { opacity: 0, x: -48 },
  visible: { opacity: 1, x: 0, transition: SPRING },
};

export const slideInRight = reducedMotion ? noMotion : {
  hidden:  { opacity: 0, x: 48 },
  visible: { opacity: 1, x: 0, transition: SPRING },
};

// Container that staggers its children
export const staggerContainer = {
  hidden:  {},
  visible: {
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

export const staggerContainerFast = {
  hidden:  {},
  visible: {
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.05,
    },
  },
};

// Shared viewport config for whileInView
export const viewportOnce = { once: true, margin: '-80px' };

// Convenience: inline transition prop for simple one-off animations
export const springTransition = SPRING;
export const springFastTransition = SPRING_FAST;
export const springSlowTransition = SPRING_SLOW;
