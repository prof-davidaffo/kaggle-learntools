"""Inspect source coverage; update the translation lock only after human review."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import runpy
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT/'ai_lab'
TRACKS = ('machine_learning','deep_learning_intro','deep_learning')


def snapshot():
    tracks = {}
    support = {}
    for track in TRACKS:
        metadata_path = ROOT/'notebooks'/track/'track_meta.py'
        module = runpy.run_path(str(metadata_path))
        registered = {item['filename']:item for item in module['notebooks']}
        entries=[]
        for path in sorted((ROOT/'notebooks'/track/'raw').glob('*.ipynb')):
            notebook=json.loads(path.read_text())
            item=registered.get(path.name)
            entries.append({'source':str(path.relative_to(ROOT)),
                            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                            'registered':bool(item),
                            'topic':module['lessons'][item['lesson_idx']]['topic'] if item else 'Unregistered historical material',
                            'metadata':item,'cells':len(notebook['cells']),
                            'markdown_cells':sum(cell['cell_type']=='markdown' for cell in notebook['cells'])})
        tracks[track]=entries
        support[str(metadata_path.relative_to(ROOT))]=hashlib.sha256(metadata_path.read_bytes()).hexdigest()
    for path in sorted((ROOT/'notebooks/nb_utils').glob('*.py')):
        support[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    for package in ('core', *TRACKS):
        for path in sorted((ROOT/'learntools'/package).glob('*.py')):
            support[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    return {'upstream_commit':commit,'tracks':tracks,'support_hashes':support}


def differences(before,after):
    old={entry['source']:entry['sha256'] for group in before.get('tracks',{}).values() for entry in group}
    new={entry['source']:entry['sha256'] for group in after['tracks'].values() for entry in group}
    return {'added':sorted(new.keys()-old.keys()),'removed':sorted(old.keys()-new.keys()),
            'changed':sorted(path for path in old.keys() & new.keys() if old[path]!=new[path]),
            'support_changed':sorted(path for path,value in before.get('support_hashes',{}).items()
                                     if after['support_hashes'].get(path)!=value)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update',action='store_true',help='Write the source lock after reviewing corresponding translations')
    args=parser.parse_args()
    lock=LAB/'reports/inventory.json'
    before=json.loads(lock.read_text()) if lock.exists() else {}
    current=snapshot()
    print(json.dumps(differences(before,current),indent=2))
    for track,entries in current['tracks'].items():
        print(track, 'notebooks:',len(entries),'markdown cells:',sum(entry['markdown_cells'] for entry in entries))
    if args.update:
        lock.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
        print('Updated the reviewed source lock:',lock)
