"""Build the bilingual dated archive and homepage highlights from data/news.json.
Run build_navigation.py, then build_zh.py (which calls this builder).
"""
from pathlib import Path
from html import escape
from datetime import date
import json,re
ROOT=Path(__file__).resolve().parent.parent
ROWS=json.loads((ROOT/'data/news.json').read_text())
CATS={'all':('All stories','全部动态'),'collaboration':('Collaborations','科研合作'),'growth':('Careers & growth','职业与成长'),'conference':('Conferences & seminars','会议与讲座'),'publication':('Publications','研究论文'),'outreach':('Public engagement','公众科普'),'fundraising':('Fundraising','慈善筹款'),'life':('Lab life','实验室生活')}
SVG='<span aria-hidden="true" class="cell-emblem"><svg class="cell-icon" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path class="cell-membrane" d="M25 3C37 2 45 12 45 24c1 12-9 21-21 21C12 46 3 37 3 25 2 13 12 3 25 3Z"/><path class="cell-lipid" d="M26 9c9-1 14 6 13 15 0 9-6 15-15 15-9 0-15-6-14-15 0-8 7-15 16-15Z"/><ellipse class="cell-nucleus" cx="9" cy="32" rx="2.3" ry="4" transform="rotate(-27 9 32)"/><path class="cell-arrow" d="M18 30 30 18M19 18h11v11"/></svg></span>'
def tr(en,zh,cn):return zh if cn else en
def field(x,key,cn):return x.get(key+'_zh',x[key]) if cn else x[key]
def day(d,cn=False):
 v=date.fromisoformat(d);return f'{v.year}年{v.month}月{v.day}日' if cn else f'{v.day} {v.strftime("%B %Y")}'
def photo(x,cn=False,idx=0,home=False):
 if len(x['photos'])<=idx:return '<div class="story-no-photo" aria-hidden="true">'+SVG+'</div>'
 p=x['photos'][idx];src=('../' if cn else '')+p['path'];alt=field(p,'caption',cn) if p.get('caption') else tr('Image from the original post: ','原始动态配图：',cn)+field(x,'title',cn)
 return f'<img src="{src}" alt="{escape(alt)}" width="{p["width"]}" height="{p["height"]}" loading="lazy" decoding="async" />'+(f'<span class="photo-credit">{escape(alt)}</span>' if p.get('caption') else '')
def home(cn):
 items=''
 for x in ROWS[:3]:
  items+=f'<a class="home-news-item" href="news.html#{x["id"]}"><div class="home-story-image">{photo(x,cn,home=True)}</div><span class="story-meta"><time datetime="{x["published"]}">{day(x["published"],cn)}</time><span>{CATS[x["topic"]][cn]}</span></span><h3>{escape(field(x,"title",cn))}</h3><p>{escape(field(x,"summary",cn))}</p><span class="tile-link">{tr("Read update","阅读动态",cn)} {SVG}</span></a>'
 return f'<section class="home-news content-width" id="latest-news"><div class="section-top"><div><p class="eyebrow">{tr("From the laboratory","实验室动态",cn)}</p><h2>{tr("News &amp; events","新闻与活动",cn)}</h2></div><a class="text-link" href="news.html">{tr("All updates","全部动态",cn)} {SVG}</a></div><div class="home-news-grid">{items}</div></section>'
def card(x,cn):
 title=escape(field(x,'title',cn));body=''.join('<p>'+escape(p)+'</p>' for p in field(x,'body',cn));links=''
 for i,l in enumerate(x['links']):
  label=l.get('label_zh') if cn else l['label']
  if not label:label='相关链接 '+str(i+1)
  if label.lower() in ['here','this one','website']:label=tr('Related link ','相关链接 ',cn)+str(i+1)
  links+=f'<a href="{escape(l["url"],quote=True)}" target="_blank" rel="noopener">{escape(label)} <span aria-hidden="true">↗</span></a>'
 gallery=''.join(f'<a href="{("../" if cn else "")+p["path"]}" target="_blank" rel="noopener">{photo(x,cn,i)}</a>' for i,p in enumerate(x['photos']))
 event=f'<p class="story-event-date">{tr("Event date","活动日期",cn)}: <time datetime="{x["eventDate"]}">{day(x["eventDate"],cn)}</time></p>' if x.get('eventDate') else ''
 source=tr('Original lab post','实验室原始文章',cn) if x['sourceType']=='archive' else tr('Toni’s LinkedIn post','Toni 的 LinkedIn 原帖',cn)
 if x['sourceType']=='lab':source=tr('Lab announcement and photographs supplied by TVPlab','资料来源：TVPlab 提供的通知与照片',cn)
 origin=tr('Lab archive','实验室档案',cn) if x['sourceType']=='archive' else tr('From Toni’s LinkedIn','来自 Toni 的 LinkedIn',cn)
 if x['sourceType']=='lab':origin=tr('From TVPlab','来自 TVPlab',cn)
 source_markup=(f'<a href="{escape(x["sourceUrl"],quote=True)}" target="_blank" rel="noopener">{source} <span aria-hidden="true">↗</span></a>' if x.get('sourceUrl') else f'<span>{source}</span>')
 archive_note='<p class="story-source-note">'+tr('An archived lab story. References to roles, opportunities and campaigns reflect the original publication date.','实验室历史记录。文中职务、机会与筹款活动均反映原文发布时的情况。',cn)+'</p>' if x['sourceType']=='archive' else ''
 return f'''<article class="archive-story" id="{x['id']}" data-date="{x['published']}" data-topic="{x['topic']}" data-year="{x['published'][:4]}" aria-labelledby="title-{x['id']}"><div class="story-picture">{photo(x,cn)}</div><div class="story-content"><div class="story-meta"><span class="story-topic">{CATS[x['topic']][cn]}</span><span>{tr('Published','发布于',cn)} <time datetime="{x['published']}">{day(x['published'],cn)}</time></span></div><h2 id="title-{x['id']}">{title}</h2>{event}<p class="story-summary">{escape(field(x,'summary',cn))}</p><details class="story-details"><summary><span>{tr('Read story','阅读详情',cn)}</span>{SVG}</summary><div class="story-full">{archive_note}{body}<div class="story-gallery">{gallery}</div><div class="story-source-links">{source_markup}{links}</div></div></details><div class="story-foot"><span>{origin}</span><a class="story-permalink" href="#{x['id']}" aria-label="{escape(tr('Link to: ','链接至：',cn)+field(x,'title',cn),quote=True)}">{tr('Permalink','本条链接',cn)}</a></div></div></article>'''
def main(cn):
 count=len(ROWS);years=sorted({x['published'][:4] for x in ROWS},reverse=True)
 chips=''.join(f'<button type="button" data-topic-filter="{key}" aria-pressed="{str(key=="all").lower()}">{v[cn]}</button>' for key,v in CATS.items())
 options=''.join(f'<option value="{y}">{y}</option>' for y in years)
 event=next(x for x in ROWS if x['id']=='cipf-research-careers-open-day-2026')
 return f'''<main id="main-content"><section class="news-masthead"><div class="content-width"><p class="eyebrow">{tr('Discovery. Connections. People.','发现 · 合作 · 成长',cn)}</p><h1>{tr('News &amp; Events','新闻与活动',cn)}</h1><div class="news-masthead-bottom"><p>{tr('Research across borders, milestones worth celebrating, and life in our lab. Explore the stories behind TVPlab.','跨越国界的科研合作、值得庆祝的成长时刻，以及实验室里的日常。一起了解 TVPlab 的故事。',cn)}</p><p class="archive-scope"><strong>{count}</strong> {tr('stories','篇动态',cn)}<span>2017 — 2026</span></p></div></div></section>
<section class="calendar-feature content-width" aria-labelledby="calendar-title" data-event-date="2026-09-25"><div><p class="eyebrow">{tr('On the calendar','活动日历',cn)}</p><p class="calendar-date">25 <span>{tr('September 2026','2026年9月',cn)}</span></p><p>{tr('15:30 · UK time (BST)','15:30 · 英国时间（BST）',cn)}</p></div><div><h2 id="calendar-title">{escape(field(event,'title',cn))}</h2><p>{escape(field(event,'summary',cn))}</p><div class="calendar-actions"><a class="text-link" href="#{event['id']}">{tr('Explore the event','了解活动',cn)} {SVG}</a><a class="calendar-download" href="{('../' if cn else '')}events/cipf-careers-2026.ics" download>{tr('Add to calendar','添加到日历',cn)} <span aria-hidden="true">+</span></a></div></div></section>
<section class="news-archive content-width" id="archive" aria-labelledby="archive-title"><div class="archive-heading"><div><p class="eyebrow">{tr('The archive','动态档案',cn)}</p><h2 id="archive-title">{tr('Our stories, through the years.','这些年，我们的故事。',cn)}</h2></div><p>{tr('Newest publication first','按发布时间从新到旧排列',cn)}</p></div><div class="news-tools" hidden><div class="news-search-row"><label class="news-search">{tr('Search stories','搜索动态',cn)}<input type="search" id="news-search" placeholder="{tr('Try Nanjing, PhD, or a name…','搜索南京、博士或成员姓名…',cn)}" /></label><label>{tr('Year','年份',cn)}<select id="news-year"><option value="all">{tr('All years','全部年份',cn)}</option>{options}</select></label><label>{tr('Order','排序',cn)}<select id="news-sort"><option value="newest">{tr('Newest first','从新到旧',cn)}</option><option value="oldest">{tr('Oldest first','从旧到新',cn)}</option></select></label></div><div class="news-topic-filters" role="group" aria-label="{tr('Filter news by topic','按主题筛选动态',cn)}">{chips}</div><div class="news-result-row"><p id="news-results" role="status" aria-live="polite"></p><button type="button" id="news-reset">{tr('Reset filters','重置筛选',cn)}</button></div></div><div id="news-stories">{''.join(card(x,cn) for x in ROWS)}</div><p id="news-empty" hidden>{tr('No stories match these filters. Try another keyword or reset the filters.','没有符合条件的动态，请尝试其他关键词或重置筛选。',cn)}</p><div class="news-more"><button type="button" id="news-more" hidden>{tr('Show more stories','加载更多动态',cn)} {SVG}</button></div><p class="news-editorial-note">{tr('Lab news, the original archive and selected public updates from Toni’s LinkedIn. Times use Europe/London (UK time); overseas event locations are noted. Publication dates determine the order; event dates are shown separately. Last reviewed: 22 September 2026.','本页收录实验室新闻、原始档案及 Toni 的部分公开 LinkedIn 动态。时间按英国 Europe/London 时区显示，海外活动地点另行注明。按发布时间排序，活动日期单独标注。最近核对：2026年9月22日。',cn)}</p></section></main>'''
for cn in [False,True]:
 prefix=ROOT/'zh' if cn else ROOT
 index=prefix/'index.html';s=index.read_text()
 s=re.sub(r'<section class="home-news\b.*?</section>',home(cn),s,flags=re.S)
 if 'news.css' not in s:s=s.replace('</head>',f'<link rel="stylesheet" href="{("../" if cn else "")}news.css?v=20260921-1" /></head>')
 index.write_text(s)
 header=re.search(r'<header class="site-header">.*?</header>',s,re.S).group()
 header=header.replace('class="nav-group" name="primary-menu" id="nav-news-events"','class="nav-group active" name="primary-menu" id="nav-news-events"')
 header=re.sub(r'(<a href="news.html")(>)',r'\1 aria-current="page"\2',header,count=1)
 header=re.sub(r'(<nav class="language-switch".*?</nav>)',lambda m:m.group().replace('index.html','news.html'),header,flags=re.S)
 footer=re.search(r'<footer class="site-footer">.*?</footer>',s,re.S).group()
 rel='../' if cn else ''
 title=tr('News & Events — TVPlab','新闻与活动 — TVPlab',cn)
 head=f'''<!DOCTYPE html><html lang="{'zh-CN' if cn else 'en'}"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><title>{title}</title><meta name="description" content="{tr('News, collaborations, career milestones and events from TVPlab, Cambridge. Browse the dated archive and upcoming activities.','TVPlab 新闻、科研合作、职业成长与活动。按日期浏览实验室档案与活动信息。',cn)}" /><link rel="alternate" hreflang="en" href="{rel}news.html" /><link rel="alternate" hreflang="zh-CN" href="{'news.html' if cn else 'zh/news.html'}" />'''
 for css in ['styles','refresh','controls','navigation','news']:head+=f'<link rel="stylesheet" href="{rel}{css}.css?v=20260922-1" />'
 for js in ['site','navigation','news']:head+=f'<script src="{rel}{js}.js?v=20260922-1" defer></script>'
 (prefix/'news.html').write_text(head+'</head><body class="inner-page news-page"><a class="skip-link" href="#main-content">'+tr('Skip to content','跳转到正文',cn)+'</a>'+header+main(cn)+footer+'</body></html>')
# Keep the homepage source compatible with the general Chinese-page generator.
i18n={}
for x in ROWS[:3]:
 for key in ['title','summary']:i18n[x[key]]=x[key+'_zh']
 i18n[day(x['published'])]=day(x['published'],True)
 i18n['Image from the original post: '+x['title']]='原始动态配图：'+x['title_zh']
for en,zh in CATS.values():i18n[en]=zh
for x in ROWS:
 for p in x['photos']:
  if p.get('caption'):i18n[p['caption']]=p['caption_zh']
(ROOT/'data/news-i18n.json').write_text(json.dumps(i18n,ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(ROWS)} bilingual news entries and 3 verified homepage highlights.')
