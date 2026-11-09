"""Builds index.html from src/template.html + links.json + dictionaries (src/fix_es.json, src/i18n/*.txt).
Run from anywhere:  python3 src/build.py"""
import json, html, glob, os
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
p = lambda *a: os.path.join(*a)
L = json.load(open(p(ROOT, 'links.json'), encoding='utf-8'))
def S(lid, brand, title, desc, label='Shop on'):
    off = html.escape(L[lid]['official'])
    return (f'<div class="store"><div><b>{title}</b><span>{desc}</span></div>'
            f'<a class="go" data-link="{lid}" href="{off}" target="_blank" rel="noopener sponsored">{label} <span class="notranslate">{brand}</span><em>Opens partner site ↗</em></a></div>\n')
G={
'shipping':S('planet-express','Planet Express','US address for your orders','Get a US address and ship your online purchases anywhere.','Go to')+S('shipito','Shipito','Worldwide package forwarding','US warehouse address and package forwarding worldwide.','Go to'),
'women':S('italo-women','Italojewelry','Fashion &amp; fine jewelry','Necklaces, earrings, rings and bracelets')+S('bern-women','Bernardelli','Designer jewelry from Italy','Jewels from international designer brands'),
'men':S('italo-men','Italojewelry','Jewelry for men','Rings, chains and bracelets')+S('bern-men','Bernardelli','Designer jewelry for men','Italian designer store'),
'kids':S('ae-kids','AliExpress','Kids jewelry','Small earrings, bracelets and necklaces')+S('ae-baby','AliExpress','Baby jewelry','Name bracelets and keepsakes'),
'personal':S('italo-personal','Italojewelry','Personalized jewelry','Names, initials and engravings'),
'wedding':S('italo-engage','Italojewelry','Engagement rings','Rings for your marriage proposal')+S('italo-wedding','Italojewelry','Wedding bands','Wedding rings for both partners'),
'luxury':S('luxury','The Luxury Closet','Pre-owned luxury','Jewelry and watches from luxury houses'),
'macrame':S('ae-mac-cord','AliExpress','Macramé cord','Cotton cord in many colors and sizes')+S('ae-mac-kit','AliExpress','Macramé kits','Everything you need to start')+S('ae-mac-brace','AliExpress','Macramé bracelets','Ready-made handmade bracelets')+S('dh-macrame','DHgate','Macramé at wholesale prices','Cords and pieces in larger quantities'),
'embroidery':S('ae-emb-kit','AliExpress','Embroidery kits','Embroidery hoop, threads, needles and pattern')+S('ae-emb-thread','AliExpress','Embroidery thread','Embroidery floss in many colors')+S('ae-emb-ear','AliExpress','Embroidered earrings','Handmade embroidered jewelry'),
'diy':S('ae-diy-supp','AliExpress','Jewelry-making supplies','Clasps, wire, pliers and jewelry findings')+S('ae-diy-beads','AliExpress','Jewelry beads','Glass, crystal and stone beads')+S('dh-beads','DHgate','Jewelry beads at wholesale prices','Silver and decorative beads'),
'learn':S('udemy-mac','Udemy','Macramé courses','Learn knots and projects step by step')+S('udemy-emb','Udemy','Embroidery courses','From basic stitches to full designs')+S('udemy-jew','Udemy','Jewelry-making courses','Bead jewelry, wire jewelry and more'),
'business':S('alibaba','Alibaba','Wholesale from manufacturers','Search "wholesale jewelry" or "macrame cord"'),
'deals':S('italo-deals','Italojewelry','Clearance sale','Discounted pieces while stock lasts'),
}
t = open(p(SRC, 'template.html'), encoding='utf-8').read()
FIX = {'es': json.load(open(p(SRC, 'fix_es.json'), encoding='utf-8'))}
K = open(p(SRC, 'i18n', 'keys.txt'), encoding='utf-8').read().splitlines()
for fn in sorted(glob.glob(p(SRC, 'i18n', '*.txt'))):
    code = os.path.basename(fn)[:-4]
    if code == 'keys': continue
    V = open(fn, encoding='utf-8').read().splitlines()
    assert len(V) == len(K), f"{code}.txt has {len(V)} lines, keys.txt has {len(K)}"
    FIX[code] = dict(zip(K, V))
t = t.replace('@@FIX@@', json.dumps(FIX, ensure_ascii=False, separators=(',', ':')))
t = t.replace('@@ICON@@', open(p(SRC, 'icon.inc'), encoding='utf-8').read()).replace('@@LINKS@@', json.dumps(L, separators=(',', ':')))
for k, v in G.items(): t = t.replace('@@' + k + '@@', v)
assert '@@' not in t
open(p(ROOT, 'index.html'), 'w', encoding='utf-8').write(t)
print('index.html built:', ', '.join(sorted(FIX)))
