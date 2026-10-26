// shimmer — Shimmer Text
// Ported from Magic UI Animated Shiny Text (https://magicui.design/docs/components/animated-shiny-text)
// to plain CSS, keeping its defaults: shimmerWidth 100px, 8s loop with the glare crossing
// between 30% and 60%, text at 70% opacity, glare black/80 (light) or white/80 (dark).
// MIT, Copyright (c) Magic UI — see _shared/LICENSE-magicui.md

// Runs forever, so it only animates while its section is mounted.
export const meta = { hint: "看標籤上那道反覆掃過的光——它會一直播放，佔掉同畫面唯一的持續動畫額度" };

export const html = `
  <div class="hero">
    <a class="badge" href="#" onclick="return false"><span class="shiny">✨ 推出全新 AI 摘要功能</span><span class="arrow">→</span></a>
    <h2>一份文件，三秒看懂</h2>
    <p class="muted">流光只放在一個小地方：公告標籤。主標題保持靜止，讓眼睛知道先看哪裡。</p>
  </div>`;

export const css = `
  .hero { width: min(760px, 100%); text-align: center; }
  .badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px; border-radius: 999px;
    border: 1px solid var(--line); background: var(--surface); text-decoration: none; font-size: 14px; }
  .shiny {
    --shiny-width: 100px;
    color: color-mix(in srgb, var(--muted) 70%, transparent);
    background-image: linear-gradient(to right, transparent, var(--shine) 50%, transparent);
    background-size: var(--shiny-width) 100%;
    background-position: 0 0;
    background-repeat: no-repeat;
    -webkit-background-clip: text;
    background-clip: text;
  }
  .arrow { color: var(--muted); }
  h2 { margin: 28px 0 12px; font-size: clamp(30px, 6vw, 52px); line-height: 1.2; }
  &[data-mounted] .shiny { animation: shimmer-shiny-text 8s infinite; }
  [data-reduced] &[data-mounted] .shiny { animation: none; }
  & { --shine: rgb(0 0 0 / 0.8); }
  [data-theme="dark"] & { --shine: rgb(255 255 255 / 0.8); }
`;

export const globalCss = `
  @keyframes shimmer-shiny-text {
    0%, 90%, 100% { background-position: calc(-100% - var(--shiny-width)) 0; }
    30%, 60% { background-position: calc(100% + var(--shiny-width)) 0; }
  }
`;

export function mount() {
  return () => {};
}
