// spot — Spotlight Card
// Ported from Magic UI Magic Card, gradient mode (https://magicui.design/docs/components/magic-card)
// to plain JS + CSS, keeping its defaults: gradientSize 200, gradientOpacity 0.8,
// border gradient #9E7AFF → #FE8BBB, and the docs' gradientColor per theme
// (#262626 dark, #D9D9D955 light — the --spot-inner token).
// MIT, Copyright (c) Magic UI — see _shared/LICENSE-magicui.md

// Follows the pointer only and never moves on its own, so it stays on under reduced motion.
export const meta = { hint: "把游標在卡片之間移動，注意邊框和卡片內的光" };

export const html = `
  <div class="center">
    <div class="grid">
      <div class="magic"><h3>AI 摘要</h3><p>上傳文件，三秒得到重點。</p></div>
      <div class="magic"><h3>多語翻譯</h3><p>支援 40 種語言，保留原本格式。</p></div>
      <div class="magic"><h3>團隊協作</h3><p>即時共同編輯，留言不漏接。</p></div>
    </div>
    <p class="note">深色背景最明顯，可以切到上方的「深色」比較；觸控裝置上沒有這個效果</p>
  </div>`;

export const css = `
  .center { width: min(760px, 100%); }
  .grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
  .magic {
    --size: 200px; --x: -200px; --y: -200px;
    position: relative; isolation: isolate; overflow: hidden;
    border-radius: var(--radius); border: 1px solid transparent; padding: 24px;
    background:
      linear-gradient(var(--surface) 0 0) padding-box,
      radial-gradient(var(--size) circle at var(--x) var(--y), #9E7AFF, #FE8BBB, var(--line) 100%) border-box;
  }
  .magic::after {
    content: ""; position: absolute; inset: 1px; z-index: -1; border-radius: inherit;
    pointer-events: none; opacity: 0; transition: opacity 0.3s;
    background: radial-gradient(var(--size) circle at var(--x) var(--y), var(--spot-inner), transparent 100%);
  }
  .magic:hover::after { opacity: 0.8; }
  h3 { margin: 0 0 6px; font-size: 17px; }
  .magic p { margin: 0; font-size: 14px; color: var(--muted); }
  .note { font-size: 13px; color: var(--muted); margin: 16px 0 0; text-align: center; }
`;

export function mount(root) {
  const offs = [];
  root.querySelectorAll(".magic").forEach((card) => {
    const onMove = (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty("--x", `${e.clientX - r.left}px`);
      card.style.setProperty("--y", `${e.clientY - r.top}px`);
    };
    const onLeave = () => { card.style.setProperty("--x", "-200px"); card.style.setProperty("--y", "-200px"); };
    card.addEventListener("pointermove", onMove);
    card.addEventListener("pointerleave", onLeave);
    offs.push(() => {
      card.removeEventListener("pointermove", onMove);
      card.removeEventListener("pointerleave", onLeave);
    });
  });
  return () => offs.forEach((off) => off());
}
