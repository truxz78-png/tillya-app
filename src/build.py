"""Builds index.html from src/template.html + links.json + dictionaries (src/fix_es.json, src/i18n/*.txt).
Run from anywhere:  python3 src/build.py"""
import json, html, glob, os
SRC = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(SRC)
p = lambda *a: os.path.join(*a)
L = json.load(open(p(ROOT, 'links.json'), encoding='utf-8'))
def S(lid, brand, title, desc, label='Shop on', cls=''):
    off = html.escape(L[lid]['official'])
    return (f'<div class="store{(" "+cls) if cls else ""}"><div><b>{title}</b><span>{desc}</span></div>'
            f'<a class="go" data-link="{lid}" href="{off}" target="_blank" rel="noopener sponsored">{label} <span class="notranslate">{brand}</span><em>Opens partner site ↗</em></a></div>\n')
G={
'shipping':S('planet-express','Planet Express','US address for your orders','Get a US address and ship your online purchases anywhere.','Go to')+S('shipito','Shipito','Worldwide package forwarding','US warehouse address and package forwarding worldwide.','Go to'),
'women':S('italo-women','Italojewelry','Fashion &amp; fine jewelry','Necklaces, earrings, rings and bracelets')+S('bern-women','Bernardelli','Designer jewelry from Italy','Jewels from international designer brands')+S('tlc-women','The Luxury Closet','Luxury designer fine jewelry','New and pre-owned pieces from the top luxury brands')+S('tatacliq-jew','Tata CLiQ','Jewelry from Indian brands','Gold, diamond, silver and fashion jewelry. Delivers within India only.',cls='india-only')+S('palmonas','Palmonas','Demi-fine jewelry from India','Gold-plated and silver everyday jewelry. Delivers within India only.',cls='india-only')+S('giva','GIVA','925 silver jewelry from India','Everyday silver and gold-plated jewelry. Delivers within India only.',cls='india-only')+S('bluestone','BlueStone','Gold and diamond jewelry from India','Rings, earrings and engagement jewelry. Delivers within India only.',cls='india-only'),
'womenfashion':S('miravia-women','Miravia','Fashion jewelry in Spain','Earrings, necklaces and bracelets with fast local delivery. Spain and Portugal only.',cls='iberia-only')+S('answear-women','Answear','Fashion and accessories in Ukraine','Jewelry, bags and accessories from European brands. Ukraine only.',cls='ukraine-only')+S('shein-women','SHEIN','Trendy fashion jewelry','Earrings, necklaces, bracelets and jewelry sets in the latest styles')+S('ae-women','AliExpress','Fashion jewelry at low prices','Thousands of necklaces, earrings, rings and bracelets for women')+S('temu-women','Temu','Low-cost jewelry and gift sets','Jewelry sets, watches and earrings for women at very low prices')+S('dh-women','DHgate','Wholesale-priced jewelry for women','Necklaces, earrings and rings from global sellers at factory prices'),
'men':S('italo-men','Italojewelry','Jewelry for men','Rings, chains and bracelets')+S('bern-men','Bernardelli','Designer jewelry for men','Italian designer store'),
'menfashion':S('shein-men','SHEIN','Trendy jewelry for men','Chains, rings, bracelets and pendants in the latest styles')+S('ae-men','AliExpress','Men’s jewelry at low prices','Steel chains, bracelets and pendants from global sellers')+S('dh-men','DHgate','Men’s jewelry at wholesale prices','Rings, chains and bracelets at factory prices'),
'kids':S('ae-kids','AliExpress','Kids jewelry','Small earrings, bracelets and necklaces')+S('ae-baby','AliExpress','Baby jewelry','Name bracelets and keepsakes')+S('shein-kids','SHEIN','Jewelry sets for kids','Cute necklaces, bracelets and earrings for girls and boys'),
'personal':S('italo-personal','Italojewelry','Personalized jewelry','Names, initials and engravings')+S('ae-personal','AliExpress','Name necklaces at low prices','Necklaces, bracelets and rings with your name or initials')+S('shein-personal','SHEIN','Trendy custom name jewelry','Name and initial necklaces in the latest styles')+S('dh-personal','DHgate','Custom name jewelry at wholesale prices','Name necklaces and engraved pieces at factory prices'),
'wedding':S('italo-engage','Italojewelry','Engagement rings','Rings for your marriage proposal')+S('italo-wedding','Italojewelry','Wedding bands','Wedding rings for both partners'),
'luxury':S('luxury','The Luxury Closet','Pre-owned luxury','Jewelry and watches from luxury houses'),
'macrame':S('ae-mac-cord','AliExpress','Macramé cord','Cotton cord in many colors and sizes')+S('ae-mac-kit','AliExpress','Macramé kits','Everything you need to start')+S('ae-mac-brace','AliExpress','Macramé bracelets','Ready-made handmade bracelets')+S('dh-macrame','DHgate','Macramé at wholesale prices','Cords and pieces in larger quantities'),
'embroidery':S('ae-emb-kit','AliExpress','Embroidery kits','Embroidery hoop, threads, needles and pattern')+S('ae-emb-thread','AliExpress','Embroidery thread','Embroidery floss in many colors')+S('ae-emb-ear','AliExpress','Embroidered earrings','Handmade embroidered jewelry'),
'diy':S('ae-diy-supp','AliExpress','Jewelry-making supplies','Clasps, wire, pliers and jewelry findings')+S('ae-diy-beads','AliExpress','Jewelry beads','Glass, crystal and stone beads')+S('dh-beads','DHgate','Jewelry beads at wholesale prices','Silver and decorative beads'),
'learn':S('udemy-mac','Udemy','Macramé courses','Learn knots and projects step by step','Browse on')+S('udemy-emb','Udemy','Embroidery courses','From basic stitches to full designs','Browse on')+S('udemy-jew','Udemy','Jewelry-making courses','Bead jewelry, wire jewelry and more','Browse on'),
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
