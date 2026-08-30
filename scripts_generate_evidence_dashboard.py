import json
from pathlib import Path
from html import escape
import shutil

RESULTS_PATH = Path('artifacts/test-results/results.json')
SCREENSHOTS_DIR = Path('artifacts/screenshots')
EVIDENCE_DIR = Path('artifacts/evidence-dashboard')
OUTPUT_PATH = EVIDENCE_DIR / 'index.html'
PACKAGED_SCREENSHOTS_DIR = EVIDENCE_DIR / 'screenshots'


def safe_text(value, default=''):
    return escape(str(value)) if value is not None else default


def load_results():
    if not RESULTS_PATH.exists():
        return {}
    return json.loads(RESULTS_PATH.read_text(encoding='utf-8'))


def build_test_cards(results):
    tests = results.get('tests', [])
    cards = []
    for test in tests:
        nodeid = test.get('nodeid', 'unknown')
        outcome = test.get('outcome', 'unknown')
        module = nodeid.split('::')[0] if '::' in nodeid else nodeid
        test_name = nodeid.split('::')[-1]
        screenshot_name = ''.join(c if c.isalnum() or c in '._-' else '_' for c in nodeid) + '.png'
        screenshot_path = SCREENSHOTS_DIR / screenshot_name
        screenshot_html = ''
        if screenshot_path.exists():
            screenshot_html = f'''<a class="shot-link" href="screenshots/{safe_text(screenshot_name)}" target="_blank">
                <img src="screenshots/{safe_text(screenshot_name)}" alt="{safe_text(test_name)} screenshot" loading="lazy" />
            </a>'''
        else:
            screenshot_html = '<div class="missing">Screenshot not available</div>'

        duration = test.get('call', {}).get('duration', 0)
        cards.append(f'''<div class="card">
            <div class="card-top">
                <div>
                    <div class="module">{safe_text(module)}</div>
                    <h3>{safe_text(test_name)}</h3>
                </div>
                <span class="pill {'pass' if outcome == 'passed' else 'other'}">{safe_text(outcome.title())}</span>
            </div>
            <div class="meta">Execution time: {duration:.3f}s</div>
            <div class="shot">{screenshot_html}</div>
            <div class="nodeid">{safe_text(nodeid)}</div>
        </div>''')
    return '\n'.join(cards)


def main():
    results = load_results()
    summary = results.get('summary', {})
    passed = summary.get('passed', 0)
    total = summary.get('total', 0)
    collected = summary.get('collected', total)
    failed = max(total - passed, 0)
    pass_rate = int((passed / total) * 100) if total else 0

    if EVIDENCE_DIR.exists():
        shutil.rmtree(EVIDENCE_DIR)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGED_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    if SCREENSHOTS_DIR.exists():
        for screenshot in SCREENSHOTS_DIR.glob('*.png'):
            shutil.copy2(screenshot, PACKAGED_SCREENSHOTS_DIR / screenshot.name)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SauceDemo Evidence Dashboard</title>
  <style>
    :root {{
      --bg: #07111f;
      --panel: #0f172a;
      --panel-2: #111c34;
      --text: #e6eef8;
      --muted: #9fb0c7;
      --border: rgba(148,163,184,.18);
      --success: #22c55e;
      --accent: #60a5fa;
      --shadow: 0 18px 50px rgba(0,0,0,.35);
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Inter, Arial, sans-serif; color: var(--text); background: linear-gradient(135deg,#020617,#07111f 55%,#0f172a); }}
    .wrap {{ max-width: 1400px; margin: 0 auto; padding: 28px 20px 50px; }}
    .hero {{ background: linear-gradient(135deg, rgba(37,99,235,.25), rgba(34,197,94,.14)); border: 1px solid var(--border); border-radius: 24px; padding: 28px; box-shadow: var(--shadow); }}
    h1 {{ margin: 0 0 8px; font-size: 34px; }}
    p {{ margin: 0; color: var(--muted); }}
    .stats {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 16px; margin-top: 22px; }}
    .stat {{ background: rgba(15,23,42,.78); border: 1px solid var(--border); border-radius: 20px; padding: 20px; box-shadow: var(--shadow); }}
    .label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .9px; margin-bottom: 10px; }}
    .value {{ font-size: 32px; font-weight: 800; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 18px; margin-top: 24px; }}
    .card {{ background: rgba(15,23,42,.86); border: 1px solid var(--border); border-radius: 18px; padding: 16px; box-shadow: var(--shadow); }}
    .card-top {{ display: flex; justify-content: space-between; gap: 12px; align-items: flex-start; margin-bottom: 10px; }}
    .module {{ color: var(--accent); font-size: 12px; margin-bottom: 6px; word-break: break-word; }}
    h3 {{ margin: 0; font-size: 16px; line-height: 1.35; word-break: break-word; }}
    .pill {{ display: inline-block; padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 800; }}
    .pill.pass {{ color: #dcfce7; background: rgba(34,197,94,.14); border: 1px solid rgba(34,197,94,.28); }}
    .pill.other {{ color: #fff; background: rgba(148,163,184,.18); border: 1px solid rgba(148,163,184,.28); }}
    .meta {{ color: var(--muted); font-size: 13px; margin-bottom: 12px; }}
    .shot {{ background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.06); border-radius: 14px; min-height: 220px; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
    .shot img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .shot-link {{ display: block; width: 100%; height: 100%; }}
    .nodeid {{ color: var(--muted); font-size: 12px; margin-top: 12px; word-break: break-word; }}
    .missing {{ color: var(--muted); font-size: 14px; padding: 16px; }}
    .footer {{ margin-top: 22px; color: var(--muted); font-size: 13px; }}
    @media (max-width: 1100px) {{ .grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); }} .stats {{ grid-template-columns: repeat(2, minmax(0,1fr)); }} }}
    @media (max-width: 700px) {{ .grid, .stats {{ grid-template-columns: 1fr; }} h1 {{ font-size: 28px; }} }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>SauceDemo Test Evidence Dashboard</h1>
      <p>Visual evidence report generated automatically from Playwright + pytest results and captured success screenshots.</p>
      <div class="stats">
        <div class="stat"><div class="label">Collected</div><div class="value">{collected}</div></div>
        <div class="stat"><div class="label">Passed</div><div class="value" style="color: var(--success);">{passed}</div></div>
        <div class="stat"><div class="label">Failed</div><div class="value">{failed}</div></div>
        <div class="stat"><div class="label">Pass Rate</div><div class="value">{pass_rate}%</div></div>
      </div>
    </section>

    <section class="grid">
      {build_test_cards(results)}
    </section>

    <div class="footer">Open any screenshot tile to view the full-size evidence image.</div>
  </div>
</body>
</html>'''

    OUTPUT_PATH.write_text(html, encoding='utf-8')
    print(f'Generated {OUTPUT_PATH}')


if __name__ == '__main__':
    main()
