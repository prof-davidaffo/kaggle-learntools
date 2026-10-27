"""Execute school notebooks in a kernel or as ordinary Python, and record evidence."""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import platform
import shutil
import tempfile
import time
import traceback

LAB = Path(__file__).resolve().parents[1]


def run(kernel=False, require_all=False, export_reference=False):
    records=[]
    with tempfile.TemporaryDirectory(prefix='ai-lab-execution-') as temporary:
        workspace=Path(temporary)
        previous=Path.cwd()
        try:
            os.chdir(workspace)
            for path in sorted((LAB/'notebooks').glob('*.ipynb')):
                notebook=json.loads(path.read_text())
                dependencies=notebook['metadata']['ai_lab']['dependencies']
                missing=[name for name in dependencies if importlib.util.find_spec(name) is None]
                record={'notebook':path.name, 'mode':'jupyter_kernel' if kernel else 'python_cells',
                        'dependencies':dependencies}
                if missing:
                    record.update(status='not_run',reason='Missing dependencies: '+', '.join(missing))
                    records.append(record)
                    print(path.name, 'NOT RUN:',record['reason'])
                    continue
                started=time.monotonic()
                stream=io.StringIO()
                try:
                    if kernel:
                        import nbformat
                        from nbclient import NotebookClient
                        nb=nbformat.read(path,as_version=4)
                        client=NotebookClient(nb,timeout=300,kernel_name='python3',resources={'metadata':{'path':str(workspace)}})
                        client.execute()
                        executed=LAB/'reports/executed'
                        executed.mkdir(exist_ok=True)
                        nbformat.write(nb,executed/path.name)
                        output='\n'.join(out.get('text','') for cell in nb.cells if cell.cell_type=='code'
                                         for out in cell.outputs if out.output_type=='stream')
                    else:
                        namespace={'__name__':'__main__'}
                        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                            for index,cell in enumerate(notebook['cells']):
                                if cell['cell_type']=='code':
                                    exec(compile(cell['source'],f'{path.name}:cell-{index}','exec'),namespace)
                        output=stream.getvalue()
                    record.update(status='passed',output=output.strip())
                except Exception:
                    record.update(status='failed',output=stream.getvalue(),error=traceback.format_exc())
                record['seconds']=round(time.monotonic()-started,3)
                records.append(record)
                print(path.name, record['status'].upper(), str(record['seconds'])+'s')
            reference=next((r for r in records if r['notebook']=='07-progetto-riferimento.ipynb'),None)
            if reference and reference['status']=='passed' and export_reference:
                artifact=workspace/'reference-model.json'
                shutil.copy2(artifact,LAB/'assets/reference-model.json')
        finally:
            os.chdir(previous)
    report={'python':platform.python_version(), 'mode':'jupyter_kernel' if kernel else 'python_cells',
            'note':'python_cells executes every code cell in order with a fresh namespace per notebook; it does not test Jupyter UI or kernel integration.' if not kernel else 'Executed with nbclient and an actual Jupyter kernel.',
            'results':records}
    (LAB/'reports/execution.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    failures=[r for r in records if r['status']=='failed' or require_all and r['status']!='passed']
    if failures:
        for item in failures:
            print(item.get('error',item.get('reason')))
        raise SystemExit(1)
    return records


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--kernel',action='store_true')
    parser.add_argument('--require-all',action='store_true')
    parser.add_argument('--export-reference',action='store_true')
    args=parser.parse_args()
    run(args.kernel,args.require_all,args.export_reference)
