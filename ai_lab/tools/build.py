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
from urllib.parse import urlparse

import markdown
import nbformat
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

from catalog import TRACKS
from feedback import translations as feedback_translations
from code_translation import translate_notebook
from colab import generate as generate_colab, launch_url

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
        return f'## Ora prova tu\n\n[Apri l’esercizio]({self.lesson.exercise.forking_url}).'

    def KEEP_GOING(self, **kwargs):
        if not hasattr(self.lesson, 'next'):
            return '## Corso completato\n\n[Torna al programma](../../catalogo.html).'
        target = self.lesson.next
        return f'## Prosegui\n\n[{target.topic}]({target.tutorial.url}).'

    def NEXT_NOTEBOOK_URL(self, **kwargs):
        if self.nb_meta.type == 'tutorial' and hasattr(self.lesson, 'exercise'):
            return self.lesson.exercise.forking_url
        if hasattr(self.lesson, 'next'):
            return self.lesson.next.tutorial.url
        return '../../catalogo.html'

    def SUBMIT_TO_COMP(self, **kwargs):
        return ('La procedura storica richiedeva **Save Version → Save and Run All → Save**, '
                'poi l’apertura della versione con **Open in Viewer** e l’invio del CSV dalla '
                'scheda **Data** o **Output** con **Submit**. Richiede account, regole accettate '
                'e ambiente Kaggle. Interfaccia e invio attuali non verificati da AI Lab.')


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
            lesson.tutorial = SimpleNamespace(url='../../catalogo.html')
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
                                         course_url='../../catalogo.html'),
                lesson=lessons[entry['index']], nb_meta=SimpleNamespace(type=entry['kind']),
                track_cfg={'testing': False, 'development': False, 'daily': False})


def render_markdown(text):
    # Protect math before Markdown consumes backslashes and underscores.
    formulas = []
    def stash(match):
        formulas.append(match.group())
        return f'AILABMATHPLACEHOLDER{len(formulas)-1}END'
    text = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)|(?<!\\)\$\$.*?(?<!\\)\$\$|(?<![\\\w])\$[^\n$]+?\$', stash, text, flags=re.S)
    output = markdown.markdown(text, extensions=['fenced_code', 'tables', 'toc', 'codehilite', 'footnotes'],
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
                                     else '](' + CONFIG['site_url'] + 'catalogo.html)'), cell.source)


def notebook_content(nb, entry, outdir):
    parts = []
    notes = dict(re.findall(r'^\[\^([^\]]+)\]: (.*)$', '\n'.join(cell.source for cell in nb.cells if cell.cell_type == 'markdown'), re.M))
    used_notes = set()
    for number, cell in enumerate(nb.cells):
        if cell.get('id') in {'ai-lab-local-guide', 'ai-lab-local-setup'}:
            continue
        if cell.cell_type == 'markdown':
            source = re.sub(r'^\[\^[^\]]+\]: .*$', '', cell.source, flags=re.M)
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


def derived_pages(entries, output):
    pages = {}
    intro = nbformat.read(LAB/'notebooks/00-python-essenziale.ipynb', as_version=4)
    translate_notebook(intro)
    intro_url = launch_url(CONFIG, '00-python-essenziale.ipynb')
    intro_html = f'<div class="actions"><a class="button" href="{intro_url}">Apri in Colab</a><a class="button secondary" download href="notebooks/00-python-essenziale.ipynb">Scarica notebook</a></div>'
    intro_html += notebook_content(intro, {'track': 'python', 'stem': 'intro'}, output)
    pages['python.html'] = ('Python per il corso', intro_html, 'school')
    for cell in intro.cells:
        if cell.cell_type == 'markdown':
            cell.source = re.sub(r'\]\(([^)]+\.html)\)',
                                 lambda match: '](' + CONFIG['site_url'] + match[1] + ')',
                                 cell.source)
    nbformat.write(intro, output/'notebooks/00-python-essenziale.ipynb')
    catalog = '# Il corso completo\n\nSegui tutti i moduli di **Intro to Machine Learning** e **Intro to Deep Learning**, nello stesso ordine dei corsi Kaggle, con lezioni ed esercizi tradotti in italiano dai sorgenti disponibili.\n\nPrima di iniziare: [Python per il corso](python.html), un ripasso della sintassi e delle operazioni sui dati.\n\n[Inizia dalla prima lezione](corsi/machine_learning/tut1.html) · [Scarica tutti i notebook e i dataset](downloads/ai-lab-studenti.zip).\n\n'
    for track, setting in TRACKS.items():
        group = [entry for entry in entries if entry['track'] == track and is_core(entry)]
        if not group:
            continue
        catalog += f'## {setting["title"]}\n\n'
        if track == 'deep_learning':
            catalog += 'Archivio del precedente corso: API datate e video esterni non tradotti. È materiale aggiuntivo, distinto da Intro to Deep Learning.\n\n'
        catalog += '| Modulo | Lezione | Esercizio |\n| --- | --- | --- |\n'
        for index, (title, _) in enumerate(setting['topics']):
            subset = [entry for entry in group if entry['index'] == index]
            if not subset:
                continue
            links = {}
            for entry in subset:
                label = 'Leggi' if entry['kind'] == 'tutorial' else 'Esercizio'
                name = f'{entry["track"]}-{entry["stem"]}.ipynb'
                links[entry['kind']] = f'[{label}]({entry["page"]}) · [Colab]({launch_url(CONFIG, name)})'
            catalog += f'| {index+1:02d} · {title} | {links.get("tutorial", "Non presente nei sorgenti")} | {links.get("exercise", "Non presente nei sorgenti")} |\n'
        catalog += '\n'
    catalog += '## Altri materiali disponibili\n\nGli ulteriori notebook recuperati dalla fork, i materiali storici e le attività originali AI Lab sono conservati nella sezione [Materiali aggiuntivi](aggiuntivi.html).\n\n[Inventario con hash e metadati](inventory.json) · [Ambienti e dataset](esecuzione.html) · [Licenze](attribuzioni.html).\n'
    pages['catalogo.html'] = ('Il corso completo', render_markdown(catalog), 'school')
    exercises = '# Esercitazioni in Colab\n\nApri un esercizio, salva una copia nel tuo Drive ed esegui la cella **Preparazione in Colab** prima di iniziare. I dataset vengono caricati automaticamente.\n\n'
    for track in ('machine_learning', 'deep_learning_intro'):
        exercises += f'## {TRACKS[track]["title"]}\n\n'
        for entry in entries:
            if entry['track'] != track or entry['kind'] != 'exercise' or not is_core(entry):
                continue
            name = f'{entry["track"]}-{entry["stem"]}.ipynb'
            exercises += f'- **{entry["index"]+1}. {entry["title"]}** — [Apri in Colab]({launch_url(CONFIG, name)}) · [Lezione ed esercizio]({entry["page"]})\n'
        exercises += '\n'
    exercises += '[Istruzioni per Colab](esecuzione.html) · [Ripasso Python in Colab](' + intro_url + ').\n'
    pages['esercitazioni.html'] = ('Esercitazioni in Colab', render_markdown(exercises), 'school')
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
    lab_text = '# Notebook e laboratori\n\n## Percorso principale: esercizi Kaggle e dataset originali\n\nScarica il [pacchetto studenti completo](downloads/ai-lab-studenti.zip), estrailo e segui la [preparazione dei dataset](dataset.html). Include notebook tradotti, codice learntools originale e strumenti per scaricare o importare gli archivi. Non è necessario sostituire i dati con simulazioni.\n\nLe pagine del [corso completo](catalogo.html) propongono anche download individuali. Il bootstrap locale mantiene i percorsi originali e disattiva il solo invio di eventi all’iframe Kaggle, senza modificare i sorgenti. La compatibilità dei controlli Keras va verificata con le versioni indicate.\n\n## Laboratori aggiuntivi AI Lab\n\nI notebook seguenti sono materiale originale aggiuntivo; non sostituiscono i contenuti Kaggle. Contengono esempi inizialmente completi e attività da svolgere modificando il codice.\n\n'
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
    lab_text += '\nIl notebook 08 usa il file JSON creato dal notebook 07 nella stessa cartella. I laboratori 01–03 ricostruiscono alberi ed ensemble con Python standard per essere eseguibili senza scikit-learn; non riproducono tutte le funzionalità della libreria. La rete del laboratorio 04 è realmente addestrata con NumPy; non è un’esecuzione TensorFlow.\n\n## Notebook dei corsi Kaggle\n\nOgni pagina del [corso completo](catalogo.html) include il download del notebook tradotto. Sono mantenuti codice originale e controlli, con una nota sui dati richiesti. Le versioni Colab preparano i dati e adattano i metadati Keras usati dai controlli. La sessione remota resta da verificare con un account Google. Le soluzioni sono pubbliche.\n\n[Guida a Jupyter e ambienti remoti](esecuzione.html) · [Dettagli delle verifiche](verifiche.html).'
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
    checks += '\n## Limiti e controlli da completare\n\nGli originali Kaggle non sono stati eseguiti con i dataset remoti. I notebook Colab sono predisposti con caricamento dei dati e adattatore Keras; download, cache e integrità dei file sono controllati localmente. La sessione autenticata Colab non è stata eseguita qui. Invii a competizioni, servizi AutoML e TPU non sono verificati. Le immagini esterne possono non caricarsi senza rete. Formule, font, CSS, ricerca e interfaccia sono risorse locali del sito. La verifica visiva desktop/mobile non è stata completata: il server locale e Chromium sono impediti dai permessi di questo ambiente.\n\nLe esecuzioni con TensorFlow e scikit-learn restano da svolgere in un ambiente compatibile. Il workflow Pages compila e controlla i link prima di rendere disponibile un artefatto. La pubblicazione manuale richiede autorizzazione ed è documentata nel README.\n'
    pages['verifiche.html'] = ('Stato delle verifiche',render_markdown(checks),'school')
    return pages


def build(output):
    global CONFIG
    CONFIG = json.loads((LAB/'config.json').read_text())
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
    (output/'assets/syntax.css').write_text(HtmlFormatter(style='friendly').get_style_defs('.highlight'))
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
                    cell.source = translations[f"{entry['stem']}:{i}"]
            nb, _ = ItalianPreprocessor().preprocess(nb, make_resources(entry, entries))
            nb.nbformat_minor = 5
            nb.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                           'language_info': {'name': 'python'},
                           'ai_lab': {'source': str(entry['source'].relative_to(ROOT)),
                                      'source_sha256': hashlib.sha256(entry['source'].read_bytes()).hexdigest(),
                                      'execution_status': 'not_verified', 'license': 'Apache-2.0', 'language': 'it'}}
            intro = f"# {entry['title']}\n\n"
            if not is_core(entry):
                intro += status_text(entry) + '\n\n'
            nb.cells.insert(0, nbformat.v4.new_markdown_cell(intro, id='ai-lab-context'))
            if not entry['historical'] and not entry['special']:
                nb.cells.insert(1, nbformat.v4.new_markdown_cell('## Preparazione\n\nEsegui questa cella prima della lezione. Mantieni il notebook nella cartella del pacchetto studenti.', id='ai-lab-local-guide'))
                nb.cells.insert(2, nbformat.v4.new_code_cell(LOCAL_SETUP,id='ai-lab-local-setup'))
            translate_notebook(nb)
            label = ('Esercizio: ' if entry['kind']=='exercise' else '')+entry['title']
            name = entry['track']+'-'+entry['stem']+'.ipynb'
            colab_button = f'<a class="button" href="{launch_url(CONFIG, name)}">Apri in Colab</a>' if is_core(entry) else ''
            content = f'<div class="actions">{colab_button}<a class="button secondary" download href="../../notebooks/{name}">Scarica notebook</a><a class="button secondary" href="../../esecuzione.html">Come eseguirlo</a></div>'
            content += notebook_content(nb, entry, output)
            # Retain every source media URL and reference, including ones condensed in translation.
            source_text = '\n'.join(c.source for c in nbformat.read(entry['source'], as_version=4).cells if c.cell_type=='markdown')
            urls = sorted(set(re.findall(r'https?://[^\s<>"\)]+', source_text)))
            content += '<details><summary>Provenienza e riferimenti del sorgente</summary>'
            source_relative = str(entry['source'].relative_to(ROOT))
            commit = json.loads((LAB/'reports/inventory.json').read_text())['upstream_commit']
            content += f'<p>Fonte: <a href="{CONFIG["repository"]}/blob/{commit}/{source_relative}">{source_relative}</a>, Kaggle Learn, Apache-2.0. Traduzione italiana AI Lab.</p><ul>'
            content += ''.join(f'<li><a href="{html.escape(url,quote=True)}">{html.escape(url)}</a></li>' for url in urls)+'</ul></details>'
            normalize_notebook_links(nb, entry, entries)
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    cell.outputs=[]
                    cell.execution_count=None
            nbformat.validate(nb)
            nbformat.write(nb, output/'notebooks'/name)
            pages[entry['page']] = (label, content, entry['track'])
            coverage.append({'source': source_relative, 'page': entry['page'], 'notebook':name,
                             'markdown_cells': len([k for k in translations if k.startswith(entry['stem']+':')]),
                             'status':'translated_adaptation', 'execution':'not_verified'})
    for source in (LAB/'content/school').glob('*.md'):
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
        dest.write_text(shell(page, title, body, section, entries))
    index = [{'title':title, 'url':page, 'text':re.sub('<[^>]+>', ' ', body)} for page,(title,body,_) in pages.items()]
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
        for path in sorted((LAB/'requirements').glob('*.txt')):
            if path.name != 'kaggle-local.txt':
                bundle.write(path,'ai-lab-studenti/'+str(path.relative_to(ROOT)))
        bundle.write(LAB/'content/school/dataset.md','ai-lab-studenti/LEGGIMI-DATI.md')
        for path, relative in packaged_data:
            bundle.write(path,'ai-lab-studenti/'+relative)
    (output/'.nojekyll').touch()
    (LAB/'reports/coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(pages)} pages and {len(list((output/"notebooks").glob("*.ipynb")))} notebooks in {output}')


def shell(page, title, body, section, entries):
    rel = lambda target: relative_link(page, target)
    body = re.sub(r'(<a\b[^>]*\bhref="https://colab\.research\.google\.com/[^"]*")',
                  r'\1 target="_blank" rel="noopener noreferrer"', body)
    nav = ''
    for key,label in [('index.html','Panoramica'),('python.html','Python per il corso'),('catalogo.html','Programma completo'),('esercitazioni.html','Esercitazioni in Colab'),('dataset.html','Dataset originali'),('esecuzione.html','Come eseguire Python'),('aggiuntivi.html','Materiali aggiuntivi'),('attribuzioni.html','Fonti e licenze')]:
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
<link rel="stylesheet" href="{rel('assets/style.css')}"><link rel="stylesheet" href="{rel('assets/syntax.css')}">
<link rel="stylesheet" href="{rel('assets/vendor/katex/katex.min.css')}">
<script defer src="{rel('assets/vendor/katex/katex.min.js')}"></script>
<script defer src="{rel('assets/vendor/katex/auto-render.min.js')}"></script>
<script defer src="{rel('assets/app.js')}"></script></head>
<body data-root="{rel('index.html').removesuffix('index.html') or './'}"><a class="skip" href="#contenuto">Vai al contenuto</a>
<header><a class="brand" href="{rel('index.html')}"><span>{html.escape(CONFIG['title'])}</span></a>
<div class="header-actions"><button id="menu" aria-expanded="false" aria-controls="sidebar">Indice</button><button id="theme" aria-label="Cambia tema" aria-pressed="false">Tema scuro</button></div></header>
<aside id="sidebar"><label for="search">Cerca nel corso</label><input id="search" type="search" placeholder="Cerca…" autocomplete="off"><div id="search-status" role="status"></div><div id="results"></div><nav aria-label="Navigazione del corso">{nav}</nav><p class="teacher">{html.escape(CONFIG['teacher'])}</p></aside>
<main id="contenuto">{'<div class="breadcrumb">'+crumb+'</div>' if crumb else ''}<article>{body}</article><nav class="pager" aria-label="Lezione precedente e successiva">{pager}</nav>
<footer><a href="{rel('attribuzioni.html')}">Fonti e licenze</a> · <a href="{rel('verifiche.html')}">Verifiche tecniche</a></footer></main></body></html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=LAB/'build')
    args = parser.parse_args()
    destination = args.output.resolve()
    if destination in (ROOT, LAB) or ROOT.is_relative_to(destination):
        parser.error('Output must be a dedicated build directory')
    build(destination)
