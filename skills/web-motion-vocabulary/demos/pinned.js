// pinned — Pinned Scrollytelling
// Built from the GSAP ScrollTrigger docs (https://gsap.com/docs/v3/Plugins/ScrollTrigger/):
// pin a panel and scrub a timeline through it. The track reserves the scroll distance
// in CSS (pinSpacing: false), so mounting or unmounting never changes the page height.

export const meta = { hint: "往下滑：畫面會停住，內容在原地換三次，換完才繼續往下", libs: ["gsap", "ScrollTrigger"] };

const STEPS = [
  ["01", "上傳", "把會議錄音拖進來，支援 30 種格式。"],
  ["02", "整理", "AI 自動分段、標出講者、找出待辦事項。"],
  ["03", "分享", "一鍵產生摘要連結，傳給沒參加的同事。"],
];

export const html = `
  <div class="track">
    <div class="panel">
      <div class="copy">
        ${STEPS.map(([n, h, p]) => `<article class="step"><span class="n">${n}</span><h3>${h}</h3><p>${p}</p></article>`).join("")}
      </div>
      <div class="visual">
        ${STEPS.map(([n]) => `<div class="shot"><span>${n}</span></div>`).join("")}
      </div>
      <div class="dots">${STEPS.map(() => "<i></i>").join("")}</div>
    </div>
  </div>`;

export const css = `
  & { display: block; padding: 0; place-items: normal; }
  .track { height: 300vh; }
  .panel { position: relative; height: calc(100vh - var(--head-h, 0px)); max-width: 1000px; margin: 0 auto;
    padding: 0 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: center; }
  .copy, .visual { position: relative; height: 60%; }
  .step { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; }
  .n { font: 700 14px var(--mono); color: var(--muted); }
  h3 { margin: 6px 0 10px; font-size: clamp(30px, 5vw, 48px); line-height: 1.15; }
  .step p { margin: 0; color: var(--muted); max-width: 22em; }
  .shot { position: absolute; inset: 0; border-radius: 20px; display: grid; place-items: center;
    background: var(--placeholder); border: 1px solid var(--line); }
  .shot span { font: 700 72px var(--font); color: var(--num); }
  .dots { position: absolute; left: 24px; bottom: 24px; display: flex; gap: 8px; }
  .dots i { width: 28px; height: 4px; border-radius: 2px; background: var(--line); transition: background 0.2s; }
  .dots i.on { background: var(--fg); }
  @media (max-width: 720px) {
    .panel { grid-template-columns: 1fr; grid-template-rows: 1fr 1fr; gap: 16px; padding-top: 16px; padding-bottom: 48px; }
    .copy, .visual { height: 100%; }
  }
  /* Reduced motion: no pin, the three steps simply stack */
  [data-reduced] & .track { height: auto; }
  [data-reduced] & .panel { height: auto; display: block; padding: 48px 24px; }
  [data-reduced] & .copy, [data-reduced] & .visual { height: auto; }
  [data-reduced] & .step { position: static; margin-bottom: 32px; }
  [data-reduced] & .visual, [data-reduced] & .dots { display: none; }
  /* Before mount every step is readable; mount() stacks them for the scrub */
  &:not([data-mounted]) .step + .step, &:not([data-mounted]) .shot + .shot { opacity: 0; }
`;

const headH = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--head-h")) || 0;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const gsap = window.gsap;
  const steps = root.querySelectorAll(".step");
  const shots = root.querySelectorAll(".shot");
  const dots = root.querySelectorAll(".dots i");
  const ctx = gsap.context(() => {
    gsap.set([...steps].slice(1), { autoAlpha: 0, y: 30 });
    gsap.set([...shots].slice(1), { autoAlpha: 0, scale: 0.94 });
    const tl = gsap.timeline({
      defaults: { ease: "power2.inOut" },
      scrollTrigger: {
        trigger: root.querySelector(".track"),
        start: () => `top top+=${headH()}`,
        end: "bottom bottom",
        pin: root.querySelector(".panel"),
        pinSpacing: false,
        scrub: 0.5,
        invalidateOnRefresh: true,
        onUpdate: (self) => {
          const i = Math.min(steps.length - 1, Math.floor(self.progress * steps.length));
          dots.forEach((d, j) => d.classList.toggle("on", j === i));
        },
      },
    });
    for (let i = 1; i < steps.length; i++) {
      tl.to(steps[i - 1], { autoAlpha: 0, y: -30 }, i)
        .to(steps[i], { autoAlpha: 1, y: 0 }, i)
        .to(shots[i - 1], { autoAlpha: 0, scale: 1.04 }, i)
        .to(shots[i], { autoAlpha: 1, scale: 1 }, i);
    }
    tl.to({}, { duration: 0.6 });   // hold the last step before releasing the pin
    dots[0].classList.add("on");
  }, root);
  return () => ctx.revert();
}
