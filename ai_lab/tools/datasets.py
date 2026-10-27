"""Fetch original Kaggle data or import user-downloaded archives safely."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import zipfile

LAB = Path(__file__).resolve().parents[1]


def manifest():
    return json.loads((LAB/'datasets.json').read_text())


def install_archive(archive, key, destination, required_files=None):
    specification = manifest()[key]
    target = destination/specification['directory']
    with tempfile.TemporaryDirectory(prefix='ai-lab-data-') as temporary:
        staging = Path(temporary)
        with zipfile.ZipFile(archive) as bundle:
            total = sum(item.file_size for item in bundle.infolist())
            if total > 3_000_000_000:
                raise ValueError('Archive exceeds the 3 GB safety limit')
            for item in bundle.infolist():
                path = (staging/item.filename).resolve()
                if not path.is_relative_to(staging.resolve()) or stat.S_ISLNK(item.external_attr >> 16):
                    raise ValueError(f'Unsafe archive member: {item.filename}')
            required = specification['files'] if required_files is None else required_files
            supporting = {'data_description.txt', 'sample_submission.csv'}
            members = [item for item in bundle.infolist()
                       if item.filename in required or item.filename in supporting
                       or any(word in Path(item.filename).name.lower()
                              for word in ('license', 'licence', 'readme', 'citation', 'metadata'))]
            bundle.extractall(staging, members=members)
        required = specification['files'] if required_files is None else required_files
        missing = [name for name in required if not (staging/name).is_file()]
        if missing:
            raise ValueError('Expected original files missing at archive root: '+', '.join(missing))
        for name, expected_columns in specification.get('columns', {}).items():
            source = staging/name
            if source.is_file():
                with source.open(encoding='utf-8-sig',newline='') as stream:
                    columns = next(csv.reader(stream),[])
                absent = set(expected_columns)-set(columns)
                if absent:
                    raise ValueError(f'{key}/{name}: missing expected CSV columns: '+', '.join(sorted(absent)))
        # Compare every existing destination before any write; user data is never overwritten.
        files = [path for path in staging.rglob('*') if path.is_file()]
        for source in files:
            dest = target/source.relative_to(staging)
            if dest.exists() and source.read_bytes() != dest.read_bytes():
                raise FileExistsError(f'Existing file differs; choose a new data directory: {dest}')
        aliases = [name for name in specification.get('aliases', []) if (staging/name).is_file()]
        for name in aliases:
            alias = destination/name
            if alias.exists() and alias.read_bytes() != (staging/name).read_bytes():
                raise FileExistsError(f'Existing alias differs: {alias}')
        for source in files:
            dest = target/source.relative_to(staging)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                shutil.copy2(source, dest)
        for name in aliases:
            alias = destination/name
            if not alias.exists():
                shutil.copy2(target/name, alias)
    print(f'Installed original data: {key} -> {target}')


def install_files(paths, key, destination):
    specification = manifest()[key]
    names = [path.name for path in paths]
    if len(names) != len(set(names)):
        raise ValueError('Duplicate CSV filenames in the import')
    unexpected = set(names)-set(specification['files'])
    if unexpected:
        raise ValueError('Unexpected CSV filenames for '+key+': '+', '.join(sorted(unexpected)))
    if any(not path.is_file() for path in paths):
        raise FileNotFoundError('Every input must be an existing CSV file')
    with tempfile.TemporaryDirectory(prefix='ai-lab-csv-import-') as temporary:
        archive = Path(temporary)/'import.zip'
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as bundle:
            for path in paths:
                bundle.write(path,path.name)
        install_archive(archive,key,destination,required_files=names)


def inspect(destination):
    result = {}
    for key, item in manifest().items():
        missing = [name for name in item['files'] if not (destination/item['directory']/name).is_file()]
        missing_aliases = [name for name in item.get('aliases', []) if not (destination/name).is_file()]
        result[key] = {'status':'missing' if missing or missing_aliases else 'present',
                       'missing':missing,'missing_aliases':missing_aliases}
        print(key+':', 'missing '+', '.join(missing) if missing else 'present')
        if missing_aliases:
            print('  Missing legacy aliases:', ', '.join(missing_aliases))
    return result


def download(key, destination):
    item = manifest()[key]
    if all((destination/item['directory']/name).is_file() for name in item['files']):
        for name in item.get('aliases', []):
            alias = destination/name
            source = destination/item['directory']/name
            if not alias.exists():
                shutil.copy2(source,alias)
            elif alias.read_bytes() != source.read_bytes():
                raise FileExistsError(f'Existing alias differs: {alias}')
        print(key+': original files already present; no download')
        return
    executable = shutil.which('kaggle')
    if not executable:
        raise RuntimeError('Install the official Kaggle CLI or use --import-zip with a manually downloaded archive')
    with tempfile.TemporaryDirectory(prefix='ai-lab-download-') as temporary:
        command = [executable, 'datasets' if item['kind']=='dataset' else 'competitions', 'download',
                   '-d' if item['kind']=='dataset' else '-c', item['slug'], '-p', temporary]
        subprocess.run(command, check=True)
        archives = list(Path(temporary).glob('*.zip'))
        if len(archives) != 1:
            raise RuntimeError('Expected one Kaggle ZIP archive')
        install_archive(archives[0], key, destination)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('keys', nargs='*', choices=list(manifest()))
    parser.add_argument('--destination', type=Path, default=LAB/'input')
    imports = parser.add_mutually_exclusive_group()
    imports.add_argument('--import-zip', type=Path)
    imports.add_argument('--import-files', type=Path, nargs='+')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        inspect(args.destination)
    elif args.import_files:
        if len(args.keys) != 1:
            parser.error('--import-files requires exactly one dataset key')
        install_files(args.import_files,args.keys[0],args.destination)
    elif args.import_zip:
        if len(args.keys) != 1:
            parser.error('--import-zip requires exactly one dataset key')
        install_archive(args.import_zip, args.keys[0], args.destination)
    elif args.keys:
        for key in args.keys:
            download(key, args.destination)
    else:
        for key,item in manifest().items():
            print(key, item['use'], item['url'])
