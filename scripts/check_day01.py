from pathlib import Path
import hashlib,json,re,sys
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from masar.sources import verify_manifest
verify_manifest(ROOT/'data/masar-small-v1')
required=['DAY01_STUDENT.ipynb','README.md','course.json','resources/Masar_Cost_Model.xlsx']
required += ['day01/'+x+'.md' for x in ['README','CONCEPTS','GLOSSARY','SOURCES','PRACTICE','COMPLETION']]
required += [f'labs/lab0{i}/{x}.md' for i in (1,2) for x in ('README','WALKTHROUGH')]
assert all((ROOT/p).is_file() for p in required)
import nbformat
for p in [ROOT/'DAY01_STUDENT.ipynb',*(ROOT/'notebooks/day01').glob('*.ipynb')]:nbformat.validate(nbformat.read(p,4))
errors=[];count=0
for p in ROOT.rglob('*.md'):
 if any(x in p.parts for x in ['outputs','.git','.venv']):continue
 text=p.read_text(encoding='utf-8')
 for target in re.findall(r'href=["\']([^"\']+)["\']',text)+re.findall(r'\]\(([^)]+)\)',text):
  u=urlsplit(target)
  if u.scheme or not u.path:continue
  count+=1
  if not (p.parent/unquote(u.path)).resolve().exists():errors.append((str(p.relative_to(ROOT)),target))
assert not errors,errors
print(json.dumps({'required_files':len(required),'internal_links':count,'dataset':'unchanged','notebooks':'valid'},indent=2))
