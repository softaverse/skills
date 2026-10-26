// spring — Spring Button
// Built from the Motion docs: https://motion.dev/docs/hover , https://motion.dev/docs/press

export const meta = { hint: "游標移到兩個按鈕上，再按下去，比較手感", libs: ["motion"] };

export const html = `
  <div class="pair">
    <div><button class="btn plain" type="button">開始免費試用</button><span class="label">一般按鈕：只換顏色</span></div>
    <div><button class="btn springy" type="button">開始免費試用</button><span class="label">彈簧按鈕：放大、按下回彈</span></div>
  </div>`;

export const css = `
  .pair { display: flex; gap: 40px; flex-wrap: wrap; justify-content: center; text-align: center; }
  .label { display: block; margin-top: 14px; font-size: 13px; color: var(--muted); }
  .btn { font: inherit; font-size: 16px; font-weight: 600; padding: 14px 28px; border-radius: 999px;
    border: 0; background: var(--fg); color: var(--bg); cursor: pointer; }
  .btn.plain:hover { background: var(--fg-hover); }
  .btn.springy { will-change: transform; }
  [data-reduced] & .btn.springy:hover { background: var(--fg-hover); }
`;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const { animate, hover, press } = window.Motion;
  const btn = root.querySelector(".btn.springy");
  const springy = { type: "spring", stiffness: 400, damping: 18 };

  const stopHover = hover(btn, (el) => {
    animate(el, { scale: 1.05 }, springy);
    return () => animate(el, { scale: 1 }, springy);
  });
  const stopPress = press(btn, (el) => {
    animate(el, { scale: 0.94 }, springy);
    return () => animate(el, { scale: 1.05 }, springy);
  });

  return () => { stopHover(); stopPress(); };
}
