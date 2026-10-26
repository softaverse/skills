// Builds one continuous page out of demo modules and keeps it honest:
// each section mounts a screen before it is reached and is cleaned up once it is
// far away, so nothing runs out of sight. Each section's heading sticks to the top
// and carries its replay and details controls.
//
// page.html?title=…&group=A｜…&ids=reveal,stagger&group=B｜…&ids=magnet&reduced=1&theme=dark
//
// A demo module (demos/<id>.js) exports:
//   meta  { hint, replay?, heavy?, keepAlive?, libs?: ["motion" | "gsap" | "ScrollTrigger" | "lenis" | "three" | …] }
//         keepAlive: never unmounted once started — for effects on the whole page (smooth scroll)
//   html  the section's markup
//   css   plain CSS; it is nested under [data-demo="<id>"], so it cannot leak
//   globalCss?  CSS that cannot be nested, e.g. @keyframes — prefix its names with the id
//   mount(root, { reduced }) → cleanup()   start the effect; undo everything it did
// Mounting and unmounting must not change the section's height: layout never jumps.
// Each section's heading sticks to the top; its height is the CSS variable --head-h,
// so anything pinned must start below it rather than at the very top.

const LIBS = {
  motion: "https://cdn.jsdelivr.net/npm/motion@12.23.12/dist/motion.js",
  gsap: "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js",
  ScrollTrigger: "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/ScrollTrigger.min.js",
  SplitText: "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/SplitText.min.js",
  ScrambleTextPlugin: "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/ScrambleTextPlugin.min.js",
  DrawSVGPlugin: "https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/DrawSVGPlugin.min.js",
  lenis: "https://cdn.jsdelivr.net/npm/lenis@1.3.26/dist/lenis.min.js",
  lottie: "https://cdn.jsdelivr.net/npm/lottie-web@5.13.0/build/player/lottie_light.min.js",
  // ES module only: imported, then exposed as window.THREE like the script-tag libraries
  three: { module: "https://cdn.jsdelivr.net/npm/three@0.186.1/build/three.module.js", global: "THREE" },
};
const NEEDS = { ScrollTrigger: ["gsap"], SplitText: ["gsap"], ScrambleTextPlugin: ["gsap"], DrawSVGPlugin: ["gsap"] };

const loading = new Map();
function loadLib(name) {
  if (!loading.has(name)) {
    loading.set(name, (async () => {
      for (const dep of NEEDS[name] || []) await loadLib(dep);
      const lib = LIBS[name];
      if (lib.module) {
        window[lib.global] = await import(lib.module);
        return;
      }
      await new Promise((resolve, reject) => {
        const s = document.createElement("script");
        s.src = LIBS[name];
        s.onload = resolve;
        s.onerror = () => reject(new Error(`failed to load ${name}`));
        document.head.append(s);
      });
      if (window.gsap && window[name] && name !== "gsap") window.gsap.registerPlugin(window[name]);
    })());
  }
  return loading.get(name);
}

const params = new URLSearchParams(location.search);
const reduced = params.has("reduced") || matchMedia("(prefers-reduced-motion: reduce)").matches;
if (reduced) document.documentElement.dataset.reduced = "";
if (params.get("theme") === "dark") document.documentElement.dataset.theme = "dark";

const splitName = (name) => {
  const m = /^(.*?)\s*\((.+)\)$/.exec(name);
  return m ? [m[1], m[2]] : [name, ""];
};
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const rich = (s) => esc(s)
  .replace(/`([^`]+)`/g, "<code>$1</code>")
  .replace(/https?:\/\/[^\s，。、）)]+/g, (u) => `<a href="${u}" target="_blank" rel="noopener">${u}</a>`);

// ---- page structure -------------------------------------------------------

const groups = [];
for (const [key, value] of params) {
  if (key === "group") groups.push({ label: value, ids: [] });
  if (key === "ids") {
    if (!groups.length) groups.push({ label: "", ids: [] });
    groups.at(-1).ids.push(...value.split(",").map((s) => s.trim()).filter(Boolean));
  }
}

const vocab = await fetch("/vocab.json").then((r) => (r.ok ? r.json() : {})).catch(() => ({}));
const page = document.getElementById("page");
const title = params.get("title") || "動畫效果";
const multi = groups.reduce((n, g) => n + g.ids.length, 0) > 1;

if (multi) {
  page.insertAdjacentHTML("beforeend",
    `<header class="demo-intro"><div><h1>${esc(title)}</h1><p>往下滑，每一段是一個效果・目前在看哪一個，看頂端的標題${reduced ? "・減少動態模式" : ""}</p></div></header>`);
}

// Each effect is a chapter: a numbered heading that sticks to the top while the
// chapter is on screen, then the body the module renders into. Backgrounds alternate so the eye feels
// where one effect ends and the next begins.
const total = groups.reduce((n, g) => n + g.ids.length, 0);
const sections = [];
for (const group of groups) {
  if (group.label) page.insertAdjacentHTML("beforeend", `<div class="demo-group"><h2>${esc(group.label)}</h2></div>`);
  for (const id of group.ids) {
    const n = sections.length + 1;
    const v = vocab[id] || { name: id, fields: {} };
    const [zh, en] = splitName(v.name);
    const f = v.fields || {};
    const tool = (f.工具 || "").split("；")[0].replace(/`/g, "");
    const rows = ["感受", "適合", "注意", "工具", "成本", "手機", "減少動態", "來源"]
      .filter((k) => f[k]).map((k) => `<dt>${k}</dt><dd>${rich(f[k])}</dd>`).join("");
    const el = document.createElement("section");
    el.className = "demo-section" + (n % 2 ? "" : " alt");
    el.innerHTML = `
      <header class="demo-head">
        <span class="num">${String(n).padStart(2, "0")}<small>/${String(total).padStart(2, "0")}</small></span>
        <div class="title"><h2>${esc(zh)}${en ? ` <span class="en">${esc(en)}</span>` : ""}</h2><p class="hint"></p></div>
        ${tool ? `<span class="tool">${esc(tool)}</span>` : ""}
        <div class="actions">
          <button type="button" data-act="replay" hidden>↻ 重播</button>
          <button type="button" data-act="more" aria-expanded="false">細節</button>
        </div>
        <div class="demo-more" hidden><p>${rich(v.def || "")}</p><dl>${rows}</dl></div>
      </header>
      <div class="demo-body" data-demo="${esc(id)}"></div>`;
    page.append(el);
    sections.push({ id, n, el, body: el.querySelector(".demo-body"), mod: null, cleanup: null });
  }
}

if (multi) {
  page.insertAdjacentHTML("beforeend",
    `<footer class="demo-end"><p>到底了・<a href="#" onclick="scrollTo({top:0});return false" style="color:inherit">回到頂端</a></p></footer>`);
}

// ---- modules --------------------------------------------------------------

async function prepare(s) {
  try {
    s.mod = await import(`../${s.id}.js`);
  } catch {
    s.body.innerHTML = `<p class="demo-missing">「${esc(vocab[s.id]?.name || s.id)}」的 demo 尚未製作——標題右側「細節」裡有官方範例連結</p>`;
    return;
  }
  const style = document.createElement("style");
  style.textContent = `[data-demo="${s.id}"] {\n${s.mod.css || ""}\n}\n${s.mod.globalCss || ""}`;
  document.head.append(style);
  await Promise.all((s.mod.meta?.libs || []).map(loadLib));
  s.el.querySelector(".demo-head .hint").textContent = s.mod.meta?.hint || "";
  s.el.querySelector("[data-act=replay]").hidden = !s.mod.meta?.replay;
  idle(s);
}

function idle(s) {
  if (s.mod.meta?.heavy) {
    s.body.innerHTML = `<div class="demo-heavy"><p>這個效果會一直佔用 GPU，點了才啟動</p><button type="button">▶ 啟動</button></div>`;
    s.body.querySelector("button").addEventListener("click", () => mount(s));
  } else {
    s.body.innerHTML = s.mod.html;
  }
}

function mount(s) {
  if (!s.mod || s.cleanup) return;
  s.body.innerHTML = s.mod.html;
  s.cleanup = s.mod.mount(s.body, { reduced }) || (() => {});
  s.body.dataset.mounted = "";
}

function unmount(s) {
  if (!s.cleanup || s.mod.meta?.keepAlive) return;
  s.cleanup();
  s.cleanup = null;
  delete s.body.dataset.mounted;
  idle(s);
}

await Promise.all(sections.map(prepare));

// Pinned effects start below the sticky heading (see template.js for the ScrollTrigger start).
const publishHeadHeight = () => {
  const head = document.querySelector(".demo-head");
  if (head) document.documentElement.style.setProperty("--head-h", `${head.offsetHeight}px`);
};
publishHeadHeight();
addEventListener("resize", publishHeadHeight);

// Mount a screen ahead of the viewport; clean up three screens away.
const near = new IntersectionObserver((entries) => entries.forEach((en) => {
  const s = sections.find((x) => x.el === en.target);
  if (en.isIntersecting && s.mod && !s.mod.meta?.heavy) mount(s);
}), { rootMargin: "100% 0px" });
const far = new IntersectionObserver((entries) => entries.forEach((en) => {
  if (!en.isIntersecting) unmount(sections.find((x) => x.el === en.target));
}), { rootMargin: "300% 0px" });
sections.forEach((s) => { near.observe(s.el); far.observe(s.el); });

// ---- heading controls -----------------------------------------------------

function setOpen(s, open) {
  s.el.querySelector(".demo-more").hidden = !open;
  s.el.querySelector("[data-act=more]").setAttribute("aria-expanded", String(open));
  s.el.querySelector("[data-act=more]").textContent = open ? "收起" : "細節";
}

document.addEventListener("click", (ev) => {
  const btn = ev.target.closest("[data-act]");
  const s = btn && sections.find((x) => x.el.contains(btn));
  // A click anywhere outside an open details panel closes it.
  sections.forEach((x) => { if (x !== s && !x.el.querySelector(".demo-more").contains(ev.target)) setOpen(x, false); });
  if (!s) return;
  if (btn.dataset.act === "more") setOpen(s, s.el.querySelector(".demo-more").hidden);
  if (btn.dataset.act === "replay") { s.cleanup?.(); s.cleanup = null; mount(s); }
});
