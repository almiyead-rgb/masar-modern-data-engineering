"""Keep dbt's supported classroom interpreter explicit in its preflight."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'src/masar/dbt_lab.py'
text=p.read_text(encoding='utf-8')
if '\nimport sys\n' not in text:
    text=text.replace('\nimport os\n','\nimport os\nimport sys\n')
needle="    report['scope'] = 'DBT_DEPENDENCY_PREFLIGHT_ONLY'"
if 'sys.version_info[:2] != (3, 11)' not in text:
    text=text.replace(needle,"    if sys.version_info[:2] != (3, 11):\n        report['issues'].append('The dbt session runtime requires Python 3.11')\n"+needle)
compile(text,str(p),'exec')
p.write_text(text,encoding='utf-8')
print('dbt interpreter preflight matches the course environment.')
