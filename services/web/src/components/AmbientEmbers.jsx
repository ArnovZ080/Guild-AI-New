import { useEffect, useRef } from 'react';

/**
 * AmbientEmbers — Crucible Mode
 *
 * Embers rise from an invisible heat source at the bottom-centre of the screen,
 * fanning outward as they climb. Mouse parallax drifts particles 4px toward cursor.
 * Amber burst on load settles into the ambient palette after ~2s.
 */
export default function AmbientEmbers() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W = 0, H = 0;
    let animId;
    let mouseX = 0.5, mouseY = 0.5; // normalised
    const startTime = performance.now();

    // ── Palette — logo colours: blue, light blue, white, yellow, touch of orange ──
    const PALETTE_AMBIENT = [
      '59, 130, 246',    // blue (primary — logo blue)
      '59, 130, 246',    // blue (weighted)
      '96, 165, 250',    // light blue
      '147, 197, 253',   // pale/icy blue
      '219, 234, 254',   // near-white blue
      '250, 204, 21',    // yellow (logo yellow)
      '253, 186, 116',   // light orange / amber (sparse)
    ];

    const PALETTE_BURST = [
      '250, 204, 21',    // yellow burst
      '250, 204, 21',    // yellow (weighted)
      '253, 186, 116',   // orange
      '249, 115, 22',    // deeper orange
      '59, 130, 246',    // blue
      '147, 197, 253',   // light blue
    ];

    function getPalette(age) {
      // First 2s: burst palette, then fade to ambient
      return age < 2000 ? PALETTE_BURST : PALETTE_AMBIENT;
    }

    function pickColor(age) {
      const palette = getPalette(age);
      return palette[Math.floor(Math.random() * palette.length)];
    }

    const isMobile = window.innerWidth < 768;
    const COUNT = isMobile ? 45 : 85;
    const particles = [];

    function makeParticle(forceAmber = false) {
      // Crucible source: bottom-centre with horizontal spread that grows with height
      const xBase = 0.5 + (Math.random() - 0.5) * 0.12; // tight at birth
      return {
        x: xBase,
        y: 1.02 + Math.random() * 0.05,
        xBase,                                    // reference for fan-out calc
        vx: (Math.random() - 0.5) * 0.00025,
        vy: -(Math.random() * 0.00055 + 0.00018),
        r: Math.random() * 2.2 + 0.6,
        base: Math.random() * 0.55 + 0.35,
        t: Math.random() * Math.PI * 2,
        ts: Math.random() * 0.035 + 0.012,
        col: forceAmber ? '245, 158, 11' : pickColor(0),
        swayAmp: (Math.random() - 0.5) * 0.00022,
        swayFreq: Math.random() * 0.08 + 0.02,
        swayOff: Math.random() * Math.PI * 2,
        parallaxFactor: Math.random() * 0.006 + 0.002, // how much it reacts to mouse
      };
    }

    // Seed initial particles spread across screen
    for (let i = 0; i < COUNT; i++) {
      const p = makeParticle(false);
      p.y = Math.random(); // scatter vertically on init
      p.col = pickColor(9999); // ambient palette on init
      particles.push(p);
    }
    // Add a burst of amber particles on top
    for (let i = 0; i < 15; i++) {
      const p = makeParticle(true);
      p.y = 0.85 + Math.random() * 0.15;
      particles.push(p);
    }

    function resize() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }

    function draw(now) {
      const age = now - startTime;
      ctx.clearRect(0, 0, W, H);

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        // Upward drift with fan-out: the higher the particle, the wider it spreads
        p.y += p.vy;
        const heightFraction = 1 - p.y; // 0 at bottom, 1 at top
        const fanX = (p.xBase - 0.5) * heightFraction * 0.18; // gentle fan

        if (p.y < -0.02) {
          // Respawn from crucible source
          Object.assign(p, makeParticle(false));
          p.col = pickColor(age);
        }

        // Horizontal sway + fan
        p.x += p.vx + Math.sin(p.t * p.swayFreq + p.swayOff) * p.swayAmp + fanX * 0.002;
        p.x = ((p.x % 1) + 1) % 1;
        p.t += p.ts;

        // Mouse parallax — drift toward cursor
        const targetX = p.x + (mouseX - p.x) * p.parallaxFactor * 0.04;
        const targetY = p.y + (mouseY - p.y) * p.parallaxFactor * 0.04;
        p.x += (targetX - p.x) * 0.04;
        p.y += (targetY - p.y) * 0.015;

        // Opacity flicker
        const flicker = 0.3 + 0.7 * Math.abs(Math.sin(p.t));
        const a = p.base * flicker;

        const px = p.x * W;
        const py = p.y * H;

        // Outer glow
        const g = ctx.createRadialGradient(px, py, 0, px, py, p.r * 5);
        g.addColorStop(0, `rgba(${p.col}, ${a * 0.45})`);
        g.addColorStop(1, `rgba(${p.col}, 0)`);
        ctx.beginPath();
        ctx.arc(px, py, p.r * 5, 0, Math.PI * 2);
        ctx.fillStyle = g;
        ctx.fill();

        // Bright core
        ctx.beginPath();
        ctx.arc(px, py, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${p.col}, ${Math.min(a * 1.4, 1)})`;
        ctx.shadowColor = `rgba(${p.col}, 0.9)`;
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      animId = requestAnimationFrame(draw);
    }

    resize();
    animId = requestAnimationFrame(draw);
    window.addEventListener('resize', resize);

    const handleMouse = (e) => {
      mouseX = e.clientX / window.innerWidth;
      mouseY = e.clientY / window.innerHeight;
    };
    window.addEventListener('mousemove', handleMouse);

    return () => {
      window.removeEventListener('resize', resize);
      window.removeEventListener('mousemove', handleMouse);
      cancelAnimationFrame(animId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      style={{ position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none' }}
    />
  );
}
