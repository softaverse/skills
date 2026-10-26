// parallax — Parallax
// Built from the GSAP ScrollTrigger docs (https://gsap.com/docs/v3/Plugins/ScrollTrigger/):
// each layer scrubs with the scroll at its own speed; the text layer does not move.

export const meta = { hint: "往下滑，注意太陽、遠山、近山和文字的移動速度都不同", libs: ["gsap", "ScrollTrigger"] };

export const html = `
  <div class="scene">
    <div class="sun" aria-hidden="true"></div>
    <svg class="layer far" viewBox="0 0 1200 400" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0 260 L160 150 L300 230 L460 110 L640 220 L800 130 L980 210 L1200 120 L1200 400 L0 400 Z"/>
    </svg>
    <svg class="layer mid" viewBox="0 0 1200 400" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0 300 L220 200 L380 280 L560 190 L760 290 L940 210 L1200 280 L1200 400 L0 400 Z"/>
    </svg>
    <svg class="layer near" viewBox="0 0 1200 400" preserveAspectRatio="none" aria-hidden="true">
      <path d="M0 340 L260 290 L480 350 L700 300 L920 360 L1200 310 L1200 400 L0 400 Z"/>
    </svg>
    <div class="copy">
      <h2>走進山裡的三天兩夜</h2>
      <p>越遠的東西移動得越慢：太陽最慢、遠山次之，近山和文字跟著頁面走——<br>速度差讓平面的畫面有了前後的距離。</p>
    </div>
  </div>`;

export const css = `
  & { display: block; padding: 0; place-items: normal; }
  .scene { position: relative; height: 140vh; overflow: hidden;
    background: linear-gradient(to bottom, color-mix(in srgb, var(--fg) 6%, var(--section-bg)), var(--section-bg) 80%); }
  .sun { position: absolute; top: 34vh; left: 62%; width: 18vh; height: 18vh; border-radius: 50%;
    background: color-mix(in srgb, var(--fg) 12%, var(--section-bg)); will-change: transform; }
  .layer { position: absolute; left: 0; width: 100%; height: 75vh; bottom: 0; will-change: transform; }
  .far path { fill: color-mix(in srgb, var(--fg) 16%, var(--section-bg)); }
  .mid path { fill: color-mix(in srgb, var(--fg) 28%, var(--section-bg)); }
  .near path { fill: color-mix(in srgb, var(--fg) 42%, var(--section-bg)); }
  .far { bottom: 26vh; }
  .mid { bottom: 12vh; }
  .near { height: 45vh; }
  .copy { position: absolute; top: 14vh; left: 0; right: 0; text-align: center; padding: 0 24px; z-index: 1; }
  h2 { margin: 0 0 12px; font-size: clamp(30px, 6vw, 52px); line-height: 1.2; }
  .copy p { margin: 0; color: var(--muted); }
`;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const gsap = window.gsap;
  const scene = root.querySelector(".scene");
  const ctx = gsap.context(() => {
    // Farther layers lag behind the scroll more; small differences avoid motion sickness.
    [[".sun", 0.5], [".far", 0.35], [".mid", 0.18]].forEach(([sel, lag]) => {
      gsap.to(root.querySelector(sel), {
        y: () => scene.offsetHeight * lag,
        ease: "none",
        scrollTrigger: { trigger: scene, start: "top bottom", end: "bottom top", scrub: true, invalidateOnRefresh: true },
      });
    });
  }, root);
  return () => ctx.revert();
}
