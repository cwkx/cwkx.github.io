# Row order controls the blog; categories group the sidebar independently.
# Run python3 data/genblog.py after editing an article. No dependencies.

from collections import Counter
from html import escape
from pathlib import Path
import re

categories = ('reflections', 'teaching', 'research')
posts = [  # Path below data/, sidebar category, sidebar label.
    ('research/gridflow', 'research', 'gridflow'),
    ('blog/zooming-out-of-bounds', 'reflections', 'zooming out of bounds'),
    ('blog/deep-learning-teaching', 'teaching', 'deep learning'),
    ('blog/multiresolution-implicit-representations', 'teaching', 'implicit representations'),
    ('blog/reinforcement-learning-teaching', 'teaching', 'reinforcement learning'),
    ('teaching/course-materials', 'teaching', 'course materials'),
    ('research/infty-diff', 'research', 'infty-diff'),
    ('research/unleashing-transformers', 'research', 'transformers'),
    ('research/protein-conformational-space', 'research', 'protein conformations'),
    ('research/gradient-origin-networks', 'research', 'gradient origin networks'),
    ('research/measuring-macular-holes', 'research', 'macular holes'),
    ('research/extracting-3d-curves', 'research', '3D curves'),
    ('research/sparse-volumetric-deformation', 'research', 'volumetric deformation'),
    ('research/feature-varying-skeletonization', 'research', 'skeletonization'),
]

root = Path(__file__).resolve().parent.parent
page = root / 'blog.html'
start = '<!--GENERATED-BLOG-->'
end = '<!--END-GENERATED-->'
text = page.read_text(encoding='utf-8')
if text.count(start) != 1 or text.count(end) != 1:
    raise ValueError('Expected one GENERATED-BLOG / END-GENERATED block')
before, rest = text.split(start)
_, after = rest.split(end)

articles = {}
ids = Counter()
for name, category, label in posts:
    if category not in categories or name in articles:
        raise ValueError(f'{name}: unknown category or duplicate entry')
    href = f'/data/{name}.html'
    source = (root / href.lstrip('/')).read_text(encoding='utf-8')
    blocks = re.findall(r'<article\b[^>]*>.*?</article>', source, re.S)
    if len(blocks) != 1:
        raise ValueError(f'{href}: expected exactly one article')
    article = blocks[0]
    titles = re.findall(r'<h1 id="([^"]+)">(.*?)</h1>', article, re.S)
    if len(titles) != 1:
        raise ValueError(f'{href}: expected one h1 title with an id')
    anchor, title = titles[0]
    ids.update(re.findall(r'\bid="([^"]+)"', article))
    article = re.sub(r'<(/?)h2\b', r'<\1h3', article)
    article = article.replace(
        f'<h1 id="{anchor}">{title}</h1>',
        f'<h2 id="{anchor}"><a href="{href}">{title}</a></h2>',
    )
    articles[name] = anchor, article

nav = ['<div id="nav">', '  <ul>', '    <li><a href="#"><b>blog</b></a></li>']
for group in categories:
    nav += [f'    <li><a href="#{group}-posts"><b>{group}</b></a>', '      <ul>']
    for name, category, label in posts:
        if category == group:
            anchor = articles[name][0]
            nav.append(f'        <li><a href="#{anchor}">{escape(label)}</a></li>')
    nav += ['      </ul>', '    </li>']
nav += ['  </ul>', '</div>', '<hr class="hidden"/>']

main = ['<div id="main">', '<h1>Blog</h1>', '<hr>']
seen = set()
for name, category, label in posts:
    anchor, article = articles[name]
    if ids[anchor] != 1:
        raise ValueError(f'{name}: duplicate article id {anchor}')
    # Research pages share headings such as "citation"; make these unique here.
    for value in re.findall(r'\bid="([^"]+)"', article):
        if ids[value] > 1:
            article = article.replace(f'id="{value}"', f'id="{anchor}-{value}"')
            article = article.replace(f'href="#{value}"', f'href="#{anchor}-{value}"')
    if category not in seen:
        main.append(f'<a id="{category}-posts"></a>')
        seen.add(category)
    main += [article, '<hr>']
main += ['<a href="#top">[return to top]</a>', '</div>']

generated = before + start + '\n' + '\n'.join(nav + main) + '\n' + end + after
if generated != text:
    page.write_text(generated, encoding='utf-8')
print(f'Generated {len(articles)} articles and sidebar in blog.html')
