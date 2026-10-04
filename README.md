# System Design Notes

A personal system design knowledge base for learning, revision, and building system design intuition.

I write notes in my own words while studying *System Design Interview: An Insider’s Guide* by Alex Xu and other resources. This project continuously evolves with my understanding. The initial topic files contain empty outlines for me to fill in.

[Website](https://suleymanssardogan.github.io/system-design-notes/)

## Structure

- `docs/fundamentals/` — foundational topic outlines
- `docs/designs/` — system design topic outlines
- `docs/interview-framework/` — interview preparation outlines
- `docs/vocabulary.md` — personal vocabulary
- `docs/templates/topic-template.md` — reusable writing template
- `mkdocs.yml` — theme, Markdown extensions, and sidebar navigation
- `.github/workflows/deploy.yml` — automatic GitHub Pages deployment

## Run locally

Use Python 3.12 or later. From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

On Windows, activate with `.venv\Scripts\activate` instead. Open http://127.0.0.1:8000 in your browser. Changes to Markdown files appear during local preview.

Validate and build:

```sh
mkdocs build --strict
```

The generated `site/` directory is ignored by Git.

## Write a note

Fill in an existing outline or copy `docs/templates/topic-template.md` into the appropriate section. Use short explanations in your own words, simple technical English, a personal takeaway, and sources. Add a small diagram when useful. Add new pages to `nav` in `mkdocs.yml` and link them from their section overview.

Mermaid is supported through Material’s native integration: use a fenced code block labeled `mermaid` under the Diagram heading. No additional diagram plugin is required. Standard fenced code blocks support syntax highlighting and copying.

## GitHub Pages

One-time setup: in **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**. Ensure GitHub Actions is enabled for the repository. If the first workflow ran before this setting was enabled, rerun it from the Actions tab or push another commit.

Every push to `main` installs dependencies, builds with `mkdocs build --strict`, uploads the generated site as a Pages artifact, and deploys it through GitHub’s official Pages actions. No deployment branch or manual deploy command is needed. The workflow also supports manual runs for recovery.

The site is published at https://suleymanssardogan.github.io/system-design-notes/.

## Tooling references

- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Material Mermaid configuration](https://squidfunk.github.io/mkdocs-material/reference/diagrams/)
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
