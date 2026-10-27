"""Translate prose comments while preserving every executable Python token."""
from __future__ import annotations

import io
import json
from pathlib import Path
import re
import tokenize


COMMENT_TRANSLATIONS = json.loads(
    (Path(__file__).resolve().parents[1]/'localization/comments.it.json').read_text())


def translate_code(source, unknown=None):
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    lines = source.splitlines(keepends=True)
    for token in reversed(tokens):
        if token.type != tokenize.COMMENT:
            continue
        key = token.string.rstrip()
        replacement = COMMENT_TRANSLATIONS.get(key)
        if replacement is None and '#' in key[1:]:
            prefix, separator, tail = key.rpartition('#')
            translated_tail = COMMENT_TRANSLATIONS.get('# '+tail.strip())
            if translated_tail:
                replacement = prefix + translated_tail
        if replacement is not None:
            row = token.start[0]-1
            lines[row] = lines[row][:token.start[1]] + replacement + lines[row][token.end[1]:]
        elif unknown is not None:
            unknown.add(key)
    translated = ''.join(lines)
    translated_tokens = list(tokenize.generate_tokens(io.StringIO(translated).readline))
    original_code = [(t.type, t.string) for t in tokens if t.type != tokenize.COMMENT]
    translated_code = [(t.type, t.string) for t in translated_tokens if t.type != tokenize.COMMENT]
    if original_code != translated_code:
        raise ValueError('Comment localization changed executable Python tokens')
    return translated


def translate_notebook(notebook, unknown=None):
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            cell.source = translate_code(cell.source, unknown)
        elif cell.cell_type == 'markdown':
            cell.source = re.sub(
                r'(```(?:python|py)\s*\n)(.*?)(```)',
                lambda match: match[1] + translate_code(match[2], unknown) + match[3],
                cell.source, flags=re.S)
    return notebook
