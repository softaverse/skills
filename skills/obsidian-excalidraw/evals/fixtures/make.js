// Synthetic fixtures for the generic evals (no real user data).
const fs = require('fs'), path = require('path');
const L = require(path.join(__dirname, '../../scripts/lib.js'));
const ST = require(path.join(__dirname, '../../scripts/styles.json'));
const st = (n, x = {}) => ({ ...ST[n], ...x });
const out = __dirname;
const save = (d, p) => fs.writeFileSync(path.join(out, p), L.serialize(d));

// fixture-arch: a requirements summary frame; base = last written by the skill, current = user added a note + renamed frame
{
  const d = L.create('x'), S = new L.Scene(d);
  const f = S.frame('需求摘要（草稿）', -40, -60, 10, 10); const o = { frameId: f.id };
  S.box('目標\n讓會員可在 Web 與 iOS 下單、付款、收到通知', 0, 0, 520, 90, st('note', o));
  S.box('非功能需求\n• 尖峰 500 TPS\n• 訂單資料保留 7 年', 560, 0, 400, 110, st('note', o));
  S.box('範圍外\n• 實體門市 POS', 0, 140, 520, 70, st('muted', o));
  S.fitFrame(f, 40);
  save(d, 'fixture-arch.base.excalidraw.md');
  const d2 = L.load(path.join(out, 'fixture-arch.base.excalidraw.md')), S2 = new L.Scene(d2);
  const fr = S2.findFrame('需求摘要'); fr.name = '需求摘要（v2）'; S2.bump(fr);
  S2.text('PM：金流要支援退款', 1060, 20, { fontSize: 20, color: '#e03131' });
  save(d2, 'fixture-arch.excalidraw.md');
}
// fixture-seq: an existing note with a small login flow
{
  const d = L.create('x'), S = new L.Scene(d);
  const f = S.frame('登入功能', -40, -60, 10, 10); const o = { frameId: f.id };
  const a = S.box('登入頁', 0, 0, 200, 70, st('ui', o));
  const b = S.box('選擇\nGoogle 登入', 300, 0, 200, 80, st('process', o));
  const c = S.box('登入完成\n進入首頁', 600, 0, 200, 80, st('success', o));
  S.arrow(a, b, { frameId: f.id }); S.arrow(b, c, { frameId: f.id });
  S.fitFrame(f, 40);
  save(d, 'fixture-seq.excalidraw.md');
}
console.log('ok');
