// <id> — <English name>
// Source: the official example this demo is based on, its URL, and its license.
// Copy to demos/<id>.js and point the entry's Demo line at it.
//
// Rules (see runtime.js): mount() must undo everything it does; mounting and
// unmounting must not change the section's height; content stays readable when
// the effect never runs (hide things from mount(), not from css); anything pinned
// starts below the sticky heading:
//   const headH = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--head-h")) || 0;
//   ScrollTrigger.create({ trigger, pin: true, start: () => `top top+=${headH()}` });

export const meta = {
  hint: "說明怎麼操作，例如：往下滑",
  replay: false,          // true for one-shot effects: adds ↻ to the corner label
  heavy: false,           // true when it keeps the GPU busy: waits for a click
  keepAlive: false,       // true when it changes the whole page (smooth scroll): never unmounted
  libs: [],               // any of: motion, gsap, ScrollTrigger, SplitText, ScrambleTextPlugin, DrawSVGPlugin, lenis, lottie, three
};

export const html = `
  <div class="card">
    <h2>效果名稱</h2>
  </div>`;

// Plain CSS. It is nested under [data-demo="<id>"], so use `&` for the effect area itself.
// The area centers its content (display: grid; place-items: center). For full-width
// layouts use `& { display: block; padding: 0; place-items: normal; }`.
export const css = `
  h2 { margin: 0; }
`;

// Optional: CSS that cannot be nested, e.g. @keyframes <id>-name { … }
// export const globalCss = ``;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  // GSAP: wrap everything in gsap.context(() => { … }, root) and call ctx.revert() on cleanup,
  // which also kills its ScrollTriggers.
  return () => {};
}
