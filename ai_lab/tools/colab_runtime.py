"""Download and initialize the course runtime inside a hosted notebook."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
from urllib.error import URLError
from urllib.request import urlopen


def _read_url(url):
    try:
        with urlopen(url, timeout=90) as response:
            return response.read()
    except (OSError, URLError) as error:
        raise RuntimeError('Unable to load course files. Check the connection and that '
                           'the latest course files have been pushed to GitHub: '+url) from error


def download_runtime(manifest_url, source_url, root):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(_read_url(manifest_url))
    if manifest.get('schema') != 1:
        raise ValueError('Unsupported course runtime manifest')

    def fetch(item):
        relative = PurePosixPath(item['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Invalid runtime path')
        target = root.joinpath(*relative.parts)
        if not target.resolve().is_relative_to(root):
            raise ValueError('Runtime path escapes the course directory')
        if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256']:
            return
        data = _read_url(source_url.rstrip('/')+'/'+str(relative))
        if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('Course file changed or download is incomplete: '+str(relative)+
                             '. Reopen the latest notebook and run preparation again.')
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name+'.part')
        temporary.write_bytes(data)
        temporary.replace(target)

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(fetch, manifest['files']))
    for alias in ('train.csv', 'test.csv'):
        destination = root/'ai_lab/input'/alias
        shutil.copy2(root/'ai_lab/input/home-data-for-ml-course'/alias, destination)
    return root


def setup(root, namespace, deep_learning=False):
    root = Path(root).resolve()
    required = {'numpy': 'numpy', 'pandas': 'pandas', 'matplotlib': 'matplotlib',
                'sklearn': 'scikit-learn', 'IPython': 'ipython'}
    if deep_learning:
        required['tensorflow'] = 'tensorflow'
    missing = [package for module, package in required.items()
               if importlib.util.find_spec(module) is None]
    if missing:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', *missing])
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    os.environ['LEARN_USE_KAGGLE_SDK'] = 'False'
    runtime = root/'ai_lab/runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    os.chdir(runtime)
    from learntools.core import binder, tracking
    tracking.track = lambda event: None
    if not binder.bound:
        binder.bind(namespace)
    from ai_lab.tools.feedback import install
    install()
    if deep_learning:
        from ai_lab.tools.keras_compat import install as install_keras_compat
        install_keras_compat()
