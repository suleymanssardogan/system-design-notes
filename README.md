# System Design Notes

A personal system design knowledge base for learning, revision, and building system design intuition. I write English notes in my own words while studying *System Design Interview: An Insider’s Guide* by Alex Xu and other resources. The project continuously evolves. Topic pages begin as empty outlines.

[Website](https://suleymanssardogan.github.io/system-design-notes/)

## Structure

- `docs/fundamentals/` — 8 topic outlines
- `docs/designs/` — 12 topic outlines
- `docs/interview-framework/` — interview preparation outlines
- `docs/vocabulary.md` — personal vocabulary
- `docs/templates/topic-template.md` — reusable writing template
- `build.py` — small Markdown-to-HTML builder; validates Markdown links
- `assets/` — custom CSS and JavaScript for navigation, search, themes, and optional Mermaid
- `.github/workflows/deploy.yml` — automatic GitHub Pages deployment

Each topic has its own page. The site uses custom HTML/CSS, with no frontend framework or MkDocs. Dark mode is the default; the theme toggle remembers your preference.

## Run locally

Use Python 3.12 or later, from the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python build.py
python -m http.server 8000 --directory site
```

Open http://127.0.0.1:8000. On Windows activate with `.venv\Scripts\activate`. After editing Markdown, rerun `python build.py` and refresh the browser. Generated `site/` files are ignored by Git.

## Write a note

Fill in an outline or copy `docs/templates/topic-template.md` into a section. Write short explanations in your own words, use simple technical English, include one personal takeaway, and cite sources. New Markdown files in the three topic directories are automatically added to navigation. Link them from the section overview if desired.

Use standard fenced code blocks. A fence labeled `mermaid` renders as a diagram; Mermaid is loaded from jsDelivr only on pages containing diagrams, so those pages need an internet connection to render them. Source code remains readable if the diagram runtime cannot load.

## Deployment

GitHub Pages is configured with **GitHub Actions** as its source. Every push to `main` installs the single Markdown dependency, builds the site, uploads the generated artifact, and deploys through the official Pages actions. No manual deploy command is required.

Design direction inspired by [Selman Ay’s FDE page](https://selmanmoon.github.io/fde/): dark background, large typography, red accents, and numbered sections. All study content remains my own.
