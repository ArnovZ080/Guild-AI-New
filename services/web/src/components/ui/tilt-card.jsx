import { useRef, useState } from 'react';
import { motion } from 'framer-motion';

/**
 * TiltCard — subtle 3D perspective tilt following mouse position.
 * Drop-in wrapper: replaces any containing div.
 */
export function TiltCard({ children, className = '', maxTilt = 8, scale = 1.02, glowColor = 'rgba(94,106,210,0.15)' }) {
  const ref = useRef(null);
  const [transform, setTransform] = useState('');
  const [glow, setGlow] = useState('');

  const handleMove = (e) => {
    const rect = ref.current?.getBoundingClientRect();
    if (!rect) return;
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const cx = rect.width / 2;
    const cy = rect.height / 2;
    const rotX = ((y - cy) / cy) * -maxTilt;
    const rotY = ((x - cx) / cx) * maxTilt;
    setTransform(`perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(${scale})`);
    // Glow follows mouse
    const px = (x / rect.width) * 100;
    const py = (y / rect.height) * 100;
    setGlow(`radial-gradient(circle at ${px}% ${py}%, ${glowColor} 0%, transparent 60%)`);
  };

  const handleLeave = () => {
    setTransform('perspective(800px) rotateX(0deg) rotateY(0deg) scale(1)');
    setGlow('');
  };

  return (
    <motion.div
      ref={ref}
      className={className}
      style={{
        transform,
        transition: 'transform 0.4s cubic-bezier(0.16,1,0.3,1)',
        willChange: 'transform',
        position: 'relative',
      }}
      onMouseMove={handleMove}
      onMouseLeave={handleLeave}
    >
      {glow && (
        <div
          aria-hidden="true"
          style={{
            position: 'absolute', inset: 0, borderRadius: 'inherit',
            background: glow, pointerEvents: 'none', zIndex: 0,
          }}
        />
      )}
      <div style={{ position: 'relative', zIndex: 1 }}>{children}</div>
    </motion.div>
  );
}
