"""Generate the versioned notebooks and manifest used by Colab launch URLs."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from urllib.parse import quote, urlparse

import nbformat

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parent


def launch_url(config, filename):
    repository = urlparse(config['repository']).path.strip('/').removesuffix('.git')
    ref = quote(config.get('colab_ref', 'master'), safe='')
    return f'https://colab.research.google.com/github/{repository}/blob/{ref}/ai_lab/colab/{quote(filename)}'


def runtime_manifest():
    files = {ROOT/'learntools/__init__.py'}
    for package in ('core', 'machine_learning', 'deep_learning_intro'):
        files.update((ROOT/'learntools'/package).rglob('*.py'))
    for relative in ['LICENSE', 'ai_lab/LICENSE', 'ai_lab/NOTICE', 'ai_lab/datasets.json',
                     'ai_lab/localization/it.json', 'ai_lab/tools/feedback.py',
                     'ai_lab/tools/keras_compat.py', 'ai_lab/tools/colab_runtime.py']:
        files.add(ROOT/relative)
    manifest = json.loads((LAB/'datasets.json').read_text())
    for key in ('melbourne', 'iowa', 'deep-learning'):
        dataset = manifest[key]
        for filename in [*dataset['files'], 'ATTRIBUTION.txt']:
            files.add(LAB/'input'/dataset['directory']/filename)
    result = []
    for path in sorted(files):
        content = path.read_bytes()
        result.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': len(content),
                       'sha256': hashlib.sha256(content).hexdigest()})
    return {'schema': 1, 'files': result}


def setup_cell(config, deep_learning):
    repository = urlparse(config['repository']).path.strip('/').removesuffix('.git')
    source = f'https://raw.githubusercontent.com/{repository}/{quote(config.get("colab_ref", "master"), safe="")}'
    digest = hashlib.sha256((LAB/'tools/colab_runtime.py').read_bytes()).hexdigest()
    return f'''from pathlib import Path
import hashlib
import importlib.util
from urllib.request import urlopen
from IPython.display import display, Markdown

course_source = {source!r}
course_root = (Path("/content") if Path("/content").is_dir() else Path.home()) / "ai-lab-colab"
course_root.mkdir(parents=True, exist_ok=True)
bootstrap_path = course_root / "_bootstrap.py"
bootstrap_hash = {digest!r}
if not bootstrap_path.is_file() or hashlib.sha256(bootstrap_path.read_bytes()).hexdigest() != bootstrap_hash:
    with urlopen(course_source + "/ai_lab/tools/colab_runtime.py", timeout=90) as response:
        bootstrap_data = response.read()
    if hashlib.sha256(bootstrap_data).hexdigest() != bootstrap_hash:
        raise RuntimeError("Course setup changed. Reopen the latest notebook from the course site.")
    bootstrap_path.write_bytes(bootstrap_data)
bootstrap_spec = importlib.util.spec_from_file_location("ai_lab_colab_bootstrap", bootstrap_path)
bootstrap = importlib.util.module_from_spec(bootstrap_spec)
bootstrap_spec.loader.exec_module(bootstrap)
bootstrap.download_runtime(course_source + "/ai_lab/colab/runtime.json", course_source, course_root)
bootstrap.setup(course_root, globals(), deep_learning={deep_learning!r})
display(Markdown("**Preparazione completata.** Puoi eseguire le celle della lezione."))
'''


def generate(output, entries, config):
    destination = LAB/'colab'
    destination.mkdir(exist_ok=True)
    manifest = runtime_manifest()
    (destination/'runtime.json').write_text(json.dumps(manifest, indent=2)+'\n')
    notebooks = [('00-python-essenziale.ipynb', False)]
    notebooks += [(f'{entry["track"]}-{entry["stem"]}.ipynb', entry['track'] == 'deep_learning_intro')
                  for entry in entries]
    names = set()
    for name, deep_learning in notebooks:
        nb = copy.deepcopy(nbformat.read(output/'notebooks'/name, as_version=4))
        cells = [cell for cell in nb.cells if cell.id not in {'ai-lab-local-guide', 'ai-lab-local-setup'}]
        guide = nbformat.v4.new_markdown_cell(
            '## Preparazione in Colab\n\n'
            '1. Salvare una copia del notebook nel proprio Drive.\n'
            '2. Eseguire la cella seguente e attendere «Preparazione completata».\n'
            '3. Eseguire le celle nell’ordine e svolgere gli esercizi.\n\n'
            'La cella di preparazione acquisisce i dataset e i controlli degli esercizi '
            'dal repository del corso e configura l’ambiente Python. '
            'Dopo il riavvio della sessione occorre eseguire nuovamente la preparazione.',
            id='ai-lab-colab-guide')
        setup = nbformat.v4.new_code_cell(setup_cell(config, deep_learning), id='ai-lab-colab-setup')
        nb.cells = [cells[0], guide, setup, *cells[1:]]
        nb.metadata['colab'] = {'name': name, 'provenance': []}
        nb.metadata['ai_lab']['environment'] = 'colab'
        nb.metadata['ai_lab']['execution_status'] = 'prepared_not_cloud_executed'
        for cell in nb.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        nbformat.validate(nb)
        nbformat.write(nb, destination/name)
        names.add(name)
    for stale in destination.glob('*.ipynb'):
        if stale.name not in names:
            stale.unlink()
    (destination/'README.md').write_text(
        '# Notebook per Google Colab\n\n'
        'File generati da `python ai_lab/tools/build.py`, da versionare insieme alle sorgenti. '
        'Non modificarli direttamente: modifica le traduzioni o il notebook Python sorgente e rigenera.\n\n'
        'I link Colab aprono questi file dal branch configurato in `ai_lab/config.json` (`colab_ref`). '
        'La prima cella carica solo i file elencati in `runtime.json`, ne controlla gli hash e configura '
        'dataset, learntools e adattatore Keras. Gli originali Kaggle restano invariati.\n\n'
        'I file devono essere inviati su GitHub prima che i link e il download automatico siano utilizzabili. '
        'La preparazione locale non equivale a una sessione Colab eseguita e verificata.\n')
    return {'notebooks': len(names), 'runtime_files': len(manifest['files']),
            'download_bytes': sum(item['bytes'] for item in manifest['files']),
            'cloud_execution': 'not_run'}
