/* Local navigation, search and mathematics. No account or analytics required. */
(() => {
  const root = document.body.dataset.root;
  const themeButton = document.getElementById('theme');
  const setTheme = (dark) => {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    themeButton.setAttribute('aria-pressed', String(dark));
    themeButton.textContent = dark ? 'Tema chiaro' : 'Tema scuro';
  };
  let preference;
  try { preference = localStorage.getItem('ai-lab-theme'); } catch (_) { /* Storage may be disabled. */ }
  setTheme(preference ? preference === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches);
  themeButton.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    setTheme(dark);
    try { localStorage.setItem('ai-lab-theme', dark ? 'dark' : 'light'); } catch (_) { /* Use session theme. */ }
  });
  const menu = document.getElementById('menu');
  const sidebar = document.getElementById('sidebar');
  menu.addEventListener('click', () => {
    const open = sidebar.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      sidebar.classList.remove('open');
      menu.setAttribute('aria-expanded', 'false');
      if (matchMedia('(max-width: 720px)').matches) menu.focus();
    }
  });
  let indexPromise;
  let searchVersion = 0;
  const search = document.getElementById('search');
  const results = document.getElementById('results');
  const status = document.getElementById('search-status');
  search.addEventListener('input', async () => {
    const version = ++searchVersion;
    const query = search.value.trim().toLocaleLowerCase('it');
    results.replaceChildren();
    status.textContent = '';
    if (query.length < 2) return;
    try {
      indexPromise ??= fetch(root + 'search.json').then((response) => {
        if (!response.ok) throw new Error('Search unavailable');
        return response.json();
      }).catch((error) => { indexPromise = undefined; throw error; });
      const index = await indexPromise;
      if (version !== searchVersion) return;
      const terms = query.split(/\s+/);
      const hits = index.filter((entry) => terms.every((term) => (entry.title + ' ' + entry.text).toLocaleLowerCase('it').includes(term)));
      status.textContent = `${hits.length} risultati; mostrati i primi 12.`;
      for (const hit of hits.slice(0, 12)) {
        const link = document.createElement('a');
        link.href = root + hit.url;
        link.textContent = hit.title;
        results.append(link);
      }
    } catch (_) { status.textContent = 'Ricerca non disponibile. Usa l’indice del corso.'; }
  });
  if (typeof renderMathInElement === 'function') {
    renderMathInElement(document.querySelector('article'), {
      delimiters: [{left:'$$',right:'$$',display:true},{left:'\\[',right:'\\]',display:true},
                   {left:'\\(',right:'\\)',display:false},{left:'$',right:'$',display:false}],
      throwOnError: false,
      trust: false,
    });
  }
  document.querySelectorAll('article img').forEach((element) => {
    element.loading = 'lazy';
    element.addEventListener('error', () => {
      const caption = document.createElement('p');
      caption.className = 'notice';
      caption.textContent = `Immagine esterna non disponibile: ${element.alt || 'figura del sorgente'}. Il collegamento è conservato fra i riferimenti.`;
      element.replaceWith(caption);
    }, {once: true});
  });
  const demo = document.getElementById('model-demo');
  if (demo) {
    fetch(root + 'assets/reference-model.json').then((response) => {
      if (!response.ok) throw new Error('Model unavailable');
      return response.json();
    }).then((model) => {
      const update = () => {
        const values = [...demo.querySelectorAll('input')].map((input) => Number(input.value));
        let score = model.bias;
        values.forEach((value, index) => { score += ((value - model.mean[index]) / model.scale[index]) * model.weights[index]; });
        const probability = 1 / (1 + Math.exp(-score));
        const label = probability >= 0.5 ? 'beta' : 'alfa';
        demo.querySelector('output').textContent = `Classe prevista: ${label}. Probabilità stimata di beta: ${(100 * probability).toFixed(1)}%.`;
        demo.querySelectorAll('[data-value]').forEach((label, index) => { label.textContent = values[index].toFixed(1); });
      };
      demo.addEventListener('input', update);
      update();
    }).catch(() => { demo.querySelector('output').textContent = 'Modello non disponibile. Esegui il notebook di riferimento per rigenerarlo.'; });
  }
})();
