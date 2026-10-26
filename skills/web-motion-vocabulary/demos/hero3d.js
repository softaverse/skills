// hero3d — Interactive 3D Hero
// Built from the Three.js docs and examples (https://threejs.org/examples/): one mesh,
// two lights, rotating slowly and easing toward the pointer. Renders at most at 2× DPR,
// and releases the WebGL context when unmounted.

export const meta = {
  hint: "游標在畫面上移動，物件會跟著轉向——它持續佔用 GPU",
  heavy: true,
  libs: ["three"],
};

export const html = `
  <div class="hero">
    <div class="copy">
      <p class="eyebrow">Studio 2026</p>
      <h2>把想法做成<br>拿得起來的東西</h2>
      <p class="muted">右邊是即時運算的 3D 物件。手機上通常改成一張靜態圖。</p>
    </div>
    <div class="stage"><canvas aria-hidden="true"></canvas></div>
  </div>`;

export const css = `
  & { display: block; padding: 0; place-items: normal; }
  .hero { height: calc(100vh - var(--head-h, 0px)); min-height: 480px; max-width: 1100px; margin: 0 auto;
    padding: 0 24px; display: grid; grid-template-columns: 1fr 1fr; align-items: center; gap: 24px; }
  .eyebrow { margin: 0 0 8px; font: 600 13px var(--mono); letter-spacing: 0.2em; color: var(--muted); }
  h2 { margin: 0 0 12px; font-size: clamp(32px, 5vw, 56px); line-height: 1.15; }
  .stage { position: relative; height: 70%; }
  canvas { position: absolute; inset: 0; width: 100%; height: 100%; }
  @media (max-width: 720px) {
    .hero { grid-template-columns: 1fr; grid-template-rows: auto 1fr; padding-top: 32px; }
    .stage { height: 100%; }
  }
`;

export function mount(root, { reduced }) {
  const THREE = window.THREE;
  const canvas = root.querySelector("canvas");
  const dark = document.documentElement.dataset.theme === "dark";

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
  camera.position.set(0, 0, 7);

  const geometry = new THREE.TorusKnotGeometry(1.1, 0.36, 220, 32);
  const material = new THREE.MeshStandardMaterial({
    color: dark ? 0xd4d4d8 : 0x3f3f46, metalness: 0.35, roughness: 0.3,
  });
  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, dark ? 1.4 : 2.2));
  const key = new THREE.DirectionalLight(0xffffff, 2.5);
  key.position.set(3, 4, 5);
  scene.add(key);

  const resize = () => {
    const { clientWidth: w, clientHeight: h } = canvas;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  const ro = new ResizeObserver(resize);
  ro.observe(canvas);
  resize();

  // Ease toward the pointer: a little tilt, never a full spin.
  const target = { x: 0, y: 0 };
  const onMove = (e) => {
    target.y = (e.clientX / innerWidth - 0.5) * 1.2;
    target.x = (e.clientY / innerHeight - 0.5) * 0.8;
  };
  addEventListener("pointermove", onMove);

  let frame = 0;
  const start = performance.now();
  let last = start;
  const render = (now = performance.now()) => {
    const dt = (now - last) / 1000, elapsed = (now - start) / 1000;
    last = now;
    mesh.rotation.z += dt * 0.15;
    mesh.rotation.y += (target.y + elapsed * 0.2 - mesh.rotation.y) * 0.05;
    mesh.rotation.x += (target.x - mesh.rotation.x) * 0.05;
    renderer.render(scene, camera);
    if (!reduced) frame = requestAnimationFrame(render);   // reduced motion: one still frame
  };
  frame = requestAnimationFrame(render);

  return () => {
    cancelAnimationFrame(frame);
    removeEventListener("pointermove", onMove);
    ro.disconnect();
    geometry.dispose();
    material.dispose();
    renderer.dispose();
    renderer.forceContextLoss();
  };
}
