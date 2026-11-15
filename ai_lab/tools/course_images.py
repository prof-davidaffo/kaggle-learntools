"""Preserve the Kaggle lesson images locally without modifying their sources."""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
import re

LAB = Path(__file__).resolve().parents[1]
DIRECTORY = LAB / 'assets/kaggle-images'
URL_PATTERN = re.compile(r'https://storage\.googleapis\.com/kaggle-media/learn/images/[A-Za-z0-9_.-]+\.(?:png|gif|jpe?g|svg|webp)', re.I)
MIME_TYPES = {'.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg',
              '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.webp': 'image/webp'}


def load_images():
    manifest = json.loads((DIRECTORY / 'manifest.json').read_text())['images']
    result = {}
    for item in manifest:
        name, source = item['file'], item['source']
        if Path(name).name != name or not URL_PATTERN.fullmatch(source) or source.rsplit('/', 1)[-1] != name:
            raise ValueError(f'Invalid image manifest entry: {source}')
        if source in result:
            raise ValueError(f'Duplicate image manifest entry: {source}')
        content = (DIRECTORY / name).read_bytes()
        if len(content) != item['bytes'] or hashlib.sha256(content).hexdigest() != item['sha256']:
            raise ValueError(f'Image does not match manifest: {name}')
        mime = MIME_TYPES[Path(name).suffix.lower()]
        result[source] = {'file': name, 'data_uri': 'data:' + mime + ';base64,' + base64.b64encode(content).decode('ascii')}
    return result


def replace_images(source, images, *, notebook=False):
    def replace(match):
        url = match.group()
        if url not in images:
            raise ValueError(f'Image missing from local archive: {url}')
        return images[url]['data_uri'] if notebook else '../../assets/kaggle-images/' + images[url]['file']
    return URL_PATTERN.sub(replace, source)


def attach_images(cell, images):
    """Keep image data out of the editable Markdown while embedding it."""
    def replace(match):
        url = match.group()
        if url not in images:
            raise ValueError(f'Image missing from local archive: {url}')
        item = images[url]
        mime, data = item['data_uri'][5:].split(';base64,', 1)
        if 'attachments' not in cell:
            cell['attachments'] = {}
        cell['attachments'][item['file']] = {mime: data}
        return 'attachment:' + item['file']
    cell.source = URL_PATTERN.sub(replace, cell.source)
