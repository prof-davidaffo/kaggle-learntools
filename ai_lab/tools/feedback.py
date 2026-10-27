"""Localize educational feedback without changing Kaggle checkers or their logic."""
from __future__ import annotations

import ast
from functools import lru_cache
import json
from pathlib import Path
import re

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parent


def normalize(text):
    return ' '.join(text.split())


@lru_cache(maxsize=1)
def translations():
    requested = json.loads((LAB/'localization/it.json').read_text())
    resolved = {}
    found = set()
    for track in ('machine_learning','deep_learning_intro'):
        for path in sorted((ROOT/'learntools'/track).glob('ex[0-9].py')):
            tree = ast.parse(path.read_text())
            for definition in tree.body:
                if not isinstance(definition, ast.ClassDef):
                    continue
                for statement in definition.body:
                    if not isinstance(statement, ast.Assign) or not isinstance(statement.targets[0],ast.Name):
                        continue
                    key = f'{track}/{path.stem}.{definition.name}.{statement.targets[0].id}'
                    if key not in requested:
                        continue
                    try:
                        source = ast.literal_eval(statement.value)
                    except (ValueError,TypeError):
                        continue
                    if isinstance(source,str):
                        resolved[normalize(source)] = requested[key]
                        found.add(key)
    if found != set(requested):
        raise ValueError('Feedback sources changed: '+', '.join(sorted(set(requested)-found)))
    return resolved


def translate(text):
    exact = translations().get(normalize(text))
    if exact is not None:
        return exact
    # Preserve Python snippets, including their English comments and docstrings.
    pieces = re.split(r'(```.*?```)', text, flags=re.S)
    replacements = {
        'Your answer should look something like:':'La struttura della risposta è:',
        'Your model should look something like:':'La struttura del modello è:',
        'Your code should look something like:':'La struttura del codice è:',
        'Your solution should look something like:':'La struttura della soluzione è:',
        'Sorry, no hints available for this question.':'Per questa domanda non ci sono suggerimenti.',
        'Sorry, no auto-checking available for this question.':'Questa domanda richiede una valutazione ragionata: non ha un controllo automatico.',
        "When you've updated the starter code, `check()` will tell you whether your code is correct.":'Dopo aver completato il codice iniziale, `check()` ti indicherà l’esito del controllo.',
    }
    for index in range(0,len(pieces),2):
        for source,target in replacements.items():
            pieces[index] = pieces[index].replace(source,target)
        pieces[index] = re.sub(r'\(For another hint, call `\.hint\((\d+)\)`\)',r'(Per un altro suggerimento, chiama `.hint(\1)`)',pieces[index])
    return ''.join(pieces)


def install():
    from IPython.display import display, Markdown
    from learntools.core import problem_view, richtext
    if getattr(problem_view,'_ai_lab_italian_feedback',False):
        return

    def italian_display(value):
        if not isinstance(value,richtext.RichText):
            return display(value)
        text = translate(value.txt)
        label = ''
        if isinstance(value,richtext.PrefixedRichText):
            if isinstance(value,richtext.Hint):
                label = 'Suggerimento'+(f' {value.n}' if value.is_multi else '')
            elif isinstance(value,richtext.Correct):
                label = 'Corretto'
            elif isinstance(value,richtext.Solution):
                label = 'Soluzione'
            elif isinstance(value,richtext.TestFailure):
                label = 'Da rivedere'
            else:
                label = 'Controllo'
        display(Markdown((f'**{label}**\n\n' if label else '')+text))

    problem_view.display = italian_display
    problem_view._ai_lab_italian_feedback = True
