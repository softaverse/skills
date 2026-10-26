// magnet — Magnetic Button
// Built from the GSAP docs (gsap.quickTo): https://gsap.com/docs/v3/GSAP/gsap.quickTo()
// React Bits has a ready-made Magnet component (https://reactbits.dev/animations/magnet);
// its code is not included here because its license forbids redistribution.

export const meta = { hint: "把游標移到按鈕附近，慢慢繞一圈", libs: ["gsap"] };

export const html = `
  <div class="center">
    <div class="field"><button class="btn" type="button"><span>聯絡我們</span></button></div>
    <p class="note">觸控裝置沒有游標，這個效果在手機上不會出現</p>
    <label class="toggle"><input type="checkbox"> 顯示感應範圍</label>
  </div>`;

export const css = `
  .center { display: grid; justify-items: center; }
  .field { position: relative; display: grid; place-items: center; width: 320px; height: 220px; }
  .field::before { content: ""; position: absolute; inset: 0; border-radius: 999px;
    border: 1px dashed transparent; transition: border-color 0.2s; }
  .show-field .field::before { border-color: var(--muted); }
  .btn { font: inherit; font-size: 16px; font-weight: 600; padding: 16px 32px; border-radius: 999px;
    border: 0; background: var(--fg); color: var(--bg); cursor: pointer; }
  .btn span { display: inline-block; }
  .note { font-size: 13px; color: var(--muted); margin: 8px 0 0; }
  .toggle { margin-top: 16px; font-size: 13px; color: var(--muted); display: flex; gap: 6px; align-items: center; }
`;

export function mount(root, { reduced }) {
  const field = root.querySelector(".field");
  const btn = root.querySelector(".btn");
  const label = btn.querySelector("span");
  const box = root.querySelector(".toggle input");
  const onToggle = () => root.classList.toggle("show-field", box.checked);
  box.addEventListener("change", onToggle);
  if (reduced) return () => box.removeEventListener("change", onToggle);

  const gsap = window.gsap;
  const ctx = gsap.context(() => {
    const strength = 0.35;   // button follows 35% of the pointer's offset
    const ease = { duration: 0.4, ease: "power3.out" };
    const bx = gsap.quickTo(btn, "x", ease), by = gsap.quickTo(btn, "y", ease);
    const lx = gsap.quickTo(label, "x", ease), ly = gsap.quickTo(label, "y", ease);

    const onMove = (e) => {
      const r = btn.getBoundingClientRect();
      const dx = e.clientX - (r.left + r.width / 2);
      const dy = e.clientY - (r.top + r.height / 2);
      bx(dx * strength); by(dy * strength);
      lx(dx * strength * 0.4); ly(dy * strength * 0.4);   // text drifts a little further: depth
    };
    const onLeave = () => gsap.to([btn, label], { x: 0, y: 0, duration: 0.8, ease: "elastic.out(1, 0.4)" });
    field.addEventListener("pointermove", onMove);
    field.addEventListener("pointerleave", onLeave);
    return () => {
      field.removeEventListener("pointermove", onMove);
      field.removeEventListener("pointerleave", onLeave);
    };
  }, root);

  return () => {
    box.removeEventListener("change", onToggle);
    ctx.revert();
  };
}
