// stagger — Stagger
// Built from the Motion docs: https://motion.dev/docs/stagger

export const meta = { hint: "捲到時卡片會依序出現；按上面的按鈕比較「交錯」和「同時」", replay: true, libs: ["motion"] };

export const html = `
  <div class="wrap">
    <div class="modes">
      <button type="button" data-gap="0.08" aria-pressed="true">▶ 交錯出現（間隔 0.08 秒）</button>
      <button type="button" data-gap="0" aria-pressed="false">▶ 同時出現</button>
    </div>
    <div class="grid">
      <div class="card"><div class="icon"></div><h3>即時同步</h3><p>所有裝置上的資料自動更新。</p></div>
      <div class="card"><div class="icon"></div><h3>權限管理</h3><p>每個成員只看得到該看的。</p></div>
      <div class="card"><div class="icon"></div><h3>版本紀錄</h3><p>任何修改都能回到上一步。</p></div>
      <div class="card"><div class="icon"></div><h3>自動化</h3><p>重複的工作交給規則處理。</p></div>
      <div class="card"><div class="icon"></div><h3>報表</h3><p>一鍵匯出每週的成果。</p></div>
      <div class="card"><div class="icon"></div><h3>整合</h3><p>連接你已經在用的工具。</p></div>
    </div>
  </div>`;

export const css = `
  .wrap { width: min(760px, 100%); }
  .modes { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
  .modes button { font: inherit; font-size: 14px; color: var(--fg); background: var(--surface);
    border: 1px solid var(--line); border-radius: 999px; padding: 6px 14px; cursor: pointer; }
  .modes button[aria-pressed="true"] { background: var(--fg); color: var(--bg); }
  .grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
  .card h3 { margin: 0 0 6px; font-size: 16px; }
  .card p { margin: 0; font-size: 14px; color: var(--muted); }
  .icon { width: 32px; height: 32px; border-radius: 8px; background: var(--icon); margin-bottom: 12px; }
`;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const { animate, inView, stagger } = window.Motion;
  const cards = root.querySelectorAll(".grid .card");
  const buttons = root.querySelectorAll(".modes button");
  let running = null;

  const play = (gap) => {
    running?.stop();
    running = animate(cards,
      { opacity: [0, 1], y: [24, 0] },
      { duration: 0.5, ease: [0.22, 1, 0.36, 1], delay: gap ? stagger(gap) : 0 });
  };

  const onClick = (ev) => {
    const b = ev.target.closest("button");
    if (!b) return;
    buttons.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    play(Number(b.dataset.gap));
  };
  root.addEventListener("click", onClick);

  // Mounted a screen early, so wait until the cards are actually seen.
  cards.forEach((c) => (c.style.opacity = 0));
  const stopInView = inView(root.querySelector(".grid"), () => { play(0.08); }, { amount: 0.3 });

  return () => {
    stopInView();
    running?.stop();
    root.removeEventListener("click", onClick);
  };
}
