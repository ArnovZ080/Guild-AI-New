import { useEffect, useRef } from 'react';

/**
 * Full-screen ambient particle canvas.
 * Renders behind all UI via z-index 0, with pointer-events: none.
 *
 * Particles drift slowly upward like embers rising from a forge.
 * Gentle horizontal sway, flickering opacity, and a warm glow halo.
 * Time-of-day colour shift creates an organic, living quality.
 *
 * Performance: ~60-70 particles on desktop, ~35 on mobile.
 * Uses requestAnimationFrame — no jank.
 */
export default function AmbientEmbers() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W = 0, H = 0;
    let animId;

    // ── Guild's nature-inspired ember palette ──
    const COLORS_DEFAULT = [
      '99, 102, 241',   // indigo (primary accent)
      '79, 121, 210',   // muted cobalt
      '16, 185, 129',   // forest green
      '99, 102, 241',   // indigo (weighted higher)
      '139, 92, 246',   // soft violet
      '180, 210, 240',  // pale sky
      '217, 119, 6',    // warm amber (sparse — like actual embers)
    ];

    const COLORS_MORNING = [
      '217, 119, 6',    // warm amber
      '217, 119, 6',    // amber (doubled)
      '99, 102, 241',   // indigo
      '180, 210, 240',  // pale sky
      '139, 92, 246',   // violet
    ];

    const COLORS_EVENING = [
      '99, 102, 241',   // indigo
      '99, 102, 241',   // indigo (doubled)
      '79, 121, 210',   // cobalt
      '139, 92, 246',   // violet
      '16, 185, 129',   // forest green (sparse)
    ];

    // ── Time-of-day colour weighting ──
    function getTimeWeightedPalette() {
      const hour = new Date().getHours();
      if (hour >= 6 && hour < 12) return COLORS_MORNING;
      if (hour >= 18 || hour < 6) return COLORS_EVENING;
      return COLORS_DEFAULT;
    }

    function pickColor() {
      const palette = getTimeWeightedPalette();
      return palette[Math.floor(Math.random() * palette.length)];
    }

    // ── Particle count: lighter on mobile ──
    const isMobile = window.innerWidth < 768;
    const PARTICLE_COUNT = isMobile ? 35 : 70;
    const particles = [];

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random(),
        y: Math.random(),
        vx: (Math.random() - 0.5) * 0.00015,
        vy: -(Math.random() * 0.00022 + 0.00006),
        r: Math.random() * 1.8 + 0.4,
        base: Math.random() * 0.5 + 0.2,
        t: Math.random() * Math.PI * 2,
        ts: Math.random() * 0.018 + 0.005,
        col: pickColor(),
        swayAmp: (Math.random() - 0.5) * 0.0001,
        swayFreq: Math.random() * 0.035 + 0.008,
        swayOff: Math.random() * Math.PI * 2,
      });
    }

    function resize() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }

    function draw() {
      ctx.clearRect(0, 0, W, H);

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        // Upward drift — wrap at top
        p.y += p.vy;
        if (p.y < -0.02) {
          p.y = 1.02;
          p.col = pickColor(); // re-roll colour on respawn
        }

        // Horizontal sway
        p.x += p.vx + Math.sin(p.t * p.swayFreq + p.swayOff) * p.swayAmp;
        p.x = ((p.x % 1) + 1) % 1;

        p.t += p.ts;

        // Flicker: opacity pulses
        const flicker = 0.3 + 0.7 * Math.abs(Math.sin(p.t));
        const a = p.base * flicker;

        const px = p.x * W;
        const py = p.y * H;

        // Outer glow halo
        const g = ctx.createRadialGradient(px, py, 0, px, py, p.r * 5);
        g.addColorStop(0, `rgba(${p.col}, ${a * 0.4})`);
        g.addColorStop(1, `rgba(${p.col}, 0)`);
        ctx.beginPath();
        ctx.arc(px, py, p.r * 5, 0, Math.PI * 2);
        ctx.fillStyle = g;
        ctx.fill();

        // Bright core
        ctx.beginPath();
        ctx.arc(px, py, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${p.col}, ${Math.min(a * 1.3, 1)})`;
        ctx.shadowColor = `rgba(${p.col}, 0.85)`;
        ctx.shadowBlur = 7;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      animId = requestAnimationFrame(draw);
    }

    resize();
    draw();
    window.addEventListener('resize', resize);

    return () => {
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(animId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 0,
        pointerEvents: 'none',
      }}
    />
  );
}
