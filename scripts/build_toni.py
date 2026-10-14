"""Build the academic biography from the same CV data as Toni's member profile."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parent.parent

def build():
    data=json.loads((ROOT/'data/profile-details.json').read_text())['toni']
    sections=[]
    for section in data['sections']:
        paragraphs=''.join('<p style="font-size:16px; line-height:1.9; color:var(--muted); margin-bottom:20px;">'+escape(item['text'])+'</p>' for item in section['items'])
        sections.append('<section class="zw-section" id="'+section['id']+'"><h2 class="zw-section-label">'+escape(section['heading'])+'</h2>'+paragraphs+'</section>')
    links='<div class="pi-links"><a class="pi-link-btn" href="mailto:ajv22@medschl.cam.ac.uk">Email</a><a class="pi-link-btn" href="publications.html">Publications page</a><a class="pi-link-btn" href="https://scholar.google.com/citations?user=Z-B7RdUAAAAJ" target="_blank" rel="noopener">Google Scholar</a></div>'
    path=ROOT/'antonio-vidal-puig.html'
    s=path.read_text()
    s=re.sub(r'<div class="inner-wrap">[\s\S]*?</main>', '<div class="inner-wrap">\n'+links+'\n'+'\n'.join(sections)+'\n</div>\n</main>',s,count=1)
    path.write_text(s)

if __name__=='__main__':
    build()
