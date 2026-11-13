"""Structural safeguards for complete translations, not semantic certification.

Compare each Markdown cell with the locked Kaggle source. Word counts flag
major shortening only; fidelity still requires reading both texts.
"""
from collections import Counter
import io
import re
import tokenize


def code_tokens(source):
    ignored = {tokenize.COMMENT, tokenize.ENCODING, tokenize.NL,
               tokenize.NEWLINE, tokenize.ENDMARKER}
    return [(token.type, token.string) for token in
            tokenize.generate_tokens(io.StringIO(source).readline)
            if token.type not in ignored]


def prose_words(source):
    source = re.sub(r'```[^\n]*\n.*?```', '', source, flags=re.S)
    source = re.sub(r'<[^>]*>', ' ', source)
    source = re.sub(r'https?://[^\s<>"\)]+', '', source)
    return len(source.split())


def audit_cell(source, translation):
    errors = []
    # Preserve repetitions as well as unique links: the same image can be used
    # at several points in an explanation.
    urls = lambda text: Counter(re.findall(r'https?://[^\s<>"\)]+', text))
    missing = urls(source) - urls(translation)
    if missing:
        errors.append('Missing source links/media: ' + ', '.join(sorted(missing)))
    def images(text):
        markdown_images = re.findall(r'!\[[^\]]*\]\(([^\s)]+)', text)
        html_images = re.findall(r'<img\b[^>]*\bsrc=["\']([^"\']+)', text, re.I)
        return Counter(markdown_images + html_images)
    if images(source) != images(translation):
        errors.append('Changed inline images (a reference link is not a replacement)')
    macros = lambda text: Counter(re.findall(r'#\$[^$]+\$', text))
    if macros(source) != macros(translation):
        errors.append('Changed source navigation macros')
    headings = lambda text: re.findall(r'^(#{1,6})\s+', text, re.M)
    if headings(source) != headings(translation):
        errors.append('Changed heading hierarchy')
    fences = lambda text: re.findall(r'^```[^\n]*\n(.*?)^```', text, re.M | re.S)
    original_blocks, translated_blocks = fences(source), fences(translation)
    if len(original_blocks) != len(translated_blocks):
        errors.append('Missing or added fenced code blocks')
    else:
        for index, (original, translated) in enumerate(zip(original_blocks, translated_blocks)):
            if code_tokens(original) != code_tokens(translated):
                errors.append(f'Changed example code in block {index + 1}')
    source_words, translated_words = prose_words(source), prose_words(translation)
    ratio = translated_words / source_words if source_words else None
    if source_words >= 100 and ratio < 0.70:
        errors.append('Substantial shortening: review against the full source')
    return {'source_words': source_words, 'translation_words': translated_words,
            'word_ratio': round(ratio, 3) if ratio is not None else None,
            'errors': errors}
