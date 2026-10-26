// countup — Count-up
// Ported from Magic UI Number Ticker (https://magicui.design/docs/components/number-ticker)
// to vanilla Motion, keeping its spring (damping 60, stiffness 100), once-in-view trigger,
// and tabular numbers. MIT, Copyright (c) Magic UI — see _shared/LICENSE-magicui.md

export const meta = { hint: "數字捲進畫面時開始跳動", replay: true, libs: ["motion"] };

export const html = `
  <div class="stats">
    <div class="card stat"><span class="num" data-value="12000">0</span><span class="num">+</span><p>家企業正在使用</p></div>
    <div class="card stat"><span class="num" data-value="98">0</span><span class="num">%</span><p>客戶續約率</p></div>
    <div class="card stat"><span class="num" data-value="4.9" data-decimals="1">0.0</span><p>App Store 評分</p></div>
  </div>`;

export const css = `
  .stats { width: min(760px, 100%); display: grid; gap: 12px;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); }
  .stat { text-align: center; padding: 28px 16px; }
  .num { display: inline-block; font-size: clamp(36px, 8vw, 52px); font-weight: 700;
    letter-spacing: 0.02em; font-variant-numeric: tabular-nums; }
  .stat p { margin: 4px 0 0; color: var(--muted); font-size: 14px; }
`;

export function mount(root, { reduced }) {
  const { animate, inView } = window.Motion;
  const stops = [];

  root.querySelectorAll("[data-value]").forEach((el) => {
    const value = Number(el.dataset.value);
    const decimals = Number(el.dataset.decimals || 0);
    const format = (v) => Intl.NumberFormat("en-US", {
      minimumFractionDigits: decimals, maximumFractionDigits: decimals,
    }).format(Number(v.toFixed(decimals)));

    if (reduced) {
      el.textContent = format(value);
      return;
    }
    stops.push(inView(el, () => {
      const a = animate(0, value, {
        type: "spring", damping: 60, stiffness: 100,
        onUpdate: (v) => { el.textContent = format(v); },
        onComplete: () => { el.textContent = format(value); },
      });
      stops.push(() => a.stop());
    }, { margin: "0px" }));
  });

  return () => stops.forEach((stop) => stop());
}
