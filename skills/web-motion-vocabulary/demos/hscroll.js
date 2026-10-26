// hscroll — Horizontal Scroll
// Built from the GSAP ScrollTrigger docs (https://gsap.com/docs/v3/Plugins/ScrollTrigger/):
// pin the panel and scrub the row sideways. The track reserves the scroll distance in CSS
// (pinSpacing: false), so mounting or unmounting never changes the page height.

export const meta = { hint: "往下滑：畫面停住，作品改成往左移動", libs: ["gsap", "ScrollTrigger"] };

const WORKS = ["品牌識別", "電商改版", "App 設計", "活動網站", "年度報告", "包裝設計"];

export const html = `
  <div class="track">
    <div class="panel">
      <div class="intro"><h2>精選作品</h2><p class="muted">往下滑，作品會橫向經過</p></div>
      <div class="row">
        ${WORKS.map((w, i) => `<figure class="work"><div class="img"><span>${String(i + 1).padStart(2, "0")}</span></div><figcaption>${w}</figcaption></figure>`).join("")}
      </div>
    </div>
  </div>`;

export const css = `
  & { display: block; padding: 0; place-items: normal; }
  .track { height: 300vh; }
  .panel { height: calc(100vh - var(--head-h, 0px)); display: flex; flex-direction: column;
    justify-content: center; gap: 28px; overflow: hidden; }
  .intro { padding: 0 max(24px, calc((100% - 1100px) / 2)); }
  h2 { margin: 0 0 4px; font-size: clamp(28px, 5vw, 44px); }
  .intro p { margin: 0; }
  .row { display: flex; gap: 20px; width: max-content; padding: 0 max(24px, calc((100vw - 1100px) / 2)); will-change: transform; }
  .work { margin: 0; width: clamp(240px, 32vw, 380px); }
  .img { aspect-ratio: 4 / 3; border-radius: 16px; background: var(--placeholder); border: 1px solid var(--line);
    display: grid; place-items: center; }
  .img span { font: 700 56px var(--font); color: var(--num); }
  figcaption { margin-top: 10px; font-weight: 600; }
  /* Reduced motion: no pin; the row scrolls sideways natively */
  [data-reduced] & .track { height: auto; }
  [data-reduced] & .panel { height: auto; padding: 48px 0; overflow: visible; }
  [data-reduced] & .row { width: auto; overflow-x: auto; }
  [data-reduced] & .work { flex: none; }
`;

const headH = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--head-h")) || 0;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const gsap = window.gsap;
  const row = root.querySelector(".row");
  const panel = root.querySelector(".panel");
  const ctx = gsap.context(() => {
    gsap.to(row, {
      x: () => -Math.max(0, row.scrollWidth - panel.clientWidth),
      ease: "none",
      scrollTrigger: {
        trigger: root.querySelector(".track"),
        start: () => `top top+=${headH()}`,
        end: "bottom bottom",
        pin: panel,
        pinSpacing: false,
        scrub: 0.5,
        invalidateOnRefresh: true,
      },
    });
  }, root);
  return () => ctx.revert();
}
