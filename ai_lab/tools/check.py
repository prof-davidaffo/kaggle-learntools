"""Validate generated pages, links, notebooks, source hashes and student bundle."""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import zipfile

import nbformat
from build import LAB, get_entries, check_source_lock


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self.ids=set()
        self.language=None
        self.titles=0
    def handle_starttag(self, tag, attrs):
        attributes=dict(attrs)
        if tag=='html': self.language=attributes.get('lang')
        if tag=='title': self.titles+=1
        if attributes.get('id'): self.ids.add(attributes['id'])
        for key in ('href','src'):
            if key in attributes: self.links.append(attributes[key])


def check(directory):
    pages={}
    errors=[]
    config = json.loads((LAB/'config.json').read_text())
    if not (directory/'index.html').is_file(): errors.append('Missing Pages entry point index.html')
    if not (directory/'.nojekyll').is_file(): errors.append('Missing .nojekyll marker')
    for asset in directory.rglob('*'):
        if asset.is_symlink(): errors.append(f'Pages artifact must not contain symbolic links: {asset}')
    for path in directory.rglob('*.html'):
        parser=Document()
        text=path.read_text()
        parser.feed(text)
        pages[path.resolve()]=parser
        if parser.language!='it': errors.append(f'{path}: missing Italian lang')
        if parser.titles!=1: errors.append(f'{path}: invalid title count')
        canonical = config['site_url'] + path.relative_to(directory).as_posix()
        if f'<link rel="canonical" href="{canonical}">' not in text:
            errors.append(f'{path}: incorrect Pages canonical URL')
        if re.search(r'#\$[^$]+\$|#%%|#_COMMENT_IF',text): errors.append(f'{path}: unexpanded macro')
    for path,document in pages.items():
        for link in document.links:
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc or link.startswith('//'):
                continue
            if parsed.path.startswith('/'):
                errors.append(f'{path}: root-relative link breaks project Pages: {link}')
                continue
            destination=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
            if destination.is_dir(): destination=destination/'index.html'
            if not destination.is_relative_to(directory.resolve()):
                errors.append(f'{path}: link escapes build directory: {link}')
            elif not destination.exists():
                errors.append(f'{path}: missing target {link}')
            elif parsed.fragment and destination in pages and unquote(parsed.fragment) not in pages[destination].ids:
                errors.append(f'{path}: missing fragment {link}')
    expected={entry['page'] for entry in get_entries()}
    for page in expected:
        if not (directory/page).is_file(): errors.append('Missing course page: '+page)
    for number in range(1,9):
        if not (directory/f'incontro-{number}.html').is_file(): errors.append(f'Missing meeting {number}')
    notebooks=list((directory/'notebooks').glob('*.ipynb'))
    for path in notebooks:
        try: nbformat.validate(nbformat.read(path,as_version=4))
        except Exception as error: errors.append(f'{path}: {error}')
    index=json.loads((directory/'search.json').read_text())
    for entry in index:
        if not (directory/entry['url']).is_file(): errors.append('Invalid search target: '+entry['url'])
    check_source_lock(get_entries())
    bundle_path=directory/'downloads/ai-lab-studenti.zip'
    with zipfile.ZipFile(bundle_path) as bundle:
        if bundle.testzip(): errors.append('Student bundle integrity failed')
        names=bundle.namelist()
        if len([n for n in names if n.endswith('.ipynb')])!=len(notebooks):
            errors.append('Student bundle notebook count mismatch')
        required=['learntools/core/__init__.py','ai_lab/tools/datasets.py','ai_lab/datasets.json','LICENSE']
        for item in required:
            if 'ai-lab-studenti/'+item not in names: errors.append('Bundle missing '+item)
        dataset_manifest = json.loads((LAB/'datasets.json').read_text())
        data_files_checked = 0
        for key in ('melbourne','iowa','deep-learning'):
            item = dataset_manifest[key]
            for filename in item['files']:
                relative = f'{item["directory"]}/{filename}'
                source = LAB/'input'/relative
                published = directory/'datasets'/relative
                bundled = 'ai-lab-studenti/ai_lab/input/'+relative
                if not source.is_file() or not published.is_file() or bundled not in names:
                    errors.append('Missing original dataset in repository, site or student bundle: '+relative)
                    continue
                expected_digest = hashlib.sha256(source.read_bytes()).hexdigest()
                if hashlib.sha256(published.read_bytes()).hexdigest() != expected_digest:
                    errors.append('Site dataset differs from imported CSV: '+relative)
                if hashlib.sha256(bundle.read(bundled)).hexdigest() != expected_digest:
                    errors.append('Bundled dataset differs from imported CSV: '+relative)
                data_files_checked += 1
        for name in dataset_manifest['iowa']['aliases']:
            if 'ai-lab-studenti/ai_lab/input/'+name not in names:
                errors.append('Student bundle missing original Iowa path alias: '+name)
    report={'pages':len(pages),'course_pages':len(expected),'notebooks':len(notebooks),
            'local_links_checked':sum(len(document.links) for document in pages.values()),
            'search_entries':len(index),'original_csv_files_checked':data_files_checked,
            'student_bundle':'passed' if not errors else 'see errors',
            'errors':errors}
    (LAB/'reports/build-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if errors: raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--directory',type=Path,default=LAB/'build')
    args=parser.parse_args()
    check(args.directory)
