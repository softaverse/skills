// linedraw — Line Draw
// Built from the GSAP DrawSVGPlugin docs (https://gsap.com/docs/v3/Plugins/DrawSVGPlugin/):
// scrub the path's drawn length with the scroll; each step lights up as the line reaches it.

export const meta = { hint: "往下滑：線會跟著捲動畫出來，串起每一個步驟", libs: ["gsap", "ScrollTrigger", "DrawSVGPlugin"] };

const NODES = [
  [300, 40, "01 註冊帳號", "start"],
  [120, 260, "02 匯入資料", "start"],
  [480, 480, "03 邀請團隊", "end"],
  [300, 700, "04 開始協作", "start"],
];
const PATH = "M300 40 C300 150 120 150 120 260 C120 370 480 370 480 480 C480 590 300 590 300 700";

export const html = `
  <div class="wrap">
    <h2>四步開始使用</h2>
    <svg viewBox="0 0 600 760" role="img" aria-label="註冊、匯入、邀請、協作四個步驟">
      <path class="rail" d="${PATH}"/>
      <path class="line" d="${PATH}"/>
      ${NODES.map(([x, y, label, side]) => `
        <g class="node">
          <circle cx="${x}" cy="${y}" r="12"/>
          <text x="${side === "end" ? x - 26 : x + 26}" y="${y + 6}" text-anchor="${side}">${label}</text>
        </g>`).join("")}
    </svg>
  </div>`;

export const css = `
  .wrap { width: min(600px, 100%); text-align: center; }
  h2 { margin: 0 0 24px; font-size: clamp(26px, 5vw, 40px); }
  svg { width: 100%; height: auto; overflow: visible; }
  .rail { fill: none; stroke: var(--line); stroke-width: 3; }
  .line { fill: none; stroke: var(--fg); stroke-width: 3; stroke-linecap: round; }
  .node circle { fill: var(--section-bg); stroke: var(--fg); stroke-width: 3; transition: fill 0.3s; }
  .node text { font: 600 22px var(--font); fill: var(--fg); transition: opacity 0.3s; }
  &[data-mounted] .node:not(.on) circle { stroke: var(--line); }
  &[data-mounted] .node:not(.on) text { opacity: 0.35; }
  .node.on circle { fill: var(--fg); }
`;

export function mount(root, { reduced }) {
  const nodes = root.querySelectorAll(".node");
  if (reduced) {
    nodes.forEach((n) => n.classList.add("on"));   // the whole line, every step lit
    return () => nodes.forEach((n) => n.classList.remove("on"));
  }
  const gsap = window.gsap;
  const ctx = gsap.context(() => {
    gsap.fromTo(root.querySelector(".line"), { drawSVG: "0%" }, {
      drawSVG: "100%",
      ease: "none",
      scrollTrigger: {
        trigger: root.querySelector("svg"),
        start: "top 70%",
        end: "bottom 60%",
        scrub: 0.5,
        // The nodes sit at equal arc lengths, so progress tells which ones the line has reached.
        onUpdate: (self) => nodes.forEach((n, i) =>
          n.classList.toggle("on", self.progress >= i / (nodes.length - 1) - 0.02)),
      },
    });
    nodes[0].classList.add("on");
  }, root);
  return () => {
    ctx.revert();
    nodes.forEach((n) => n.classList.remove("on"));
  };
}
