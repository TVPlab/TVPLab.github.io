"""Regenerate English dropdown navigation, then run build_zh.py."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent.parent
OLD = 'https://www.tvplab-cambridge.com/'
GROUPS = [
 ('About', ['about','antonio-vidal-puig'], [('Lab overview','about.html'),('Principal Investigator','antonio-vidal-puig.html'),('Mission and facilities','about.html#mission'),('Life at TVPlab','index.html#gallery-title')]),
 ('Research', ['research','nanjing','valencia','collaborators'], [('Our science',None),('Research overview','research.html'),('Adipose biology','research.html#adipose-biology'),('Lipotoxicity','research.html#lipotoxicity'),('Thermogenesis','research.html#thermogenesis'),('Immunometabolism','research.html#immunometabolism'),('Publications','publications.html'),('Across borders',None),('TVPlab in Nanjing','nanjing.html'),('TVPlab in Valencia','valencia.html'),('Our collaborators','collaborators.html'),('In the media',OLD+'in-the-media'),('Seminars',OLD+'technical-seminars')]),
 ('People', ['people'], [('All people','people.html'),('Principal Investigator','people.html#toni'),('Personal Assistant','people.html#katie'),('Operations Scientific Management Lead','people.html#mark'),('Research Associates','people.html#role-researchers'),('Research Assistants','people.html#role-assistants'),('PhD Students','people.html#role-students'),('Visitors','people.html#role-visitors'),('Lab Communication Director','people.html#kaida'),('Alumni','people.html#role-alumni')]),
 ('Publications', ['publications'], [('Browse publications','publications.html'),('Research overview','research.html'),('Our collaborators','collaborators.html')]),
 ('News & Events', ['news'], [('News overview','news.html'),('Collaborations','news.html?topic=collaboration#archive'),('Careers & growth','news.html?topic=growth#archive'),('Conferences & seminars','news.html?topic=conference#archive'),('Lab life','news.html?topic=life#archive'),('Life at TVPlab','index.html#gallery-title'),('In the media',OLD+'in-the-media'),('Seminars',OLD+'technical-seminars')]),
 ('Join Us', ['vacancies'], [('Join the lab','vacancies.html#opportunities'),('Recruitment and training','vacancies.html#training'),('Contact the lab','contact.html')]),
 ('Contact', ['contact'], [('Contact overview','contact.html'),('Find the lab','contact.html#find-us'),('Write to us','contact.html#contact-form')]),
]

def navigation(current):
 out = '<nav class="site-nav" id="primary-navigation" aria-label="Main navigation">'
 for label, pages, items in GROUPS:
  key=label.lower().replace(' & ','-').replace(' ','-')
  out += '<details class="nav-group'+(' nav-wide' if label in ['Research','People'] else '')+(' active' if current in pages else '')+'" name="primary-menu" id="nav-'+key+'">'
  out += '<summary>'+escape(label)+'<svg class="nav-chevron" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="m5 7 5 5 5-5"/></svg></summary><div class="nav-panel">'
  if label=='Research':out+='<div class="nav-column">'
  for title, href in items:
   if href is None:
    if title=='Across borders':out+='</div><div class="nav-column nav-featured">'
    out+='<p class="nav-label">'+escape(title)+'</p>';continue
   external=href.startswith('https:')
   out+='<a href="'+href+'"'+(' target="_blank" rel="noopener"' if external else '')+(' aria-current="page"' if href==current+'.html' else '')+'><span>'+escape(title)+'</span>'
   if external:out+='<small>Original website <span aria-hidden="true">↗</span></small>'
   out+='</a>'
  if label=='Research':out+='</div>'
  out+='</div></details>'
 return out+'</nav>'

for p in ROOT.glob('*.html'):
 s=p.read_text()
 s=re.sub(r'<nav class="site-nav".*?</nav>',navigation(p.stem),s,flags=re.S)
 if 'navigation.css' not in s:
  s=s.replace('</head>','<link rel="stylesheet" href="navigation.css?v=20260921-1" />\n<script src="navigation.js?v=20260921-1" defer></script>\n</head>')
 p.write_text(s)
