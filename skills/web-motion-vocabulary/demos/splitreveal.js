// splitreveal — Split Text Reveal
// Built from the GSAP SplitText docs (https://gsap.com/docs/v3/Plugins/SplitText/):
// split into lines, mask each line, and slide the lines up from below the mask.
// React Bits has a ready-made Split Text (https://reactbits.dev/text-animations/split-text);
// its code is not included here because its license forbids redistribution.

export const meta = {
  hint: "標題捲進畫面時一行一行浮上來；按 ↻ 再看一次",
  replay: true,
  libs: ["gsap", "ScrollTrigger", "SplitText"],
};

export const html = `
  <div class="hero">
    <p class="eyebrow">2026 春季發表</p>
    <h1 class="headline">把每一次捲動，<br>變成值得看完的故事</h1>
    <p class="sub">標題拆成一行一行，每一行從看不見的遮罩下方升上來。<br>總長不到 0.8 秒，安靜但有分量。</p>
  </div>`;

export const css = `
  .hero { width: min(860px, 100%); }
  .eyebrow { margin: 0 0 16px; font-size: 14px; letter-spacing: 0.08em; color: var(--muted); }
  .headline { margin: 0; font-size: clamp(34px, 7vw, 68px); line-height: 1.15; letter-spacing: -0.01em; }
  .sub { margin: 24px 0 0; color: var(--muted); max-width: 34em; }
`;

export function mount(root, { reduced }) {
  if (reduced) return () => {};
  const { gsap, SplitText } = window;
  const ctx = gsap.context(() => {
    // Chinese has no spaces between words, so split by characters and let SplitText
    // regroup them into visual lines; the mask hides each line until it slides up.
    SplitText.create(root.querySelector(".headline"), {
      type: "lines,chars",
      mask: "lines",
      onSplit: (self) => gsap.from(self.lines, {
        yPercent: 100,
        duration: 0.6,
        stagger: 0.08,
        ease: "power3.out",
        scrollTrigger: { trigger: self.lines[0], start: "top 85%", once: true },
      }),
    });
    gsap.from(root.querySelectorAll(".eyebrow, .sub"), {
      opacity: 0,
      duration: 0.6,
      delay: 0.25,
      ease: "power2.out",
      scrollTrigger: { trigger: root.querySelector(".headline"), start: "top 85%", once: true },
    });
  }, root);
  return () => ctx.revert();
}
