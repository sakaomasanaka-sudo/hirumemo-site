// 全ページをスマホ幅で開き、横はみ出しとJSエラーを確認する。使い方: リポジトリ直下で node tools/check.js
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const errs = []; let bad = 0;
  const files = fs.readdirSync('site').filter(f => f.endsWith('.html') && !f.startsWith('google'));
  for (const f of files) {
    for (const w of [390, 1100]) {
      const p = await b.newPage({ viewport: { width: w, height: 1200 } });
      p.on('pageerror', e => errs.push(f + ': ' + e.message));
      await p.route('**/*', r => r.request().url().startsWith('file://') ? r.continue() : r.fulfill({ status: 204, body: '' }));
      await p.goto('file://' + process.cwd() + '/site/' + f, { waitUntil: 'domcontentloaded' });
      await p.waitForTimeout(300);
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (ov > 0) { bad++; console.log('OVERFLOW', f, w, ov); }
      await p.close();
    }
  }
  console.log('pages', files.length, 'overflow', bad, 'errors', JSON.stringify(errs));
  await b.close(); process.exit(bad || errs.length ? 1 : 0);
})();
