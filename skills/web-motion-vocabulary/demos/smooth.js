// smooth — Smooth Scroll
// Built from the Lenis docs (https://github.com/darkroomengineering/lenis), including the
// recommended GSAP ScrollTrigger sync: lenis.on("scroll", ScrollTrigger.update) and driving
// Lenis from gsap.ticker with lag smoothing off.

// Lenis changes how the whole page scrolls, so once switched on it stays on (keepAlive)
// until switched off, even after this section scrolls away.
export const meta = {
  hint: "用滑鼠滾輪或觸控板捲動，再打開開關比較手感——開啟後整頁都會套用",
  keepAlive: true,
  libs: ["gsap", "ScrollTrigger", "lenis"],
};

export const html = `
  <div class="wrap">
    <h2>同一頁，兩種捲動手感</h2>
    <p class="muted">原生捲動是滾輪轉一格、畫面跳一段；平滑捲動會帶一點慣性，滾輪停了畫面還會順順滑一小段才停。</p>
    <button class="switch" type="button" role="switch" aria-checked="false">
      <span class="knob"></span><span class="label">平滑捲動：關</span>
    </button>
    <p class="note">打開後往上、往下捲回其他段落，特別是視差和固定畫面，感受差別。<br>手機上 Lenis 預設不接管觸控捲動，維持原生手感。</p>
  </div>`;

export const css = `
  .wrap { width: min(640px, 100%); text-align: center; }
  h2 { margin: 0 0 12px; font-size: clamp(26px, 5vw, 40px); }
  .switch { margin-top: 28px; display: inline-flex; align-items: center; gap: 12px; font: inherit; font-weight: 600;
    padding: 8px 20px 8px 8px; border-radius: 999px; border: 1px solid var(--line); background: var(--surface);
    color: var(--fg); cursor: pointer; }
  .knob { width: 44px; height: 26px; border-radius: 999px; background: var(--line); position: relative; transition: background 0.2s; }
  .knob::after { content: ""; position: absolute; top: 3px; left: 3px; width: 20px; height: 20px; border-radius: 50%;
    background: var(--surface); box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25); transition: transform 0.2s; }
  .switch[aria-checked="true"] .knob { background: var(--fg); }
  .switch[aria-checked="true"] .knob::after { transform: translateX(18px); }
  .note { margin-top: 20px; font-size: 13px; color: var(--muted); }
  .switch:disabled { opacity: 0.5; cursor: not-allowed; }
`;

export function mount(root, { reduced }) {
  const sw = root.querySelector(".switch");
  const label = root.querySelector(".label");
  if (reduced) {
    sw.disabled = true;
    label.textContent = "減少動態模式下不啟用平滑捲動";
    return () => {};
  }
  const { gsap, ScrollTrigger, Lenis } = window;
  let lenis = null;
  const raf = (time) => lenis?.raf(time * 1000);

  const on = () => {
    lenis = new Lenis();
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(raf);
    gsap.ticker.lagSmoothing(0);
  };
  const off = () => {
    gsap.ticker.remove(raf);
    gsap.ticker.lagSmoothing(500, 33);   // GSAP's default
    lenis?.destroy();
    lenis = null;
  };
  const onClick = () => {
    const next = !lenis;
    next ? on() : off();
    sw.setAttribute("aria-checked", String(next));
    label.textContent = `平滑捲動：${next ? "開" : "關"}`;
  };
  sw.addEventListener("click", onClick);

  return () => {
    sw.removeEventListener("click", onClick);
    off();
  };
}
