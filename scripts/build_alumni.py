"""Build the opt-in alumni directory from the original lab website records."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parent.parent
rows=json.loads((ROOT/'data/alumni.json').read_text())
cards=[]
for p in rows:
 cards.append(f'''<article class="alumni-card" id="alumni-{p['id']}" aria-labelledby="alumni-name-{p['id']}"><img src="{p['photo']}" width="{p['width']}" height="{p['height']}" alt="{escape(p['name'])}" loading="lazy" decoding="async" /><div><h3 id="alumni-name-{p['id']}">{escape(p['name'])}</h3><p>{escape(p['details'])}</p><a href="{p['source']}" target="_blank" rel="noopener">Original profile <span aria-hidden="true">↗</span></a></div></article>''')
section='''<!-- alumni:start --><section class="alumni-directory" id="alumni-directory" aria-labelledby="alumni-title" hidden><div class="alumni-intro"><p class="eyebrow">Our wider community</p><h2 id="alumni-title">Former TVPlab members</h2><p>Celebrating the people who have been part of our laboratory. Roles and affiliations below are recorded as listed on our original website.</p></div><div class="alumni-grid">'''+''.join(cards)+'''</div></section><!-- alumni:end -->'''
p=ROOT/'people.html';s=p.read_text()
s=re.sub(r'<!-- alumni:start -->.*?<!-- alumni:end -->','',s,flags=re.S)
s=s.replace('</main>',section+'\n</main>')
if 'data-team-filter="alumni"' not in s:
 s=s.replace('>Visitors</button></div>','>Visitors</button><button type="button" data-team-filter="alumni" id="role-alumni" aria-pressed="false" aria-controls="alumni-directory">Alumni</button></div>')
s=s.replace('>View all</button>','>Current members</button>')
s=s.replace('people.css?v=','people.css?v=alumni-').replace('people.js?v=','people.js?v=alumni-') if 'people.css?v=alumni-' not in s else s
p.write_text(s)
i18n={'Alumni':'往届成员','Current members':'现任成员','Our wider community':'我们共同的科研历程','Former TVPlab members':'TVPlab 往届成员','Celebrating the people who have been part of our laboratory. Roles and affiliations below are recorded as listed on our original website.':'致敬曾在实验室工作与学习的伙伴。以下职务与机构信息沿用原网站的记录。','Original profile':'原网站资料'}
for p in rows:
 i18n[p['details']]=p['details_zh']
 i18n[p['name']]=p['name']
(ROOT/'data/alumni-i18n.json').write_text(json.dumps(i18n,ensure_ascii=False,indent=2)+'\n')
print('Built',len(rows),'alumni cards')
