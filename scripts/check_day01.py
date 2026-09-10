"""Validate only the published Day 1 learning path, including notebook links."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit
import nbformat

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar.sources import verify_manifest

verify_manifest(ROOT / "data/masar-small-v1")
required = ["day01/STUDENT.ipynb", "README.md", "course.json",
            "resources/Masar_Cost_Model.xlsx", "docs/START_HERE.md", "docs/SETUP.md",
            "docs/TROUBLESHOOTING.md", "docs/GIT_WORKFLOW.md",
            "project/README.md", "project/SUBMISSION.md"]
required += ["day01/" + name + ".md" for name in
             ["README", "CONCEPTS", "GLOSSARY", "SOURCES", "PRACTICE", "COMPLETION"]]
required += [f"labs/lab0{number}/{name}.md" for number in (1, 2)
             for name in ("README", "WALKTHROUGH")]
missing = [path for path in required if not (ROOT / path).is_file()]
if missing:
    raise AssertionError({"missing_day01_files": missing})
# Later-day drafts/tests are deliberately outside this publication's scope.
markdown = [ROOT / path for path in ["README.md", "STATUS.md", "TRAINING_CONTENT.md",
    "labs/README.md", "data/README.md", "data/DICTIONARY.md",
    "docs/START_HERE.md", "docs/SETUP.md", "docs/TROUBLESHOOTING.md",
    "docs/GIT_WORKFLOW.md", "project/README.md", "project/SUBMISSION.md",
    "templates/DECISIONS.md", "templates/LAB_NOTES.md", "templates/BENCHMARKS.md"]]
for folder in ["day01", "labs/lab01", "labs/lab02"]:
    markdown.extend((ROOT / folder).glob("*.md"))
errors, checked_links = [], 0

def check_links(path, text):
    global checked_links
    targets = re.findall(r'href=["\']([^"\']+)["\']', text)
    targets += re.findall(r'\]\(([^)]+)\)', text)
    for target in targets:
        url = urlsplit(target)
        if url.scheme or not url.path:
            continue
        checked_links += 1
        resolved = (path.parent / unquote(url.path)).resolve()
        if not resolved.is_relative_to(ROOT) or not resolved.exists():
            errors.append((str(path.relative_to(ROOT)), target))

for path in sorted(set(markdown)):
    check_links(path, path.read_text(encoding="utf-8"))
notebooks = [ROOT / "day01/STUDENT.ipynb", *sorted((ROOT / "notebooks/day01").glob("*.ipynb"))]
for path in notebooks:
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            check_links(path, cell.source)
if errors:
    raise AssertionError({"broken_day01_links": errors})
print(json.dumps({"scope": "DAY01_ONLY", "required_files": len(required),
    "markdown_pages": len(set(markdown)), "notebooks": len(notebooks),
    "internal_links": checked_links, "dataset": "unchanged", "status": "PASSED"}, indent=2))
