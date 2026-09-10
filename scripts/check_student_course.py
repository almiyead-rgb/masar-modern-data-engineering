"""Validate the learner path without interpreting reference outputs as native evidence."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys
import nbformat
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from masar.sources import verify_manifest

LAB_DAYS = {1: 1, 2: 1, 3: 2, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5}


def inspect(root=ROOT):
    errors, links, tables = [], 0, 0
    verify_manifest(root / 'data/masar-small-v1')
    for day in range(1, 6):
        for filename in ('README.md', 'CONCEPTS.md', 'GLOSSARY.md', 'PRACTICE.md', 'COMPLETION.md', 'SOURCES.md', 'STUDENT.ipynb'):
            if not (root / f'day{day:02}' / filename).is_file():
                errors.append(f'Missing Day {day} resource: {filename}')
    for lab, day in LAB_DAYS.items():
        for name in ('README.md', 'WALKTHROUGH.md'):
            if not (root / f'day{day:02}/labs/lab{lab:02}' / name).is_file():
                errors.append(f'Missing Lab {lab} resource: {name}')
    for path in sorted(root.rglob('*')):
        if not path.is_file() or any(p in path.parts for p in ('.git', 'outputs', 'evidence', '.venv', '__pycache__')):
            continue
        if path.suffix not in ('.md', '.ipynb'):
            continue
        if path.suffix == '.ipynb':
            nb = nbformat.read(path, as_version=4)
            nbformat.validate(nb)
            texts = [c.source for c in nb.cells if c.cell_type == 'markdown']
            for c in nb.cells:
                if c.cell_type == 'code':
                    try:
                        compile(c.source, str(path), 'exec')
                    except SyntaxError as exc:
                        errors.append(f'{path.relative_to(root)}: invalid code: {exc}')
        else:
            texts = [path.read_text(encoding='utf-8')]
        for text in texts:
            for target in re.findall(r'href=["\']([^"\']+)["\']', text) + re.findall(r'\]\(([^)]+)\)', text):
                url = urlsplit(target)
                if url.scheme or not url.path:
                    continue
                links += 1
                resolved = (path.parent / unquote(url.path)).resolve()
                if not resolved.is_relative_to(root) or not resolved.exists():
                    errors.append(f'{path.relative_to(root)}: missing link {target}')
            soup = BeautifulSoup(text, 'html.parser')
            for table in soup.find_all('table'):
                cells = table.find_all('td')
                if len(cells) == 2 and all(c.get('lang') for c in cells):
                    tables += 1
                    if [c.get('lang') for c in cells] != ['en', 'ar'] or [c.get('dir') for c in cells] != ['ltr', 'rtl']:
                        errors.append(f'{path.relative_to(root)}: reversed language columns')
            if path.parts[-2].startswith('day') or 'labs' in path.parts:
                words = soup.get_text(' ', strip=True)
                if re.search(r'ENGINE_NOT_EXECUTED|\bPARTIAL\b|authoring session|current authored build|لم يُنشأ مستودع', words):
                    errors.append(f'{path.relative_to(root)}: obsolete authoring commentary')
    return {'scope': 'FIVE_DAY_LEARNER_LAYOUT', 'days': 5, 'labs': 8,
            'internal_links': links, 'bilingual_tables': tables, 'errors': errors,
            'status': 'PASSED' if not errors else 'FAILED', 'engine_execution_claim': False}


if __name__ == '__main__':
    result = inspect()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['status'] == 'PASSED' else 1)
