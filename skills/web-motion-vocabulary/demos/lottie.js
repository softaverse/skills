// lottie — Lottie Animation
// Played with lottie-web (https://airbnb.io/lottie/). The animation itself,
// _shared/check.json, is hand-written for this skill: a ring draws itself with a small
// pop, then the check mark draws in. One second, played once.

export const meta = {
  hint: "按「送出」：成功時播放一段預先做好的打勾動畫；Lottie 只負責播放，不會回應游標",
  libs: ["lottie"],
};

export const html = `
  <div class="card form">
    <div class="ask">
      <h3>訂閱每週精選</h3>
      <p class="muted">每週一封，隨時可以取消。</p>
      <div class="row"><input type="email" value="you@example.com" aria-label="Email"><button type="button" class="send">送出</button></div>
    </div>
    <div class="done" hidden>
      <div class="anim" aria-hidden="true"></div>
      <h3>訂閱成功</h3>
      <button type="button" class="again">再試一次</button>
    </div>
  </div>`;

export const css = `
  .form { width: min(420px, 100%); padding: 32px; text-align: center; min-height: 290px; display: grid; place-items: center; }
  h3 { margin: 0 0 4px; font-size: 20px; }
  .ask p { margin: 0 0 20px; }
  .row { display: flex; gap: 8px; }
  input { flex: 1; min-width: 0; font: inherit; padding: 10px 14px; border-radius: 10px; border: 1px solid var(--line);
    background: var(--bg); color: var(--fg); }
  .send { font: inherit; font-weight: 600; padding: 10px 18px; border-radius: 10px; border: 0;
    background: var(--fg); color: var(--bg); cursor: pointer; }
  .anim { width: 120px; height: 120px; margin: 0 auto 8px; }
  .again { margin-top: 12px; font: inherit; font-size: 13px; color: var(--muted); background: none; border: 0;
    text-decoration: underline; cursor: pointer; }
  [hidden] { display: none; }
`;

const ANIMATION = new URL("./_shared/check.json", import.meta.url);
let data = null;

// The JSON bakes in a dark stroke; recolor it to the page's text color so it works on both themes.
function tinted(json) {
  const rgb = getComputedStyle(document.documentElement).getPropertyValue("--fg").trim();
  const hex = /^#([0-9a-f]{6})$/i.exec(rgb);
  if (!hex) return json;
  const c = [0, 2, 4].map((i) => parseInt(hex[1].slice(i, i + 2), 16) / 255).concat(1);
  const copy = structuredClone(json);
  copy.layers.forEach((l) => l.shapes.forEach((g) => g.it?.forEach((it) => { if (it.ty === "st") it.c.k = c; })));
  return copy;
}

export function mount(root, { reduced }) {
  const ask = root.querySelector(".ask");
  const done = root.querySelector(".done");
  const box = root.querySelector(".anim");
  let anim = null;

  const show = async () => {
    data ??= await fetch(ANIMATION).then((r) => r.json());
    ask.hidden = true;
    done.hidden = false;
    anim?.destroy();
    anim = window.lottie.loadAnimation({
      container: box, renderer: "svg", loop: false, autoplay: !reduced, animationData: tinted(data),
    });
    if (reduced) anim.goToAndStop(data.op - 1, true);   // reduced motion: the finished frame
  };
  const reset = () => {
    anim?.destroy();
    anim = null;
    done.hidden = true;
    ask.hidden = false;
  };

  const onClick = (ev) => {
    if (ev.target.closest(".send")) show();
    if (ev.target.closest(".again")) reset();
  };
  root.addEventListener("click", onClick);

  return () => {
    root.removeEventListener("click", onClick);
    anim?.destroy();
  };
}
