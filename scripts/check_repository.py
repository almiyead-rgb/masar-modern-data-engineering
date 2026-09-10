"""Offline authoring QA. --release is a teaching-readiness gate, NOT publishing.

Draft engine notebooks may be structurally valid but remain release blockers.
A helper run or a 'published' flag cannot supply engine execution evidence.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from masar.release_evidence import engine_evidence_issues, dbt_evidence_issues
SKIP = {".git", "outputs", "__pycache__", ".ipynb_checkpoints", ".venv", "workspaces"}
PINNED_MANIFEST = "20a7e45bed2980b9394c10e8532da3b9f40f614366bb2df26a88610253e768e3"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.cells, self.issues = [], [], []
        self.tables = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("a", "img") and (a.get("href") or a.get("src")):
            self.links.append(a.get("href") or a.get("src"))
        if tag == "table":
            self.tables += 1
            if a.get("dir") != "ltr":
                self.issues.append("Table must explicitly be LTR")
        if tag in ("td", "th"):
            self.cells.append((tag, a.get("dir"), a.get("lang"), a.get("align")))
        if tag in ("script", "iframe", "style"):
            self.issues.append("Unsupported/active HTML in GitHub Markdown: " + tag)

def check_text(text: str, file: Path, root: Path) -> tuple[list[str], int]:
    """Check narrative HTML and local file links, excluding fenced code examples."""
    text = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)
    parser = Parser()
    parser.feed(text)
    rel = str(file.relative_to(root))
    issues = [rel + ": " + issue for issue in parser.issues]
    if not parser.tables:
        issues.append(rel + ": missing bilingual table")
    for i in range(0, len(parser.cells), 2):
        cells = parser.cells[i:i+2]
        if len(cells) != 2 or cells[0][1:] != ("ltr", "en", "left") or cells[1][1:] != ("rtl", "ar", "right"):
            issues.append(rel + ": bilingual cell order/direction mismatch")
    count = 0
    refs = parser.links + re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', text)
    for ref in refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc or not url.path:
            continue
        count += 1
        target = (file.parent / unquote(url.path)).resolve()
        if not target.is_relative_to(root) or not target.exists():
            issues.append(f"Broken/escaping link: {rel} -> {ref}")
    return issues, count

def release_issues(root: Path, cfg: dict) -> list[str]:
    """Teaching readiness must precede remote creation; no published flag here."""
    issues = []
    pending = [lab["id"] for lab in cfg["labs"] if lab["status"] != "VERIFIED"]
    if pending:
        issues.append("Teaching release blocked: unverified labs " + ", ".join(pending))
    if any(n.get("kind") == "engine" and n.get("execution_status") != "VERIFIED" for n in cfg.get("notebooks", [])):
        issues.append("Teaching release blocked: engine notebook drafts remain")
    if cfg.get("day02_dbt_status") != "VERIFIED":
        issues.append("Teaching release blocked: required dbt demonstration is not verified")
    for component in ("day04_kafka_status", "day04_gx_status"):
        if cfg.get(component) != "VERIFIED":
            issues.append("Teaching release blocked: " + component + " lacks actual native evidence")
    issues.extend(engine_evidence_issues(root))
    issues.extend(dbt_evidence_issues(root))
    return issues

def inspect(root: Path) -> dict:
    root = Path(root).resolve()
    problems, warnings = [], []
    links_count = markdown_count = nb_count = python_count = 0
    files = [p for p in root.rglob("*") if p.is_file() and not any(x in SKIP for x in p.relative_to(root).parts)]
    cfg = json.loads((root / "course.json").read_text(encoding="utf-8"))
    if (cfg["days"], cfg["hours_per_day"], cfg["hours_total"]) != (5, 6, 30):
        problems.append("Wrong course duration")
    if not cfg.get("labs_are_final_project") or cfg.get("separate_final_project"):
        problems.append("Project scope changed")
    if cfg.get("distinction_required"):
        problems.append("Distinction must remain optional")
    if cfg.get("slides_current_scope"):
        problems.append("Slides are not in current scope")
    if len(cfg.get("labs", [])) != 8 or [l["id"] for l in cfg["labs"]] != [f"{i:02d}" for i in range(1, 9)]:
        problems.append("Exactly eight labs are required")
    for d in cfg["day_plan"]:
        if not (root / f'day{d["day"]:02d}/README.md').is_file():
            problems.append("Missing day hub")
    registry = {n["path"]: n for n in cfg.get("notebooks", [])}
    if len(registry) != len(cfg.get("notebooks", [])):
        problems.append("Duplicate notebook registry entry")
    for path in registry:
        if not (root / path).is_file():
            problems.append("Registered notebook missing: " + path)
    for p in files:
        rel = p.relative_to(root)
        name = rel.as_posix()
        if any(x in {"instructor_only", "authoring_private", "source_references", "private_build"} for x in rel.parts) or p.name == "INSTRUCTOR_PACKAGE.md":
            problems.append("Private path in public tree: " + name)
        if p.suffix.lower() in {".pptx", ".pem", ".key"} or p.name == ".env":
            problems.append("Prohibited/deferred file: " + name)
        if p.is_symlink():
            problems.append("Symlink requires review: " + name)
        if p.suffix == ".py":
            python_count += 1
            try:
                ast.parse(p.read_text(encoding="utf-8"))
            except SyntaxError as e:
                problems.append(f"{name}: {e}")
        if p.suffix == ".md":
            markdown_count += 1
            issues, count = check_text(p.read_text(encoding="utf-8"), p, root)
            problems.extend(issues)
            links_count += count
        if p.suffix == ".ipynb":
            nb_count += 1
            nb = json.loads(p.read_text(encoding="utf-8"))
            rec = registry.get(name)
            meta = nb.get("metadata", {}).get("masar", {})
            if not rec:
                problems.append(name + ": notebook must be registered with its execution boundary")
                continue
            for key in ("execution_status", "lab_id", "engine_verified"):
                if meta.get(key) != rec.get(key):
                    problems.append(name + ": registry/metadata mismatch for " + key)
            draft = rec.get("execution_status") == "ENGINE_NOT_EXECUTED"
            if draft:
                if rec.get("kind") != "engine" or meta.get("engine_verified") is not False:
                    problems.append(name + ": invalid engine-draft classification")
                warnings.append(name + ": authored engine draft; NOT EXECUTED")
            elif rec.get("execution_status") == "VERIFIED":
                if rec.get("kind") != "engine" or meta.get("engine_verified") is not True:
                    problems.append(name + ": verified engine notebook must declare its actual kind")
            elif rec.get("execution_status") != "EXECUTED_HELPER":
                problems.append(name + ": execution status requires a reviewed engine-evidence implementation")
            if rec.get("kind") == "preparatory" and meta.get("engine_verified") is not False:
                problems.append(name + ": helper cannot claim engine verification")
            markdown = []
            for i, cell in enumerate(nb.get("cells", [])):
                source = "".join(cell.get("source", []))
                if cell.get("cell_type") == "markdown":
                    markdown.append(source)
                if cell.get("cell_type") == "code":
                    try:
                        ast.parse(source)
                    except SyntaxError as e:
                        problems.append(f"{name}: syntax error cell {i}: {e}")
                    outputs = cell.get("outputs", [])
                    if draft:
                        if cell.get("execution_count") is not None or outputs:
                            problems.append(f"{name}: unexecuted draft contains claimed execution/output")
                    else:
                        if cell.get("execution_count") is None:
                            problems.append(f"{name}: unexecuted helper cell {i}")
                        if any(o.get("output_type") == "error" for o in outputs):
                            problems.append(f"{name}: saved runtime error")
            joined = "\n\n".join(markdown)
            if rec.get("execution_status") == "VERIFIED" and "ENGINE_NOT_EXECUTED" in joined:
                problems.append(name + ": verified notebook still carries an unexecuted notice")
            if draft and "ENGINE_NOT_EXECUTED" not in joined:
                problems.append(name + ": visible engine-draft notice missing")
            issues, count = check_text(joined, p, root)
            problems.extend(issues)
            links_count += count
    data = root / "data/masar-small-v1"
    manifest_path = data / "manifest.json"
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != PINNED_MANIFEST:
        problems.append("Approved manifest changed, even if payload hashes were recomputed")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for rec in manifest["files"]:
        target = (data / rec["path"]).resolve()
        if (not target.is_relative_to(data.resolve()) or not target.is_file()
                or hashlib.sha256(target.read_bytes()).hexdigest() != rec["sha256"]):
            problems.append("Dataset integrity mismatch: " + rec["path"])
    return {"scope": "SOURCE_AUTHORING_AND_SAVED_HELPER_OUTPUTS_ONLY", "passed": not problems,
        "files": len(files), "markdown_pages": markdown_count, "relative_links_checked": links_count,
        "notebooks": nb_count, "python_files_parsed": python_count, "issues": problems, "warnings": warnings,
        "does_not_prove": ["engine execution", "GitHub rendering", "anonymous remote access", "publication approval", "complete course readiness"]}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", action="store_true", help="Check teaching readiness, independent of publication")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = inspect(ROOT)
    if args.release:
        cfg = json.loads((ROOT / "course.json").read_text(encoding="utf-8"))
        report["scope"] = "TEACHING_RELEASE_READINESS_NOT_PUBLICATION"
        report["issues"].extend(release_issues(ROOT, cfg))
        report["passed"] = not report["issues"]
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
