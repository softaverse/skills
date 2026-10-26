// aurora — Aurora Background
// A small WebGL fragment shader: soft color bands drifting across the top of the Hero.
// React Bits has a ready-made Aurora (https://reactbits.dev/backgrounds/aurora, built on OGL);
// its code is not included here because its license forbids redistribution, so this one
// is written from scratch. It renders at reduced resolution and stops when unmounted.

export const meta = {
  hint: "背景的色彩會一直緩慢流動——注意它持續佔用 GPU，切到深色看看差別",
  heavy: true,
};

export const html = `
  <div class="hero">
    <canvas aria-hidden="true"></canvas>
    <div class="copy">
      <p class="eyebrow">AI Workspace</p>
      <h2>讓靈感自己流動</h2>
      <p class="muted">背景是一段即時運算的 WebGL 動畫。文字疊在上面時，要確認對比度夠。</p>
    </div>
  </div>`;

export const css = `
  & { display: block; padding: 0; place-items: normal; }
  .hero { position: relative; height: calc(100vh - var(--head-h, 0px)); min-height: 480px; overflow: hidden;
    display: grid; place-items: center; text-align: center; }
  canvas { position: absolute; inset: 0; width: 100%; height: 100%; }
  .copy { position: relative; padding: 0 24px; }
  .eyebrow { margin: 0 0 8px; font: 600 13px var(--mono); letter-spacing: 0.2em; color: var(--muted); }
  h2 { margin: 0 0 12px; font-size: clamp(34px, 7vw, 64px); line-height: 1.15; }
`;

const VERT = `attribute vec2 p; void main() { gl_Position = vec4(p, 0.0, 1.0); }`;
const FRAG = `
precision mediump float;
uniform vec2 res;
uniform float t;
uniform float dark;
float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1, 0)), f.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), f.x), f.y);
}
void main() {
  vec2 uv = gl_FragCoord.xy / res;
  float x = uv.x * 2.5;
  float wave = noise(vec2(x, t * 0.12)) * 0.6 + noise(vec2(x * 2.3, t * 0.2)) * 0.3;
  float center = 0.62 + (wave - 0.45) * 0.45;
  float band = smoothstep(0.32, 0.0, abs(uv.y - center)) * (0.55 + 0.45 * noise(vec2(x * 3.0, t * 0.3)));
  vec3 a = vec3(0.32, 0.15, 1.0), b = vec3(0.49, 1.0, 0.40), c = vec3(0.10, 0.70, 1.0);
  vec3 col = mix(mix(a, c, uv.x), b, noise(vec2(x * 0.7 + t * 0.08, 1.7)) * 0.8);
  float alpha = band * mix(0.55, 0.9, dark);
  gl_FragColor = vec4(col * alpha, alpha);
}`;

export function mount(root, { reduced }) {
  const canvas = root.querySelector("canvas");
  const gl = canvas.getContext("webgl", { premultipliedAlpha: true, antialias: false });
  if (!gl) return () => {};

  const shader = (type, src) => {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    return s;
  };
  const prog = gl.createProgram();
  gl.attachShader(prog, shader(gl.VERTEX_SHADER, VERT));
  gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, FRAG));
  gl.linkProgram(prog);
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const uRes = gl.getUniformLocation(prog, "res");
  const uT = gl.getUniformLocation(prog, "t");
  gl.uniform1f(gl.getUniformLocation(prog, "dark"), document.documentElement.dataset.theme === "dark" ? 1 : 0);

  // Half resolution: the bands are blurry anyway, and it quarters the GPU work.
  const resize = () => {
    canvas.width = Math.max(1, Math.round(canvas.clientWidth * 0.5));
    canvas.height = Math.max(1, Math.round(canvas.clientHeight * 0.5));
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(uRes, canvas.width, canvas.height);
  };
  const ro = new ResizeObserver(resize);
  ro.observe(canvas);
  resize();

  const start = performance.now();
  let frame = 0;
  const draw = (now) => {
    gl.uniform1f(uT, (now - start) / 1000 + 4);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    if (!reduced) frame = requestAnimationFrame(draw);   // reduced motion: one still frame
  };
  frame = requestAnimationFrame(draw);

  return () => {
    cancelAnimationFrame(frame);
    ro.disconnect();
    gl.getExtension("WEBGL_lose_context")?.loseContext();
  };
}
