"""Translation quality check for Tillya (runs on GitHub, no internet needed).

Checks the built index.html and the legal pages:
  1. Every short text of the page (menus, titles, buttons, months, stones...) has a
     hand-reviewed translation in Spanish and in every language of src/i18n.
  2. Every text of the page and of privacy/terms has a hand-reviewed Spanish version.
  3. Each translation is not empty, keeps the protected pieces (↗, 316L, 925, numbers,
     the search words "wholesale jewelry" / "macrame cord") and is written in the
     right alphabet (Chinese, Japanese, Korean, Russian, Arabic, Hindi).
  4. index.html matches a fresh build of src/ (nobody edited the page by hand).
Errors make the run fail (GitHub e-mails the owner). Warnings are only listed.
Usage: python3 tools/i18n_check.py
"""
import json, os, re, subprocess, sys, shutil, tempfile
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHORT = 10**6  # every text of the page must be in every language dictionary
SCRIPTS = {'zh-CN': r'[一-鿿]', 'ja': r'[぀-ヿ一-鿿]', 'ko': r'[가-힯]',
           'ru': r'[Ѐ-ӿ]', 'ar': r'[؀-ۿ]', 'hi': r'[ऀ-ॿ]'}
PROTECTED = ['↗', '316L', '925', 'wholesale jewelry', 'macrame cord']
SAME_OK = {'Macramé', 'Guides', 'Contact', 'Peridot', 'Amethyst', 'Saphir', 'Diamant', 'Opal', 'Rubin',
           'Granat', 'Aquamarin', 'April', 'August', 'September', 'November', 'Garnet', 'Kontak', 'Promo'}
errors, warnings = [], []


def read(name):
    return open(os.path.join(ROOT, name), encoding='utf-8').read()


def json_after(text, marker):
    i = text.index(marker) + len(marker)
    return json.JSONDecoder().raw_decode(text[i:])[0]


class Texts(HTMLParser):
    """Collects the visible text the translator would see (skips scripts and translate=no)."""
    def __init__(self):
        super().__init__(); self.stack = []; self.out = []
    def handle_starttag(self, tag, attrs):
        if tag in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source'): return
        a = dict(attrs)
        skip = tag in ('script', 'style', 'noscript', 'title') or a.get('translate') == 'no' \
            or 'notranslate' in (a.get('class') or '').split() or a.get('id') == 'lang'
        self.stack.append(skip or (self.stack[-1] if self.stack else False))
    def handle_endtag(self, tag):
        if tag in ('br', 'img', 'input', 'meta', 'link', 'hr', 'source'): return
        if self.stack: self.stack.pop()
    def handle_data(self, d):
        d = d.strip()
        if d and re.search(r'[^\W\d_]', d) and not (self.stack and self.stack[-1]) and d not in self.out:
            self.out.append(d)


def texts_of(html):
    p = Texts(); p.feed(html); return p.out


# ---------- main page ----------
index = read('index.html')
FIX = json_after(index, 'const FIX=')
page = texts_of(index)
dyn = ['Hide', 'Your birthstone:', 'US size'] + re.findall(r"'([^']+)'", re.search(r'const STONES=\[(.*?)\]', index).group(1))
page += [d for d in dyn if d not in page]
langs = sorted(k for k in FIX if k != 'es')
short = [t for t in page if len(t) <= SHORT]
long_ = [t for t in page if len(t) > SHORT]

for t in page:
    if t not in FIX['es']:
        errors.append(f'es: missing Spanish for "{t}"')
rows = []
for lang in langs:
    d = FIX[lang]; miss = [t for t in short if t not in d]
    for t in miss:
        errors.append(f'{lang}: missing translation for "{t}"')
    for k, v in d.items():
        if not v.strip():
            errors.append(f'{lang}: empty translation for "{k}"'); continue
        for tok in PROTECTED:
            if tok in k and tok not in v:
                errors.append(f'{lang}: "{k}" lost "{tok}" -> "{v}"')
        for num in re.findall(r'\d+', k):
            if num not in v and lang not in ('ja', 'ko', 'zh-CN'):
                warnings.append(f'{lang}: number {num} missing in "{v}" (from "{k}")')
        if lang in SCRIPTS and re.search(r'[A-Za-z]{3}', k) and not re.search(SCRIPTS[lang], v):
            errors.append(f'{lang}: "{v}" is not written in its alphabet (from "{k}")')
        if v == k and k not in SAME_OK and lang not in SCRIPTS:
            warnings.append(f'{lang}: "{k}" is identical to English (check it)')
    rows.append(f'| {lang} | {len(short) - len(miss)}/{len(short)} |')

# ---------- legal pages (Spanish) ----------
legal = read('legal-tr.js')
LFIX = {'es': json_after(legal, 'var FIX={es:')} if 'var FIX={es:' in legal else {}
for name in ('privacy.html', 'terms.html'):
    for t in texts_of(read(name)):
        if t not in LFIX.get('es', {}):
            errors.append(f'{name} (es): missing Spanish for "{t}"')

# ---------- index.html must match src/ ----------
if os.path.exists(os.path.join(ROOT, 'src', 'build.py')):
    tmp = tempfile.mkdtemp()
    for item in ('src', 'links.json'):
        src = os.path.join(ROOT, item)
        (shutil.copytree if os.path.isdir(src) else shutil.copy)(src, os.path.join(tmp, item))
    r = subprocess.run([sys.executable, os.path.join(tmp, 'src', 'build.py')], capture_output=True, text=True)
    if r.returncode:
        errors.append('src/build.py failed: ' + (r.stderr.strip().splitlines() or ['?'])[-1])
    elif open(os.path.join(tmp, 'index.html'), encoding='utf-8').read() != index:
        errors.append('index.html is different from a fresh build of src/ (run: python3 src/build.py)')

# ---------- report ----------
report = ['## Tillya translation check', '',
          f'Hand-reviewed: {len(page)} texts in Spanish (plus the legal pages) and in {len(langs)} more languages.',
          'Any other phone language uses Google Translate automatically.', '',
          '| Language | Texts reviewed by hand |', '|---|---|'] + rows + ['']
report += ['### ❌ Errors'] + [f'- {e}' for e in errors] + [''] if errors else ['All translations OK ✅', '']
if warnings:
    report += ['### ⚠️ Warnings (review, not blocking)'] + [f'- {w}' for w in warnings[:60]]
text = '\n'.join(report)
print(text)
if os.environ.get('GITHUB_STEP_SUMMARY'):
    open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8').write(text + '\n')
sys.exit(1 if errors else 0)
