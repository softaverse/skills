// tilt — Tilt Card
// Plain JS + CSS transforms, no library.
// React Bits has a ready-made Tilted Card (https://reactbits.dev/components/tilted-card);
// its code is not included here because its license forbids redistribution.

export const meta = { hint: "把游標移到卡片上畫圈" };

export const html = `
  <div class="center">
    <div class="scene">
      <div class="tilt">
        <div class="art"></div>
        <div class="meta"><h3>Studio Series</h3><p>限量 300 組・2026</p></div>
        <div class="glare"></div>
      </div>
    </div>
    <p class="note">觸控裝置上卡片維持平放</p>
  </div>`;

export const css = `
  .center { display: grid; justify-items: center; }
  .scene { perspective: 900px; }
  .tilt { position: relative; width: 240px; aspect-ratio: 5 / 7; border-radius: 18px; overflow: hidden;
    background: var(--tilt-face);
    border: 1px solid var(--line); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
    transform-style: preserve-3d; will-change: transform; transition: box-shadow 0.3s; }
  .tilt:hover { box-shadow: 0 30px 60px rgba(0, 0, 0, 0.28); }
  .art { position: absolute; inset: 18px 18px 110px; border-radius: 12px;
    background: var(--art); }
  .meta { position: absolute; left: 22px; right: 22px; bottom: 22px; }
  h3 { margin: 0; font-size: 20px; }
  .meta p { margin: 2px 0 0; color: var(--muted); font-size: 13px; }
  .glare { position: absolute; inset: 0; pointer-events: none; opacity: 0; transition: opacity 0.3s;
    background: radial-gradient(circle at var(--gx, 50%) var(--gy, 50%), var(--glare), transparent 55%); }
  .tilt:hover .glare { opacity: 1; }
  .note { font-size: 13px; color: var(--muted); margin: 16px 0 0; }
`;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const card = root.querySelector(".tilt");
  const glare = card.querySelector(".glare");
  const max = 10;   // degrees
  let target = { rx: 0, ry: 0 }, current = { rx: 0, ry: 0 }, frame = null;

  // Ease toward the target each frame, and stop once settled (no endless loop).
  function tick() {
    current.rx += (target.rx - current.rx) * 0.15;
    current.ry += (target.ry - current.ry) * 0.15;
    const settled = Math.abs(target.rx - current.rx) < 0.01 && Math.abs(target.ry - current.ry) < 0.01;
    if (settled) current = { ...target };
    card.style.transform = `rotateX(${current.rx}deg) rotateY(${current.ry}deg)`;
    frame = settled ? null : requestAnimationFrame(tick);
  }
  const start = () => { if (!frame) frame = requestAnimationFrame(tick); };

  const onMove = (e) => {
    const r = card.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
    target = { rx: (0.5 - py) * 2 * max, ry: (px - 0.5) * 2 * max };
    glare.style.setProperty("--gx", `${px * 100}%`);
    glare.style.setProperty("--gy", `${py * 100}%`);
    start();
  };
  const onLeave = () => { target = { rx: 0, ry: 0 }; start(); };
  card.addEventListener("pointermove", onMove);
  card.addEventListener("pointerleave", onLeave);

  return () => {
    if (frame) cancelAnimationFrame(frame);
    card.removeEventListener("pointermove", onMove);
    card.removeEventListener("pointerleave", onLeave);
  };
}
