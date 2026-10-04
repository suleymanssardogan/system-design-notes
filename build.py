"""Build the static site from personal Markdown notes. Run: python build.py."""
from pathlib import Path
import html
import json
import os
import re
import shutil
import markdown

ROOT = Path(__file__).resolve().parent
DOCS, SITE = ROOT / 'docs', ROOT / 'site'
SECTIONS = [('fundamentals', 'Fundamentals'), ('designs', 'System Designs'), ('interview-framework', 'Interview Framework')]

def route(path):
    rel = path.relative_to(DOCS)
    return rel.parent.as_posix() + '/' if rel.name == 'index.md' and rel.parent != Path('.') else ('' if rel.name == 'index.md' else rel.with_suffix('').as_posix() + '/')

def title(path):
    return next(line[2:] for line in path.read_text().splitlines() if line.startswith('# '))

pages = sorted(DOCS.rglob('*.md'))
known = {p.resolve() for p in pages}
if SITE.exists():
    shutil.rmtree(SITE)
SITE.mkdir()
shutil.copytree(ROOT / 'assets', SITE / 'assets')
search = []
for page in pages:
    dest = SITE / route(page)
    dest.mkdir(parents=True, exist_ok=True)
    base = os.path.relpath(SITE, dest).replace(os.sep, '/') + '/'
    def link(p):
        return base + route(p)
    name = 'System Design Notes' if page == DOCS / 'index.md' else title(page)
    source = page.read_text()
    # Resolve and validate Markdown links before generating directory URLs.
    def rewrite(match):
        label, target = match.groups()
        if '://' in target or target.startswith(('#', 'mailto:')):
            return match.group(0)
        address, sep, anchor = target.partition('#')
        candidate = (page.parent / address).resolve()
        if candidate not in known:
            raise ValueError(f'{page}: missing local link {target}')
        return f'[{label}]({link(candidate)}{sep}{anchor})'
    source = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', rewrite, source)
    md = markdown.Markdown(extensions=['toc', 'fenced_code', 'tables', 'footnotes', 'md_in_html'], extension_configs={'toc': {'permalink': False}})
    content = md.convert(source)
    nav = f'<a class="nav-home" href="{base}">Overview</a>'
    for directory, label in SECTIONS:
        nav += f'<details open><summary>{label}</summary>'
        for item in [DOCS / directory / 'index.md'] + sorted(p for p in (DOCS / directory).glob('*.md') if p.name != 'index.md'):
            active = ' aria-current="page"' if item == page else ''
            nav += f'<a href="{link(item)}"{active}>{html.escape("Overview" if item.name == "index.md" else title(item))}</a>'
        nav += '</details>'
    for item in [DOCS / 'vocabulary.md', DOCS / 'templates/topic-template.md']:
        nav += f'<a href="{link(item)}">{html.escape("Writing Template" if item.name == "topic-template.md" else title(item))}</a>'
    home = page == DOCS / 'index.md'
    if home:
        rows = [('fundamentals/index.md','Fundamentals','08 topic outlines'),('designs/index.md','System Designs','12 topic outlines'),('interview-framework/index.md','Interview Framework','01 topic outline'),('vocabulary.md','Vocabulary','Terms in my own words'),('templates/topic-template.md','Writing Template','A reusable outline for new notes')]
        content = content.replace('<h1 id="about-these-notes">About these notes</h1>', '<h2 id="about-these-notes">About these notes</h2>')
        content = '<div class="cover"><p class="eyebrow">Suleyman Sardogan / Personal knowledge base</p><h1>System Design<span>.</span><br>Notes</h1><p class="subtitle">Learning. Revision. Intuition<span>.</span></p></div><h2 id="contents">Contents</h2><ol class="collection">' + ''.join(f'<li><a href="{link(DOCS / p)}">{t}</a><small>{s}</small></li>' for p,t,s in rows) + '</ol><section class="about">' + content + '</section>'
    toc = '' if home else f'<aside class="on-page"><p class="eyebrow">On this page</p>{md.toc}</aside>'
    output = f'''<!doctype html>
<html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Personal system design knowledge base by Suleyman Sardogan. Notes written in my own words."><title>{html.escape(name)} · System Design Notes</title><link rel="stylesheet" href="{base}assets/style.css"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('theme')||'dark'}}catch(e){{}}</script><script defer src="{base}assets/main.js"></script></head>
<body data-root="{base}"><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="{base}">SD<span>.</span> NOTES</a><div class="tools"><button id="menu" aria-expanded="false" aria-controls="navigation">Menu</button><button id="search-open">Search <kbd>/</kbd></button><button id="theme" aria-label="Switch color theme">Light / Dark</button><a href="https://github.com/suleymanssardogan/system-design-notes">GitHub ↗</a></div></header><div class="layout"><nav id="navigation" aria-label="Topics">{nav}</nav><main id="main" class="{'home' if home else 'note'}">{content}<footer>Suleyman Sardogan <span>System Design Notes · A work in progress</span></footer></main>{toc}</div><dialog id="search-dialog"><div class="search-heading"><label for="search-input">Search notes</label><button id="search-close" aria-label="Close search">Close ×</button></div><input id="search-input" type="search" placeholder="Find a topic or phrase…" autocomplete="off"><ul id="search-results" aria-live="polite"></ul></dialog></body></html>'''
    (dest / 'index.html').write_text(output)
    search.append({'title': name, 'url': route(page), 'text': re.sub('<[^>]+>', ' ', content)})
(SITE / 'search.json').write_text(json.dumps(search))
(SITE / '.nojekyll').touch()
print(f'Built {len(pages)} pages in site/. All Markdown links validated.')
