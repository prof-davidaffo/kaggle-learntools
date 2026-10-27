/* Exercise the actual generated interface without network or a graphical browser. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {JSDOM} = require('jsdom');

const lab = path.resolve(__dirname, '..');
const build = path.join(lab, 'build');
const origin = 'https://ai-lab.local/kaggle-learntools/';
const results = [];
const tick = () => new Promise(resolve => setImmediate(resolve));

function openPage(name, mobile = false, unavailable = false) {
  const dom = new JSDOM(fs.readFileSync(path.join(build, name), 'utf8'), {
    url: origin + name, runScripts: 'outside-only', pretendToBeVisual: true,
  });
  const window = dom.window;
  window.matchMedia = query => ({matches: query.includes('max-width') && mobile});
  window.fetch = async value => {
    if (unavailable) return {ok: false};
    const url = new URL(value, window.location.href);
    assert.ok(url.href.startsWith(origin), 'Local resources must preserve the project prefix');
    const filename = path.resolve(build, decodeURIComponent(url.pathname.slice('/kaggle-learntools/'.length)));
    assert.ok(filename.startsWith(build + path.sep), 'Resource escaped build directory');
    return {ok: fs.existsSync(filename), json: async () => JSON.parse(fs.readFileSync(filename, 'utf8'))};
  };
  for (const filename of ['vendor/katex/katex.min.js', 'vendor/katex/auto-render.min.js', 'app.js']) {
    window.eval(fs.readFileSync(path.join(build, 'assets', filename), 'utf8'));
  }
  return dom;
}

async function check() {
  for (const mobile of [false, true]) {
    const dom = openPage('index.html', mobile);
    const window = dom.window;
    const document = window.document;
    document.querySelector('#theme').click();
    assert.equal(document.documentElement.dataset.theme, 'dark');
    assert.equal(window.localStorage.getItem('ai-lab-theme'), 'dark');
    assert.equal(document.querySelector('#theme').getAttribute('aria-pressed'), 'true');
    document.querySelector('#menu').click();
    assert.equal(document.querySelector('#menu').getAttribute('aria-expanded'), 'true');
    document.dispatchEvent(new window.KeyboardEvent('keydown', {key: 'Escape'}));
    assert.equal(document.querySelector('#menu').getAttribute('aria-expanded'), 'false');
    if (mobile) assert.equal(document.activeElement.id, 'menu');
    const search = document.querySelector('#search');
    search.value = 'validazione';
    search.dispatchEvent(new window.Event('input'));
    await tick(); await tick();
    assert.ok(document.querySelectorAll('#results a').length > 0);
    assert.ok([...document.querySelectorAll('#results a')].every(link => link.href.startsWith(origin)));
    search.value = '';
    search.dispatchEvent(new window.Event('input'));
    assert.equal(document.querySelectorAll('#results a').length, 0);
    results.push({check: 'search_theme_navigation', media_context: mobile ? 'mobile' : 'desktop', status: 'passed'});
    window.close();
  }

  const math = openPage('corsi/deep_learning_intro/tut1.html');
  assert.ok(math.window.document.querySelectorAll('.katex').length > 0);
  assert.equal(math.window.document.querySelectorAll('.katex-error').length, 0);
  const image = math.window.document.querySelector('article img');
  image.dispatchEvent(new math.window.Event('error'));
  assert.ok(math.window.document.querySelector('article').textContent.includes('Immagine esterna non disponibile'));
  results.push({check: 'local_math_and_image_fallback', status: 'passed'});
  math.window.close();

  const failure = openPage('index.html', false, true);
  const search = failure.window.document.querySelector('#search');
  search.value = 'validazione';
  search.dispatchEvent(new failure.window.Event('input'));
  await tick(); await tick();
  assert.match(failure.window.document.querySelector('#search-status').textContent, /Ricerca non disponibile/);
  results.push({check: 'search_failure_message', status: 'passed'});
  failure.window.close();

  const example = openPage('progetto-tabellare.html');
  await tick(); await tick();
  assert.match(example.window.document.querySelector('output').textContent, /70\.5%/);
  const inputs = example.window.document.querySelectorAll('#model-demo input');
  inputs[0].value = '0.5'; inputs[1].value = '0.2';
  inputs[0].dispatchEvent(new example.window.Event('input', {bubbles: true}));
  assert.match(example.window.document.querySelector('output').textContent, /Classe prevista: alfa/);
  results.push({check: 'saved_example_inference_interface', status: 'passed', note: 'Uses existing parameters; no training.'});
  example.window.close();
}

check().then(() => {
  const report = {mode: 'jsdom', note: 'Functional DOM checks only; no graphical layout or screenshot validation.', results};
  fs.writeFileSync(path.join(lab, 'reports/ui-checks.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
}).catch(error => { console.error(error); process.exitCode = 1; });
