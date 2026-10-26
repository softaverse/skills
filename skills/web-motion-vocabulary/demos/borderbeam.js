// borderbeam — Border Beam
// Ported from Magic UI Border Beam (https://magicui.design/docs/components/border-beam)
// to plain CSS: a gradient square travels along offset-path: rect(), masked to the border.
// Keeps its colors (#ffaa40 → #9c40ff) and linear infinite loop; size 100 / duration 8
// as in the Magic UI docs demo. MIT, Copyright (c) Magic UI — see _shared/LICENSE-magicui.md

// Runs forever, so it only animates while its section is mounted.
export const meta = { hint: "看推薦方案的邊框上那道繞行的光——它會一直播放，整頁只該給一個元素" };

const PLANS = [
  ["免費", "$0", ["3 個專案", "基本報表"]],
  ["專業", "$12", ["無限專案", "進階報表", "優先支援"], true],
  ["團隊", "$39", ["多人協作", "權限管理", "SSO 登入"]],
];

export const html = `
  <div class="plans">
    ${PLANS.map(([name, price, items, pick]) => `
      <div class="plan${pick ? " pick" : ""}">
        ${pick ? '<span class="tag">推薦</span><div class="beam" aria-hidden="true"><i></i></div>' : ""}
        <h3>${name}</h3>
        <p class="price">${price}<small> / 月</small></p>
        <ul>${items.map((x) => `<li>${x}</li>`).join("")}</ul>
      </div>`).join("")}
  </div>`;

export const css = `
  .plans { width: min(860px, 100%); display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
  .plan { position: relative; padding: 28px 24px; border-radius: 20px; background: var(--surface); border: 1px solid var(--line); }
  .tag { position: absolute; top: 16px; right: 16px; font-size: 12px; padding: 2px 10px; border-radius: 999px;
    background: var(--fg); color: var(--bg); }
  h3 { margin: 0; font-size: 16px; color: var(--muted); }
  .price { margin: 8px 0 16px; font-size: 40px; font-weight: 700; }
  .price small { font-size: 14px; font-weight: 400; color: var(--muted); }
  ul { margin: 0; padding: 0 0 0 18px; color: var(--muted); font-size: 14px; line-height: 2; }
  .beam {
    --size: 100px;
    position: absolute; inset: 0; pointer-events: none; border-radius: inherit;
    border: 1px solid transparent;
    mask: linear-gradient(transparent, transparent) padding-box, linear-gradient(#000, #000) border-box;
    mask-composite: intersect;
  }
  .beam i {
    position: absolute; width: var(--size); aspect-ratio: 1;
    background: linear-gradient(to left, #ffaa40, #9c40ff, transparent);
    offset-path: rect(0 auto auto 0 round var(--size));
    offset-distance: 0%;
  }
  &[data-mounted] .beam i { animation: borderbeam-travel 8s linear infinite; }
  [data-reduced] &[data-mounted] .beam i { animation: none; }
`;

export const globalCss = `
  @keyframes borderbeam-travel { to { offset-distance: 100%; } }
`;

export function mount() {
  return () => {};
}
