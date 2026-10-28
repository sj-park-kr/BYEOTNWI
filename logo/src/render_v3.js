const { chromium } = require('playwright');
const fs = require('fs');
const D = __dirname + '/../';
const [nx, cy] = process.argv.slice(2).map(Number);
(async () => {
  const b = await chromium.launch();
  const shot = async (svg, out, scale, clip) => {
    const p = await b.newPage({ viewport: { width: 1600, height: 560 }, deviceScaleFactor: scale });
    await p.setContent(`<html><body style="margin:0">${fs.readFileSync(D + svg, 'utf8')}</body></html>`);
    await p.screenshot({ path: D + out, clip });
    await p.close();
  };
  await shot('byeonnwi_a_gap_v3.svg', 'byeonnwi_main_v3.png', 1);
  await shot('byeonnwi_a_gap_light_v3.svg', 'byeonnwi_a_gap_light_v3.png', 1);
  await shot('byeonnwi_a_gap_v3.svg', 'byeonnwi_detail_v3.png', 3, { x: nx - 240, y: cy - 190, width: 480, height: 360 });
  await b.close();
})();
