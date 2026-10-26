// scramble — Scramble Text
// Built from the GSAP ScrambleTextPlugin docs (https://gsap.com/docs/v3/Plugins/ScrambleTextPlugin/).
// React Bits has a ready-made Scrambled Text (https://reactbits.dev/text-animations/scrambled-text);
// its code is not included here because its license forbids redistribution.

export const meta = {
  hint: "捲到時文字從亂碼解出來；游標滑過按鈕會再解一次",
  replay: true,
  libs: ["gsap", "ScrollTrigger", "ScrambleTextPlugin"],
};

export const html = `
  <div class="wrap">
    <p class="eyebrow" data-scramble>SYSTEM ONLINE</p>
    <h2 class="headline" data-scramble>AI 幫你整理一切</h2>
    <div class="stats">
      <div class="card"><span class="num" data-scramble data-chars="0123456789">99.9%</span><p>服務可用率</p></div>
      <div class="card"><span class="num" data-scramble data-chars="0123456789">&lt; 50ms</span><p>平均回應時間</p></div>
      <div class="card"><span class="num" data-scramble data-chars="0123456789">24/7</span><p>全天候監控</p></div>
    </div>
    <button class="btn" type="button"><span>START_FREE_TRIAL</span></button>
  </div>`;

export const css = `
  .wrap { width: min(760px, 100%); text-align: center; }
  .eyebrow { margin: 0 0 12px; font: 600 13px var(--mono); letter-spacing: 0.2em; color: var(--muted); }
  .headline { margin: 0; font-size: clamp(32px, 6vw, 56px); line-height: 1.2; min-height: 1.2em; }
  .stats { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin-top: 32px; }
  .num { display: block; font: 700 clamp(26px, 5vw, 36px) var(--mono); min-height: 1.3em; }
  .card p { margin: 4px 0 0; font-size: 14px; color: var(--muted); }
  .btn { margin-top: 28px; font: 600 14px var(--mono); letter-spacing: 0.06em; padding: 14px 26px;
    border-radius: 999px; border: 0; background: var(--fg); color: var(--bg); cursor: pointer; }
  .btn span { display: inline-block; min-width: 16ch; }
`;

const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const gsap = window.gsap;
  const btn = root.querySelector(".btn");
  const label = btn.querySelector("span");
  const scramble = (el, extra = {}) => gsap.to(el, {
    duration: 0.8,
    ease: "none",
    scrambleText: { text: el.dataset.text, chars: el.dataset.chars || LETTERS, speed: 0.5, revealDelay: 0.2 },
    ...extra,
  });

  const ctx = gsap.context(() => {
    root.querySelectorAll("[data-scramble]").forEach((el, i) => {
      el.dataset.text = el.textContent;
      scramble(el, {
        delay: i * 0.08,
        scrollTrigger: { trigger: root.querySelector(".headline"), start: "top 80%", once: true },
      });
    });
    label.dataset.text = label.textContent;
  }, root);

  const onEnter = () => ctx.add(() => scramble(label, { duration: 0.6 }));
  btn.addEventListener("pointerenter", onEnter);

  return () => {
    btn.removeEventListener("pointerenter", onEnter);
    ctx.revert();
  };
}
