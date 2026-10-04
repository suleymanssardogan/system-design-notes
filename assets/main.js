const root = document.body.dataset.root;
const theme = document.querySelector('#theme');
theme.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem('theme', next); } catch (_) {}
});
const menu = document.querySelector('#menu');
menu.addEventListener('click', () => {
  const open = document.querySelector('#navigation').classList.toggle('open');
  menu.setAttribute('aria-expanded', String(open));
});
const dialog = document.querySelector('#search-dialog');
const input = document.querySelector('#search-input');
const results = document.querySelector('#search-results');
let index;
async function search() {
  results.replaceChildren();
  try {
    index ??= await fetch(root + 'search.json').then(r => { if (!r.ok) throw Error(); return r.json(); });
    const query = input.value.trim().toLowerCase();
    const hits = index.filter(p => !query || (p.title + ' ' + p.text).toLowerCase().includes(query)).slice(0, 15);
    for (const page of hits) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = root + page.url; a.textContent = page.title;
      li.append(a); results.append(li);
    }
    if (!hits.length) results.textContent = 'No matching notes.';
  } catch (_) { results.textContent = 'Search could not load. Please try again.'; }
}
function openSearch() { dialog.showModal(); input.focus(); search(); }
document.querySelector('#search-open').addEventListener('click', openSearch);
document.querySelector('#search-close').addEventListener('click', () => dialog.close());
input.addEventListener('input', search);
document.addEventListener('keydown', e => {
  if (e.key === '/' && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName) && !dialog.open) { e.preventDefault(); openSearch(); }
});
// Load Mermaid only when the author adds a Mermaid code fence.
const diagrams = document.querySelectorAll('code.language-mermaid');
if (diagrams.length) {
  import('https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs').then(async ({default: mermaid}) => {
    for (const code of diagrams) { const div = document.createElement('div'); div.className = 'mermaid'; div.textContent = code.textContent; code.parentElement.replaceWith(div); }
    mermaid.initialize({startOnLoad: false, securityLevel: 'strict', theme: document.documentElement.dataset.theme === 'dark' ? 'dark' : 'default'});
    await mermaid.run({querySelector: '.mermaid'});
  }).catch(() => {});
}
