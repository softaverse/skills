// scrollzoom — Scroll Zoom
// Built from the GSAP ScrollTrigger docs (https://gsap.com/docs/v3/Plugins/ScrollTrigger/):
// pin the panel and scrub a scale on the media. Scaling with transform (not width/height)
// keeps it smooth; the track reserves the scroll distance in CSS (pinSpacing: false).

export const meta = { hint: "往下滑：中間的小畫面會一路放大到滿版", libs: ["gsap", "ScrollTrigger"] };

export const html = `
  <div class="track">
    <div class="panel">
      <div class="title"><h2>新一代工作台</h2><p class="muted">往下滑，打開它</p></div>
      <div class="media"><div class="ui"><i></i><i></i><i></i><b></b></div><p class="caption">產品畫面 · 實際尺寸</p></div>
    </div>
  </div>`;

export const css = `
  & { display: block; padding: 0; place-items: normal; }
  .track { height: 220vh; }
  .panel { position: relative; height: calc(100vh - var(--head-h, 0px)); overflow: hidden; }
  .title { position: absolute; top: 8%; left: 0; right: 0; text-align: center; padding: 0 24px; z-index: 1; }
  h2 { margin: 0 0 4px; font-size: clamp(28px, 5vw, 48px); }
  .title p { margin: 0; }
  .media { position: absolute; inset: 0; background: var(--placeholder); transform-origin: 50% 60%;
    display: grid; place-items: center; will-change: transform; }
  .ui { width: min(70%, 900px); aspect-ratio: 16 / 10; border-radius: 12px; background: var(--surface);
    border: 1px solid var(--line); box-shadow: var(--shadow); padding: 4%; display: grid; gap: 4%;
    grid-template-columns: 1fr 3fr; grid-template-rows: repeat(3, 1fr); }
  .ui i { grid-column: 1; border-radius: 6px; background: var(--icon); }
  .ui b { grid-column: 2; grid-row: 1 / 4; border-radius: 8px; background: var(--icon); }
  .caption { position: absolute; bottom: 6%; margin: 0; font-size: 13px; color: var(--muted); }
  [data-reduced] & .track { height: auto; }
`;

const headH = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--head-h")) || 0;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const gsap = window.gsap;
  const ctx = gsap.context(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: root.querySelector(".track"),
        start: () => `top top+=${headH()}`,
        end: "bottom bottom",
        pin: root.querySelector(".panel"),
        pinSpacing: false,
        scrub: 0.5,
        invalidateOnRefresh: true,
      },
    });
    tl.fromTo(root.querySelector(".media"),
      { scale: 0.35, borderRadius: 40 },
      { scale: 1, borderRadius: 0, ease: "power1.inOut" })
      .to(root.querySelector(".title"), { autoAlpha: 0, y: -40, ease: "none", duration: 0.4 }, 0)
      .to({}, { duration: 0.3 });   // hold full-bleed before releasing the pin
  }, root);
  return () => ctx.revert();
}
