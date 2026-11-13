"""Build an Italian static course without altering any upstream file."""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import html
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import sys
import zipfile
from types import SimpleNamespace
from urllib.parse import quote, urlparse

import markdown
import nbformat
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from catalog import TRACKS
from feedback import translations as feedback_translations
from code_translation import translate_notebook
from colab import generate as generate_colab, launch_url
from translation_checks import audit_cell
from course_images import load_images, replace_images, URL_PATTERN

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'ai_lab'
sys.path.insert(0, str(ROOT / 'notebooks'))
from nb_utils.lesson_preprocessor import LearnLessonPreprocessor  # noqa: E402


def is_core(entry):
    """Identify the seven ML and six DL modules in the introductory curricula."""
    return entry['index'] < {'machine_learning': 7, 'deep_learning_intro': 6}.get(entry['track'], 0)


def read_translations(track):
    source = (LAB / 'content/it' / f'{track}.txt').read_text()
    chunks = re.split(r'^@@ (\S+)\n', source, flags=re.M)
    result = {}
    for key, value in zip(chunks[1::2], chunks[2::2]):
        if key in result:
            raise ValueError(f'Duplicate translation: {track}/{key}')
        result[key] = value.strip() + '\n'
    return result


class ItalianPreprocessor(LearnLessonPreprocessor):
    """Reuse Kaggle macro processing with local navigation and Italian boilerplate."""

    def add_header_and_footer(self, cells):
        return None

    def YOURTURN(self, **kwargs):
        return f'# Ora tocca a te\n\nProva l’[esercizio pratico]({self.lesson.exercise.forking_url}) su {self.lesson.topic}.'

    def KEEP_GOING(self, **kwargs):
        if not hasattr(self.lesson, 'next'):
            return '## Corso completato\n\n[Torna all’inizio](../../index.html).'
        target = self.lesson.next
        return f'# Prosegui\n\nSei pronto per **[{target.topic}]({target.tutorial.url})**.'

    def NEXT_NOTEBOOK_URL(self, **kwargs):
        if self.nb_meta.type == 'tutorial' and hasattr(self.lesson, 'exercise'):
            return self.lesson.exercise.forking_url
        if hasattr(self.lesson, 'next'):
            return self.lesson.next.tutorial.url
        return '../../index.html'

    def SUBMIT_TO_COMP(self, **kwargs):
        return ('1. Comincia premendo **Save Version** nell’angolo in alto a destra della finestra. Si aprirà una finestra di dialogo.\n'
                '2. Assicurati che sia selezionato **Save and Run All**, poi premi **Save**.\n'
                '3. Comparirà una finestra in basso a sinistra nel notebook. Al termine dell’esecuzione, premi il numero a destra di **Save Version**: apparirà un elenco di versioni sulla destra. Premi i tre puntini **(...)** accanto alla versione più recente e seleziona **Open in Viewer**. Entrerai nella modalità di visualizzazione della stessa pagina; scorri verso il basso per tornare a queste istruzioni.\n'
                '4. Apri la scheda **Data** vicino alla parte superiore dello schermo. Seleziona il file da inviare e premi **Submit** per inviare i risultati alla classifica.\n\n'
                'Hai inviato correttamente la tua soluzione alla competizione!\n\n'
                'Se vuoi continuare a migliorare le prestazioni, seleziona **Edit** in alto a destra. Puoi quindi modificare il codice e ripetere il procedimento. C’è molto margine di miglioramento e salirai in classifica man mano che lavori.\n')


def get_entries():
    entries = []
    for track, settings in TRACKS.items():
        meta = runpy.run_path(str(ROOT / 'notebooks' / track / 'track_meta.py'))
        registered = {n['filename']: n for n in meta['notebooks']}
        for path in (ROOT / 'notebooks' / track / 'raw').glob('*.ipynb'):
            item = registered.get(path.name)
            index = item['lesson_idx'] if item else 9
            kind = item['type'] if item else ('exercise' if path.stem.startswith('ex') else 'tutorial')
            title, objective = settings['topics'][index]
            entries.append(dict(track=track, source=path, stem=path.stem, index=index,
                                kind=kind, title=title, objective=objective,
                                page=f'corsi/{track}/{path.stem}.html',
                                metadata=item or {}, historical=track == 'deep_learning' or 'automl' in path.stem,
                                special='tpu' in path.stem))
    return sorted(entries, key=lambda e: (list(TRACKS).index(e['track']), e['index'], e['kind'] == 'exercise'))


def check_source_lock(entries):
    inventory = json.loads((LAB / 'reports/inventory.json').read_text())
    locked = {e['source']: e['sha256'] for group in inventory['tracks'].values() for e in group}
    for entry in entries:
        relative = str(entry['source'].relative_to(ROOT))
        digest = hashlib.sha256(entry['source'].read_bytes()).hexdigest()
        if locked.get(relative) != digest:
            raise ValueError(f'Source changed; review translation and inventory before building: {relative}')
    for relative, expected in inventory.get('support_hashes', {}).items():
        path = ROOT/relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Original pipeline changed; review rendering and update inventory: {relative}')


def make_resources(entry, entries):
    group = [e for e in entries if e['track'] == entry['track']]
    lessons = []
    for i, (title, _) in enumerate(TRACKS[entry['track']]['topics']):
        lesson = SimpleNamespace(topic=title)
        for item in [e for e in group if e['index'] == i]:
            url = item['stem'] + '.html'
            setattr(lesson, item['kind'], SimpleNamespace(url=url, forking_url=url))
        if not hasattr(lesson, 'tutorial'):
            lesson.tutorial = SimpleNamespace(url='../../index.html')
        lessons.append(lesson)
    for a, b in zip(lessons, lessons[1:]):
        a.next = b
        b.prev = a
    if is_core(entry):
        last = 6 if entry['track'] == 'machine_learning' else 5
        if hasattr(lessons[last], 'next'):
            del lessons[last].next
        if entry['track'] == 'machine_learning':
            lessons[last].next = SimpleNamespace(
                topic=TRACKS['deep_learning_intro']['title'],
                tutorial=SimpleNamespace(url='../deep_learning_intro/tut1.html'))
    return dict(track_meta=SimpleNamespace(lessons=lessons, course_name=TRACKS[entry['track']]['title'],
                                         course_url='../../index.html'),
                lesson=lessons[entry['index']], nb_meta=SimpleNamespace(type=entry['kind']),
                track_cfg={'testing': False, 'development': False, 'daily': False})


def render_markdown(text):
    # Protect math before Markdown consumes backslashes and underscores.
    formulas = []
    def stash(match):
        formulas.append(match.group())
        return f'AILABMATHPLACEHOLDER{len(formulas)-1}END'
    text = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<![\\\w])\$[^\n$]+?\$', stash, text, flags=re.S)
    output = markdown.markdown(text, extensions=['fenced_code', 'tables', 'toc', 'codehilite', 'footnotes', 'md_in_html'],
                               extension_configs={'codehilite': {'guess_lang': False}})
    for index, formula in enumerate(formulas):
        output = output.replace(f'AILABMATHPLACEHOLDER{index}END', html.escape(formula))
    return output


def normalize_notebook_links(nb, entry, entries):
    # Notebook navigation must work independently from its HTML page.
    known = {e['stem']+'.html': f"{e['track']}/{e['stem']}.html" for e in entries if e['track']==entry['track']}
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            cell.source = re.sub(r'\]\(([^)]+\.html)\)',
                                 lambda m: m.group(0) if urlparse(m[1]).scheme else (
                                     '](' + CONFIG['site_url'] + 'corsi/' + known[m[1]] + ')' if m[1] in known
                                     else '](' + CONFIG['site_url'] + 'index.html)'), cell.source)


def notebook_content(nb, entry, outdir, images=None):
    parts = []
    notes = dict(re.findall(r'^\[\^([^\]]+)\]: (.*)$', '\n'.join(cell.source for cell in nb.cells if cell.cell_type == 'markdown'), re.M))
    used_notes = set()
    for number, cell in enumerate(nb.cells):
        if cell.get('id') in {'ai-lab-local-guide', 'ai-lab-local-setup'}:
            continue
        if cell.cell_type == 'markdown':
            source = re.sub(r'^\[\^[^\]]+\]: .*$', '', cell.source, flags=re.M)
            if images is not None:
                source = replace_images(source, images)
            for key, definition in notes.items():
                if f'[^{key}]' in source and key not in used_notes:
                    source += f'\n\n[^{key}]: {definition}\n'
                    used_notes.add(key)
            parts.append(render_markdown(source))
        elif cell.cell_type == 'code':
            parts.append('<div class="code-cell">'+highlight(cell.source, PythonLexer(), HtmlFormatter())+'</div>')
            # Keep embedded source figures; never execute upstream code during the site build.
            for index, output in enumerate(cell.get('outputs', [])):
                data = output.get('data', {})
                if 'image/png' in data:
                    name = f"{entry['track']}-{entry['stem']}-{number}-{index}.png"
                    (outdir/'assets'/name).write_bytes(base64.b64decode(data['image/png']))
                    parts.append(f'<figure><img loading="lazy" src="../../assets/{name}" alt="Grafico conservato dal notebook originale"></figure>')
                elif 'text/plain' in data:
                    value = data['text/plain']
                    parts.append('<details class="output"><summary>Output salvato nell’originale</summary><pre>'+html.escape(value)+'</pre></details>')
    return '\n'.join(parts)


def status_text(entry):
    if entry['historical']:
        return 'Archivio storico: codice conservato, esecuzione attuale non verificata. API, video e servizi esterni possono essere cambiati.'
    if entry['special']:
        return 'Approfondimento: richiede TPU, dati remoti e ambiente Kaggle. Esecuzione non verificata; escluso dalle attività obbligatorie.'
    return 'Notebook Kaggle tradotto con esercizi e dati originali. I dataset sono scaricabili: consulta la guida ai dati per prepararli localmente. Le esecuzioni su servizi remoti non sono state verificate in questa sessione.'


LOCAL_SETUP = '''# Locate the extracted student bundle or the cloned repository.
from pathlib import Path
import os
import sys

if not Path('/kaggle/input').is_dir():
    project_root = next((path for path in [Path.cwd(), *Path.cwd().parents]
                         if (path / 'learntools/core').is_dir()
                         and (path / 'ai_lab/datasets.json').is_file()), None)
    if project_root is None:
        raise FileNotFoundError('Extract the complete AI Lab student bundle and open this notebook inside it.')
    sys.path.insert(0, str(project_root))
    runtime = project_root / 'ai_lab/runtime'
    runtime.mkdir(exist_ok=True)
    os.chdir(runtime)
    os.environ['LEARN_USE_KAGGLE_SDK'] = 'False'
    from learntools.core import tracking
    tracking.track = lambda event: None
    from ai_lab.tools.feedback import install
    install()
    print('Working directory:', runtime)
    print('Original datasets expected in:', project_root / 'ai_lab/input')
'''


def relative_link(page, target):
    return os.path.relpath(target, str(Path(page).parent)).replace(os.sep, '/')


def local_notebook_url(filename):
    return f'http://127.0.0.1:8888/lab/tree/{quote(filename)}'


def local_notebook_button(filename):
    if not CONFIG.get('_development'):
        return ''
    return f'<a class="button secondary" href="{local_notebook_url(filename)}">Apri il notebook locale</a>'


def derived_pages(entries, output):
    pages = {}
    intro = nbformat.read(LAB/'notebooks/00-python-essenziale.ipynb', as_version=4)
    translate_notebook(intro)
    intro_url = launch_url(CONFIG, '00-python-essenziale.ipynb')
    intro_html = f'<div class="actions"><a class="button" href="{intro_url}">Apri in Colab</a>{local_notebook_button("00-python-essenziale.ipynb")}<a class="button secondary" download href="notebooks/00-python-essenziale.ipynb">Scarica notebook</a></div>'
    if CONFIG.get('_development'):
        intro_html += ('<p>Anteprima locale: il pulsante Colab apre la versione pubblicata su GitHub. '
                       'Avvia Jupyter con <code>./jupyter-start.sh</code> per aprire i notebook locali.</p>')
    intro_html += notebook_content(intro, {'track': 'python', 'stem': 'intro'}, output)
    pages['python.html'] = ('Python per il corso', intro_html, 'school')
    for cell in intro.cells:
        if cell.cell_type == 'markdown':
            cell.source = re.sub(r'\]\(([^)]+\.html)\)',
                                 lambda match: '](' + CONFIG['site_url'] + match[1] + ')',
                                 cell.source)
    nbformat.write(intro, output/'notebooks/00-python-essenziale.ipynb')
    extras = '# Materiali aggiuntivi\n\nQuesti contenuti sono conservati per consultazione e non fanno parte dei tredici moduli dei due corsi introduttivi.\n\n'
    for track, setting in TRACKS.items():
        group = [entry for entry in entries if entry['track'] == track and not is_core(entry)]
        if not group:
            continue
        extras += f'## {setting["title"]}\n\n'
        for entry in group:
            label = ('Esercizio: ' if entry['kind'] == 'exercise' else '') + entry['title']
            extras += f'- [{label}]({entry["page"]})\n'
        extras += '\n'
    extras += '## Attività originali AI Lab\n\n- [Notebook e laboratori aggiuntivi](laboratori.html).\n- [Progetti facoltativi](progetti.html).\n\nLe attività AI Lab sono materiale originale del progetto scolastico, distinto dalle lezioni Kaggle.\n'
    pages['aggiuntivi.html'] = ('Materiali aggiuntivi', render_markdown(extras), 'school')
    execution_path = LAB/'reports/execution.json'
    report = json.loads(execution_path.read_text()) if execution_path.exists() else {'results': []}
    states = {record['notebook']:record for record in report['results']}
    lab_text = '# Notebook e laboratori\n\nI notebook seguenti sono attività originali AI Lab, aggiuntive rispetto ai corsi Kaggle. Contengono esempi completi e attività da svolgere modificando il codice.\n\nPer i notebook dei corsi Kaggle usa il menu delle lezioni; per l’installazione e i dati, la [guida all’esecuzione](esecuzione.html).\n\n'
    lab_text += '| Notebook | Dipendenze per i calcoli | Verifica disponibile |\n| --- | --- | --- |\n'
    for path in sorted((LAB/'notebooks').glob('*.ipynb')):
        if path.name == '00-python-essenziale.ipynb':
            continue
        nb = json.loads(path.read_text())
        title = nb['cells'][0]['source'].splitlines()[0].removeprefix('# ')
        deps = ', '.join(nb['metadata']['ai_lab']['dependencies']) or 'Python standard'
        record = states.get(path.name, {})
        status = {'passed':'Celle Python eseguite' if report.get('mode')=='python_cells' else 'Kernel Jupyter eseguito',
                  'not_run':'Non eseguito: dipendenze mancanti', 'failed':'Esecuzione fallita'}.get(record.get('status'),'Non eseguito')
        lab_text += f'| [{title}](notebooks/{path.name}) | {deps} | {status} |\n'
    lab_text += '\nIl notebook 08 usa il file JSON creato dal notebook 07 nella stessa cartella. I laboratori 01–03 usano Python standard per ricostruire alberi ed ensemble; il laboratorio 04 usa NumPy. [Dettagli delle verifiche](verifiche.html).'
    pages['laboratori.html'] = ('Notebook e laboratori',render_markdown(lab_text),'school')
    checks = '# Stato delle verifiche\n\nQuesta pagina distingue ciò che è stato eseguito da ciò che richiede ancora un ambiente compatibile. Non è una certificazione dei servizi esterni.\n\n'
    checks += f'## Copertura dei sorgenti\n\n{len(entries)} notebook convertiti. La build verifica che ogni cella Markdown abbia una traduzione e che gli hash dei sorgenti corrispondano all’inventario. Riusa il preprocessor Kaggle per espandere le macro senza pulire o modificare gli originali. Le traduzioni sono adattamenti didattici, non trascrizioni integrali dei video esterni.\n\n'
    checks += '## Esecuzioni dei laboratori\n\n'
    checks += ('Modalità registrata: **'+report.get('mode','nessuna')+'**. `python_cells` esegue le celle in ordine con uno spazio dei nomi nuovo per notebook, ma non verifica il kernel o la UI Jupyter. `jupyter_kernel` usa nbclient con un kernel reale.\n\n')
    checks += '| File | Esito | Dettaglio |\n| --- | --- | --- |\n'
    for record in report['results']:
        status = {'passed':'Superato','not_run':'Non eseguito','failed':'Fallito'}[record['status']]
        checks += f'| {record["notebook"]} | {status} | {record.get("reason", str(record.get("seconds", ""))+" s")} |\n'
    reference = LAB/'assets/reference-model.json'
    if reference.exists():
        model = json.loads(reference.read_text())
        checks += f'\nIl progetto di riferimento ha ottenuto accuracy test **{model["test_accuracy"]:.3f}**, contro baseline **{model["baseline_accuracy"]:.3f}**, su {model["test_size"]} esempi sintetici. Questi risultati non descrivono capacità su fiori reali. [Parametri e protocollo](assets/reference-model.json).\n'
    ui_report = LAB/'reports/ui-checks.json'
    if ui_report.is_file():
        checks += '\n## Funzioni dell’interfaccia\n\nVerificati con un DOM locale: ricerca sotto il prefisso del repository, cambio e memorizzazione del tema, apertura/chiusura del menu, focus da tastiera nel contesto mobile, formule KaTeX, messaggi per risorse non disponibili e modulo di inferenza del modello già salvato. Non è un controllo grafico del layout e non esegue addestramento.\n'
    checks += '\n## Limiti e controlli da completare\n\nGli originali Kaggle non sono stati eseguiti con i dataset remoti. I notebook Colab sono predisposti con caricamento dei dati e adattatore Keras; download, cache e integrità dei file sono controllati localmente. La sessione autenticata Colab non è stata eseguita qui. Invii a competizioni, servizi AutoML e TPU non sono verificati. Le immagini dei notebook, formule, font, CSS, ricerca e interfaccia sono risorse locali del sito; i video esterni richiedono rete. La verifica visiva desktop/mobile non è stata completata: il server locale e Chromium sono impediti dai permessi di questo ambiente.\n\nLe esecuzioni con TensorFlow e scikit-learn restano da svolgere in un ambiente compatibile. Il workflow Pages compila e controlla i link prima di rendere disponibile un artefatto. La pubblicazione manuale richiede autorizzazione ed è documentata nel README.\n'
    pages['verifiche.html'] = ('Stato delle verifiche',render_markdown(checks),'school')
    return pages


def build(output, development=False):
    global CONFIG
    CONFIG = json.loads((LAB/'config.json').read_text())
    CONFIG['_development'] = development
    if not CONFIG['site_url'].endswith('/'):
        raise ValueError('site_url must end with /')
    site_address = urlparse(CONFIG['site_url'])
    if (site_address.scheme != 'https' or not site_address.netloc
            or site_address.query or site_address.fragment):
        raise ValueError('site_url must be an absolute HTTPS URL without query or fragment')
    if site_address.path != CONFIG['base_path']:
        raise ValueError('base_path must match the path of site_url, including the trailing /')
    entries = get_entries()
    check_source_lock(entries)
    feedback_translations()
    output.mkdir(parents=True, exist_ok=True)
    (output/'.nojekyll').write_text('')
    shutil.copytree(LAB/'assets', output/'assets', dirs_exist_ok=True)
    light_syntax = HtmlFormatter(style='friendly').get_style_defs(['.highlight', '.codehilite'])
    dark_syntax = HtmlFormatter(style='github-dark').get_style_defs(
        ['html[data-theme="dark"] .highlight', 'html[data-theme="dark"] .codehilite'])
    (output/'assets/syntax.css').write_text(light_syntax + '\n' + dark_syntax + '\n')
    css_versions = {name: hashlib.sha256((output/'assets'/name).read_bytes()).hexdigest()[:12]
                    for name in ('style.css', 'syntax.css')}
    (output/'notebooks').mkdir(exist_ok=True)
    for path in (LAB/'notebooks').glob('*.ipynb'):
        notebook = nbformat.read(path, as_version=4)
        translate_notebook(notebook)
        nbformat.write(notebook, output/'notebooks'/path.name)
    shutil.copy2(ROOT/'LICENSE', output/'LICENSE-Kaggle.txt')
    shutil.copy2(LAB/'reports/inventory.json', output/'inventory.json')
    if (LAB/'reports/data-inventory.json').is_file():
        shutil.copy2(LAB/'reports/data-inventory.json', output/'data-inventory.json')
    pages = {}
    coverage = []
    translation_audit = []
    course_images = load_images()
    referenced_images = set()
    for track in TRACKS:
        translations = read_translations(track)
        expected = {f"{e['stem']}:{i}" for e in entries if e['track']==track
                    for i,c in enumerate(nbformat.read(e['source'], as_version=4).cells) if c.cell_type=='markdown'}
        if expected != set(translations):
            raise ValueError(f'Translation coverage mismatch in {track}: {expected ^ set(translations)}')
        for entry in [e for e in entries if e['track']==track]:
            nb = nbformat.read(entry['source'], as_version=4)
            # Assign stable IDs to older notebooks without touching source files.
            for i, cell in enumerate(nb.cells):
                cell.id = f"cell-{i}"
                if cell.cell_type == 'markdown':
                    key = f"{entry['stem']}:{i}"
                    translated = translations[key]
                    referenced_images.update(URL_PATTERN.findall(translated))
                    audit = audit_cell(cell.source, translated)
                    translation_audit.append({'track': track, 'cell': key, **audit})
                    if audit['errors']:
                        raise ValueError(f"Translation integrity {track}/{key}: {audit['errors']}")
                    cell.source = translated
            nb, _ = ItalianPreprocessor().preprocess(nb, make_resources(entry, entries))
            nb.nbformat_minor = 5
            nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                           'language_info': {'name': 'python'},
                           'ai_lab': {'source': str(entry['source'].relative_to(ROOT)),
                                      'source_sha256': hashlib.sha256(entry['source'].read_bytes()).hexdigest(),
                                      'execution_status': 'not_verified', 'license': 'Apache-2.0', 'language': 'it'}}
            intro = f"# {entry['title']}\n\n"
            if not is_core(entry):
                intro += '> **Nota AI Lab — materiale aggiuntivo.** ' + status_text(entry) + '\n\n'
            nb.cells.insert(0, nbformat.v4.new_markdown_cell(intro, id='ai-lab-context'))
            if not entry['historical'] and not entry['special']:
                nb.cells.insert(1, nbformat.v4.new_markdown_cell('## Preparazione\n\nEsegui questa cella prima della lezione. Mantieni il notebook nella cartella del pacchetto studenti.', id='ai-lab-local-guide'))
                setup = LOCAL_SETUP
                if entry['track'] == 'deep_learning_intro':
                    setup += "\n    from ai_lab.tools.keras_compat import install as install_keras_compat\n    install_keras_compat()\n"
                nb.cells.insert(2, nbformat.v4.new_code_cell(setup,id='ai-lab-local-setup'))
            translate_notebook(nb)
            label = ('Esercizio: ' if entry['kind']=='exercise' else '')+entry['title']
            name = entry['track']+'-'+entry['stem']+'.ipynb'
            colab_button = f'<a class="button" href="{launch_url(CONFIG, name)}">Apri in Colab</a>' if is_core(entry) else ''
            content = f'<div class="actions">{colab_button}{local_notebook_button(name)}<a class="button secondary" download href="../../notebooks/{name}">Scarica notebook</a><a class="button secondary" href="../../esecuzione.html">Come eseguirlo</a></div>'
            content += notebook_content(nb, entry, output, course_images)
            # Source links within the translated lesson remain in their original positions.
            source_relative = str(entry['source'].relative_to(ROOT))
            commit = json.loads((LAB/'reports/inventory.json').read_text())['upstream_commit']
            content += f'<p><small>Fonte: <a href="{CONFIG["repository"]}/blob/{commit}/{source_relative}">notebook originale Kaggle</a> · <a href="../../attribuzioni.html">Autori e licenze</a></small></p>'
            normalize_notebook_links(nb, entry, entries)
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    cell.outputs=[]
                    cell.execution_count=None
                elif cell.cell_type == 'markdown':
                    # Data URIs work in both the standalone notebook and Colab,
                    # including original HTML <img> figures and animated GIFs.
                    cell.source = replace_images(cell.source, course_images, notebook=True)
            nbformat.validate(nb)
            nbformat.write(nb, output/'notebooks'/name)
            pages[entry['page']] = (label, content, entry['track'])
            coverage.append({'source': source_relative, 'page': entry['page'], 'notebook':name,
                             'markdown_cells': len([k for k in translations if k.startswith(entry['stem']+':')]),
                             'status':'translated_adaptation', 'execution':'not_verified'})
    if referenced_images != set(course_images):
        raise ValueError(f'Image archive mismatch: {referenced_images ^ set(course_images)}')
    for source in (LAB/'content/school').glob('*.md'):
        if source.name == 'dataset.md':
            continue  # Maintenance instructions remain in the repository.
        text = source.read_text()
        title = text.splitlines()[0].removeprefix('# ')
        pages[source.stem+'.html'] = (title, render_markdown(text), 'school')
    pages.update(derived_pages(entries, output))
    colab_report = generate_colab(output, [entry for entry in entries if is_core(entry)], CONFIG)
    (LAB/'reports/colab.json').write_text(json.dumps(colab_report, indent=2)+'\n')
    # Remove obsolete generated pages when the published curriculum changes.
    for stale in output.rglob('*.html'):
        if stale.relative_to(output).as_posix() not in pages:
            stale.unlink()
    for page, (title, body, section) in pages.items():
        dest = output/page
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(shell(page, title, body, section, entries, css_versions))
    index = [{'title':title, 'url':page, 'text':re.sub('<[^>]+>', ' ', body)}
             for page,(title,body,_) in pages.items()]
    (output/'search.json').write_text(json.dumps(index, ensure_ascii=False))
    (output/'downloads').mkdir(exist_ok=True)
    packaged_data = []
    dataset_manifest = json.loads((LAB/'datasets.json').read_text())
    for key, dataset in dataset_manifest.items():
        source = LAB/'input'/dataset['directory']
        if source.is_dir():
            files = [path for path in source.rglob('*') if path.is_file() and path.name != '.gitignore']
            if files:
                target = output/'datasets'/dataset['directory']
                shutil.copytree(source, target, dirs_exist_ok=True)
                notice = (dataset.get('attribution', dataset['slug'])+'\n'+dataset['url']+
                          '\nLicense: '+dataset.get('license', 'Not embedded in the downloaded archive; consult the original source.')+
                          '\n'+dataset.get('license_url', dataset['url'])+
                          '\nLicense review status: '+dataset.get('redistribution_status','not-verified')+
                          '\nOriginal data; no modifications by AI Lab. Dataset terms are separate from the Apache-2.0 code license.\n')
                (target/'ATTRIBUTION.txt').write_text(notice)
                packaged_data.extend((path, f'ai_lab/input/{dataset["directory"]}/{path.relative_to(target)}')
                                     for path in target.rglob('*') if path.is_file())
                for alias in dataset.get('aliases', []):
                    path = LAB/'input'/alias
                    if path.is_file():
                        packaged_data.append((path, f'ai_lab/input/{alias}'))
    with zipfile.ZipFile(output/'downloads/ai-lab-studenti.zip','w',zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted((output/'notebooks').glob('*.ipynb')):
            folder = ('preparazione' if path.name == '00-python-essenziale.ipynb' else
                      'kaggle' if any(path.name.startswith(track+'-') for track in TRACKS) else 'aggiuntivi')
            bundle.write(path, f'ai-lab-studenti/ai_lab/notebooks/{folder}/{path.name}')
        for path in sorted((ROOT/'learntools').rglob('*')):
            relative = path.relative_to(ROOT/'learntools')
            relevant = str(relative) == '__init__.py' or relative.parts[0] in {'core', *TRACKS}
            if relevant and path.is_file() and '__pycache__' not in path.parts and path.suffix in ('.py','.md'):
                bundle.write(path, 'ai-lab-studenti/'+str(path.relative_to(ROOT)))
        for relative in ['LICENSE','ai_lab/LICENSE','ai_lab/NOTICE','ai_lab/datasets.json','ai_lab/tools/datasets.py','ai_lab/tools/feedback.py','ai_lab/localization/it.json','ai_lab/requirements/kaggle-local.txt', 'ai_lab/input/.gitignore', 'ai_lab/runtime/.gitignore']:
            bundle.write(ROOT/relative,'ai-lab-studenti/'+relative)
        for path in sorted((LAB/'assets/kaggle-images').iterdir()):
            if path.is_file():
                bundle.write(path, 'ai-lab-studenti/ai_lab/assets/kaggle-images/'+path.name)
        for path in sorted((LAB/'requirements').glob('*.txt')):
            if path.name != 'kaggle-local.txt':
                bundle.write(path,'ai-lab-studenti/'+str(path.relative_to(ROOT)))
        bundle.write(LAB/'content/school/dataset.md','ai-lab-studenti/LEGGIMI-DATI.md')
        for path, relative in packaged_data:
            bundle.write(path,'ai-lab-studenti/'+relative)
    (output/'.nojekyll').touch()
    (LAB/'reports/coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
    (LAB/'reports/translation-checks.json').write_text(json.dumps({
        'reference': 'Locked Kaggle source notebooks in reports/inventory.json',
        'scope': 'All source Markdown cells, including additional and historical notebooks',
        'checks': ['source links', 'inline images', 'navigation macros', 'heading hierarchy',
                   'fenced code tokens excluding translated comments', 'major shortening'],
        'limitation': 'Structural checks do not certify semantic fidelity; bilingual review is required.',
        'notebooks': len(entries), 'cells': len(translation_audit),
        'errors': [], 'details': translation_audit,
    }, ensure_ascii=False, indent=2)+'\n')
    print(f'Built {len(pages)} pages and {len(list((output/"notebooks").glob("*.ipynb")))} notebooks in {output}')


def shell(page, title, body, section, entries, css_versions):
    rel = lambda target: relative_link(page, target)
    body = re.sub(r'(<a\b[^>]*\bhref="https://colab\.research\.google\.com/[^"]*")',
                  r'\1 target="_blank" rel="noopener noreferrer"', body)
    nav = ''
    for key,label in [('index.html','Introduzione'),('python.html','Python per il corso')]:
        nav += f'<a {"aria-current=page" if key==page else ""} href="{rel(key)}">{label}</a>'
    for track, setting in TRACKS.items():
        group = [e for e in entries if e['track'] == track and is_core(e)]
        if not group:
            continue
        nav += f'<details {"open" if section==track else ""}><summary>{setting["short"]}</summary>'
        for entry in group:
            name = ('↳ Esercizio' if entry['kind']=='exercise' else entry['title'])
            nav += f'<a {"aria-current=page" if page==entry["page"] else ""} href="{rel(entry["page"])}">{entry["index"]+1:02d} · {name}</a>'
        nav += '</details>'
    nav += f'<a {"aria-current=page" if page=="aggiuntivi.html" else ""} href="{rel("aggiuntivi.html")}">Materiali aggiuntivi</a>'
    core_pages = ['python.html'] + [e['page'] for e in entries if is_core(e)]
    ordered = core_pages if page in core_pages else [
        e['page'] for e in entries if e['track'] == section and not is_core(e)]
    pager = ''
    crumb = ''
    if page in ordered:
        i = ordered.index(page)
        crumb = f'{"Corso completo" if page in core_pages else "Materiali aggiuntivi"} · {i+1} di {len(ordered)}'
        if i:
            pager += f'<a href="{rel(ordered[i-1])}">← Precedente</a>'
        if i+1<len(ordered):
            pager += f'<a href="{rel(ordered[i+1])}">Successiva →</a>'
    return f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · {html.escape(CONFIG['title'])}</title>
<meta name="description" content="{html.escape(CONFIG['description'],quote=True)}">
<link rel="canonical" href="{CONFIG['site_url']}{page}">
<link rel="icon" href="{rel('assets/favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{rel('assets/style.css')}?v={css_versions['style.css']}"><link rel="stylesheet" href="{rel('assets/syntax.css')}?v={css_versions['syntax.css']}">
<link rel="stylesheet" href="{rel('assets/vendor/katex/katex.min.css')}">
<script defer src="{rel('assets/vendor/katex/katex.min.js')}"></script>
<script defer src="{rel('assets/vendor/katex/auto-render.min.js')}"></script>
<script defer src="{rel('assets/app.js')}"></script></head>
<body data-root="{rel('index.html').removesuffix('index.html') or './'}"><a class="skip" href="#contenuto">Vai al contenuto</a>
<header><a class="brand" href="{rel('index.html')}"><span>{html.escape(CONFIG['title'])}</span></a>
<div class="header-actions"><button id="menu" aria-expanded="false" aria-controls="sidebar">Indice</button><button id="theme" aria-label="Cambia tema" aria-pressed="false">Tema scuro</button></div></header>
<aside id="sidebar"><label for="search">Cerca nel corso</label><input id="search" type="search" placeholder="Cerca…" autocomplete="off"><div id="search-status" role="status"></div><div id="results"></div><nav aria-label="Navigazione del corso">{nav}</nav><p class="teacher">{html.escape(CONFIG['teacher'])}</p></aside>
<main id="contenuto">{'<div class="breadcrumb">'+crumb+'</div>' if crumb else ''}<article>{body}</article><nav class="pager" aria-label="Lezione precedente e successiva">{pager}</nav>
<footer><p>Traduzione italiana e riorganizzazione dei corsi originali Kaggle Learn · Progetto indipendente AI Lab.</p><a href="{rel('attribuzioni.html')}">Autori, fonti e licenze</a> · <a href="{rel('verifiche.html')}">Verifiche tecniche</a></footer></main></body></html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=LAB/'build')
    parser.add_argument('--dev', action='store_true', help='Add links for the local development environment')
    args = parser.parse_args()
    destination = args.output.resolve()
    if destination in (ROOT, LAB) or ROOT.is_relative_to(destination):
        parser.error('Output must be a dedicated build directory')
    build(destination, development=args.dev)
