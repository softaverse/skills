// reveal — Scroll-triggered Reveal
// Ported from Magic UI Blur Fade (https://magicui.design/docs/components/blur-fade)
// to vanilla Motion, keeping its defaults: duration 0.4, offset 6px, blur 6px,
// delay 0.04 + n, margin -50px, easeOut. MIT, Copyright (c) Magic UI — see _shared/LICENSE-magicui.md

export const meta = { hint: "往下滑，看每一段怎麼出現", replay: true, libs: ["motion"] };

export const html = `
  <div class="page">
    <div class="block">
      <h2 data-reveal>把複雜的流程，變成一個按鈕</h2>
      <p data-reveal>每一段內容捲進畫面時，從微微模糊、稍微偏上的位置，淡入到定位。</p>
      <p data-reveal>位移只有 6px、時間 0.4 秒——訪客幾乎不會「注意到動畫」，只會覺得順。</p>
    </div>
    <div class="block">
      <h2 data-reveal>三個理由</h2>
      <div class="grid">
        <div class="card" data-reveal><h3>更快</h3><p>設定時間從一週縮短到一小時。</p></div>
        <div class="card" data-reveal><h3>更穩</h3><p>自動備份，任何操作都能還原。</p></div>
        <div class="card" data-reveal><h3>更省</h3><p>只為實際用到的功能付費。</p></div>
      </div>
    </div>
    <div class="block">
      <h2 data-reveal>實際畫面</h2>
      <div class="photo" data-reveal></div>
    </div>
  </div>`;

export const css = `
  & { display: block; place-items: normal; }
  .page { max-width: 720px; margin: 0 auto; }
  .block + .block { margin-top: 30vh; }
  h2 { font-size: clamp(24px, 5vw, 36px); line-height: 1.25; margin: 0 0 12px; }
  p { margin: 0 0 12px; color: var(--muted); }
  .grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin-top: 20px; }
  .card h3 { margin: 0 0 6px; font-size: 16px; }
  .card p { margin: 0; font-size: 14px; }
  .photo { aspect-ratio: 16 / 9; border-radius: var(--radius); margin-top: 20px;
    background: var(--placeholder); }
`;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const { animate, inView } = window.Motion;
  const offset = 6, blur = "6px", duration = 0.4;
  const waiting = new Set();
  const stops = [];

  const reveal = (el, delay) => {
    if (!waiting.delete(el)) return;
    stops.push(animate(el, { opacity: 1, y: 0, filter: "blur(0px)" }, { delay, duration, ease: "easeOut" }));
  };

  // Hide with JS, not CSS: without JS the content stays visible.
  root.querySelectorAll(".block").forEach((block) => {
    block.querySelectorAll("[data-reveal]").forEach((el, i) => {
      el.style.opacity = 0;
      el.style.transform = `translateY(${-offset}px)`;
      el.style.filter = `blur(${blur})`;
      waiting.add(el);
      stops.push({ stop: inView(el, () => reveal(el, 0.04 + i * 0.05), { margin: "-50px" }) });
    });
  });

  // A fast scroll or an anchor jump can skip past an element without it ever
  // intersecting; reveal anything already above the fold so no text stays hidden.
  const onScroll = () => waiting.forEach((el) => {
    if (el.getBoundingClientRect().top < innerHeight) reveal(el, 0);
  });
  addEventListener("scroll", onScroll, { passive: true });

  return () => {
    removeEventListener("scroll", onScroll);
    stops.forEach((s) => (typeof s.stop === "function" ? s.stop() : s.stop?.()));
  };
}
