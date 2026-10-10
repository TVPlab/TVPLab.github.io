"""Build bilingual, static member homepages and their directory links.

Run after the navigation and Chinese-page builders. Uses the existing approved
biographies; source URLs remain in data files for editorial reference only.
"""
from pathlib import Path
from html import escape
import json
import os
import re

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = 'https://tvplab.github.io/'
MEMBERS = json.loads((ROOT / 'data/member-profiles.json').read_text())
SUMMARIES = {p['id']: p for p in json.loads((ROOT / 'data/people-summaries.json').read_text())}
ALUMNI = json.loads((ROOT / 'data/alumni.json').read_text())
DETAILS = json.loads((ROOT / 'data/profile-details.json').read_text())


def local(p, field, zh):
    return p.get(field + '_zh', p.get(field, '')) if zh else p.get(field, '')


def tr(en, zh, cn):
    return zh if cn else en


def current_card(p, cn):
    name, role = local(p, 'name', cn), local(p, 'role', cn)
    summary = local(SUMMARIES[p['id']], 'summary', cn)
    image = ('../' if cn else '') + p['photo']
    return f'''<article class="team-card" id="{p['id']}" data-team-category="{p['category']}">
<a class="team-card-link" href="people/{p['slug']}.html" aria-labelledby="{p['id']}-name {p['id']}-role">
<span class="team-portrait"><img src="{image}" alt="" width="{p['width']}" height="{p['height']}" loading="lazy" decoding="async" /></span>
<span class="team-caption"><span class="team-identity"><span class="team-name" id="{p['id']}-name">{escape(name)}</span><span class="team-role" id="{p['id']}-role">{escape(role)}</span></span>
<span class="team-excerpt">{escape(summary)}</span><span class="team-read">{tr('View profile', '查看个人主页', cn)}<span aria-hidden="true">→</span></span></span></a></article>'''


def alumni_card(p, cn):
    href = f"people/{p['id']}.html"
    name = escape(p['name'])
    return f'''<article class="alumni-card" id="alumni-{p['id']}" aria-labelledby="alumni-name-{p['id']}">
<a class="alumni-portrait-link" href="{href}" aria-label="{name}"><img src="{('../' if cn else '') + p['photo']}" width="{p['width']}" height="{p['height']}" alt="" loading="lazy" decoding="async" /></a>
<div><h3 id="alumni-name-{p['id']}"><a href="{href}">{name}</a></h3><p>{escape(local(p, 'details', cn))}</p><a href="{href}">{tr('View profile', '查看个人主页', cn)} <span aria-hidden="true">→</span></a></div></article>'''


def rebase(fragment):
    # Templates are one level above their profile directories, in both languages.
    def rewrite(m):
        attr, url = m.groups()
        if not url or url.startswith(('https:', 'http:', 'mailto:', 'tel:', '#', '/', 'data:')):
            return m.group()
        return f'{attr}="../{url}"'
    return re.sub(r'(href|src)="([^"]*)"', rewrite, fragment)


def linked_text(text):
    """Render source text safely; link explicit URLs, never infer destinations."""
    pieces = []
    position = 0
    for match in re.finditer(r'https?://[^\s<>]+', text):
        url = match.group().rstrip('.,;)')
        pieces.append(escape(text[position:match.start()]))
        # The original Ruoqi page has a truncated DOI, not a usable destination.
        if url == 'https://dx.doi.org/10.21037/e':
            pieces.append(escape(url))
        else:
            pieces.append(f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener">{escape(url)}</a>')
        position = match.start() + len(url)
    pieces.append(escape(text[position:]))
    return ''.join(pieces)


def full_details(person_id, cn):
    data = DETAILS.get(person_id)
    if not data:
        return '', '', ''
    contact = ''
    if data['emails']:
        emails = ''.join(f'<a href="mailto:{escape(email)}">{escape(email)}</a>' for email in data['emails'])
        contact = f'<div class="profile-contact"><span>{tr("Email", "电子邮箱", cn)}</span>{emails}</div>'
    sections, navigation = [], []
    for section in data['sections']:
        key = section['id']
        heading = local(section, 'heading', cn)
        navigation.append(f'<a href="#{key}">{escape(heading)}</a>')
        items = [linked_text(local(item, 'text', cn)) for item in section['items']]
        if key == 'publications':
            content = '<ol class="profile-publications" lang="en">' + ''.join('<li>' + item + '</li>' for item in items) + '</ol>'
        elif key == 'interests' and person_id == 'sergio':
            content = '<ol class="profile-interests">' + ''.join('<li>' + item + '</li>' for item in items) + '</ol>'
        elif key == 'interests' and person_id == 'mark':
            content = '<p>' + items[0] + '</p><ul>' + ''.join('<li>' + item + '</li>' for item in items[1:]) + '</ul>'
        else:
            content = ''.join('<p>' + item + '</p>' for item in items)
        sections.append(f'<section class="profile-detail-section" id="{key}" aria-labelledby="{key}-heading"><h2 id="{key}-heading">{escape(heading)}</h2>{content}</section>')
    if data['links']:
        navigation.append(f'<a href="#professional-links">{tr("Professional links", "学术与专业链接", cn)}</a>')
        links = ''.join(f'<li><a href="{escape(link["url"], quote=True)}" target="_blank" rel="noopener">{escape(local(link, "label", cn))} <span aria-hidden="true">↗</span></a></li>' for link in data['links'])
        sections.append(f'<section class="profile-detail-section" id="professional-links" aria-labelledby="professional-links-heading"><h2 id="professional-links-heading">{tr("Professional links", "学术与专业链接", cn)}</h2><ul class="profile-professional-links">{links}</ul></section>')
    nav = f'<nav class="profile-contents" aria-label="{tr("On this page", "本页目录", cn)}"><span>{tr("On this page", "本页目录", cn)}</span>{"".join(navigation)}</nav>' if navigation else ''
    body = '<div class="profile-full-details">' + ''.join(sections) + '</div>' if sections else ''
    return contact, nav, body


def render_profile(p, cn, header, footer, previous, following, alumni=False):
    slug = p['id'] if alumni else p['slug']
    base = ROOT / 'zh' if cn else ROOT
    output = base / 'people' / (slug + '.html')
    output.parent.mkdir(exist_ok=True)
    rel = lambda path: os.path.relpath(ROOT / path, output.parent).replace(os.sep, '/')
    name = local(p, 'name', cn)
    role = tr('Former TVPlab member', 'TVPlab 往届成员', cn) if alumni else local(p, 'role', cn)
    summary = local(p, 'details', cn) if alumni else local(SUMMARIES[p['id']], 'summary', cn)
    contact, contents, full_body = full_details(p['id'], cn)
    en = rel(f'people/{slug}.html')
    zh = rel(f'zh/people/{slug}.html')
    header = rebase(header)
    # The directory is an ancestor, not the active document.
    header = header.replace(' aria-current="page"', '')
    languages = f'''<nav class="language-switch" aria-label="{tr('Language', '语言', cn)}"><a href="{en}" data-language="en" lang="en" hreflang="en"{' aria-current="true"' if not cn else ''}>EN</a><a href="{zh}" data-language="zh" lang="zh-CN" hreflang="zh-CN"{' aria-current="true"' if cn else ''}>中文</a></nav>'''
    header = re.sub(r'<nav class="language-switch".*?</nav>', languages, header, flags=re.S)
    back = '../people.html' + ('#role-alumni' if alumni else '#' + p['id'])
    label = tr('Alumni', '往届成员', cn) if alumni else tr('Our people', '团队成员', cn)
    sections = ''
    if alumni:
        sections += f'<p class="profile-archive-note">{tr("This is an archived member profile. The biography, roles, affiliations and contact details reflect the original lab website and may not be current.", "这是往届成员的历史资料。简介、职务、机构与联系方式反映原网站记录，可能并非当前情况。", cn)}</p>'
    extras = ''
    if p['id'] == 'toni':
        extras = f'<a href="../antonio-vidal-puig.html">{tr("Full academic biography", "完整学术履历", cn)} <span aria-hidden="true">→</span></a>'
    actions = f'<a href="../research.html">{tr("Explore our research", "了解研究方向", cn)} <span aria-hidden="true">→</span></a>' if not alumni else ''
    related = ''
    for other, direction in [(previous, 'previous'), (following, 'next')]:
        if other is None:
            related += '<span></span>'
            continue
        other_slug = other['id'] if alumni else other['slug']
        direction_text = tr('Previous profile', '上一位成员', cn) if direction == 'previous' else tr('Next profile', '下一位成员', cn)
        related += f'<a href="{other_slug}.html"><span>{direction_text}</span><strong>{escape(local(other, "name", cn))}</strong></a>'
    title = escape(name + ' — TVPlab')
    canonical = ORIGIN + output.relative_to(ROOT).as_posix()
    css = ''.join(f'<link rel="stylesheet" href="{rel(f + ".css")}?v=profiles-full-20261010" />' for f in ['styles', 'refresh', 'controls', 'navigation', 'profiles'])
    js = ''.join(f'<script src="{rel(f + ".js")}?v=20260921-2" defer></script>' for f in ['site', 'navigation'])
    page = f'''<!DOCTYPE html>
<html lang="{'zh-CN' if cn else 'en'}"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title><meta name="description" content="{escape(summary, quote=True)}" />
<link rel="canonical" href="{canonical}" /><link rel="alternate" hreflang="en" href="{en}" /><link rel="alternate" hreflang="zh-CN" href="{zh}" />{css}{js}</head>
<body class="inner-page member-profile-page"><a class="skip-link" href="#main-content">{tr('Skip to content', '跳转到正文', cn)}</a>{header}
<main id="main-content" class="profile-main">
<nav class="profile-breadcrumb" aria-label="{tr('Breadcrumb', '当前位置', cn)}"><a href="../people.html">{tr('People', '团队成员', cn)}</a><span aria-hidden="true">/</span><span>{escape(name)}</span></nav>
<article class="profile-layout">
<figure class="profile-portrait{' profile-portrait-alumni' if alumni else ''}"><img src="{rel(p['photo'])}" alt="{escape(name)}" width="{p['width']}" height="{p['height']}" fetchpriority="high" decoding="async" /></figure>
<div class="profile-copy"><p class="profile-eyebrow">{tr('Our wider community', '我们共同的科研历程', cn) if alumni else 'TVPlab · Cambridge'}</p><h1>{escape(name)}</h1><p class="profile-role">{escape(role)}</p>
{contact}<div class="profile-overview"><h2>{tr('Profile', '个人简介', cn)}</h2><p>{escape(summary)}</p></div>{sections}
<div class="profile-actions">{extras}{actions}<a href="{back}">{tr('Back to ', '返回', cn)}{label} <span aria-hidden="true">↗</span></a></div></div></article>
{contents}{full_body}
<nav class="profile-adjacent" aria-label="{tr('Browse member profiles', '浏览成员主页', cn)}">{related}</nav>
</main>{rebase(footer)}</body></html>'''
    output.write_text(page)


def build():
    for cn in [False, True]:
        base = ROOT / 'zh' if cn else ROOT
        path = base / 'people.html'
        text = path.read_text()
        cards = ''.join(current_card(p, cn) for p in MEMBERS)
        text, count = re.subn(r'<div class="team-grid" id="team-grid">.*?</div>\s*</section>', '<div class="team-grid" id="team-grid">' + cards + '</div>\n</section>', text, count=1, flags=re.S)
        assert count == 1, 'Could not find current-member grid'
        text, count = re.subn(r'<div class="alumni-grid">.*?</div></section><!-- alumni:end -->', '<div class="alumni-grid">' + ''.join(alumni_card(p, cn) for p in ALUMNI) + '</div></section><!-- alumni:end -->', text, count=1, flags=re.S)
        assert count == 1, 'Could not find alumni grid'
        text = re.sub(r'(people\.(?:css|js))\?[^"\s]+', r'\1?v=profiles-20261010', text)
        path.write_text(text)
        header = re.search(r'<header class="site-header">.*?</header>', text, re.S).group()
        footer = re.search(r'<footer class="site-footer">.*?</footer>', text, re.S).group()
        for group, former in [(MEMBERS, False), (ALUMNI, True)]:
            for i, person in enumerate(group):
                render_profile(person, cn, header, footer, group[i - 1] if i else None, group[i + 1] if i + 1 < len(group) else None, former)
    print(f'Built {len(MEMBERS) + len(ALUMNI)} member profiles in English and Chinese, with local directory links.')


if __name__ == '__main__':
    build()
