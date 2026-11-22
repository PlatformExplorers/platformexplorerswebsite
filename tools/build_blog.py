"""Build the static blog. Run from anywhere: python tools/build_blog.py."""
import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path
from string import Template
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

import bleach
import markdown
import yaml

SITE = Path(__file__).resolve().parents[1]
DOMAIN = 'https://platformexplorers.com'
SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {'p','h2','h3','h4','h5','h6','pre','code','br','hr','img','table','thead','tbody','tr','th','td','del'}


def esc(value):
    return html.escape(str(value), quote=True)


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f'Duplicate metadata field: {key}')
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def text_field(data, key, context):
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{context}: {key} must contain text')
    return value.strip()


def local_image(value, site, article_dir=None):
    # A contributor can keep images beside index.md; shared portraits still work.
    if not isinstance(value, str):
        raise ValueError('Image path must contain text')
    if value.startswith('./images/') and article_dir is not None:
        path = (article_dir / value[2:]).resolve()
        allowed = (article_dir / 'images').resolve()
    elif value.startswith('/assets/blog/'):
        path = (site / value.lstrip('/')).resolve()
        allowed = (site / 'assets/blog').resolve()
    elif re.fullmatch(r'/blog/[a-z0-9]+(?:-[a-z0-9]+)*/images/[^?#]+', value):
        path = (site / value.lstrip('/')).resolve()
        allowed = (site / '/'.join(value.lstrip('/').split('/')[:3])).resolve()
    else:
        raise ValueError('Use ./images/filename inside your article folder, or /assets/blog/filename')
    if not allowed.is_relative_to(site.resolve()) or not path.is_relative_to(allowed) or not path.is_file():
        raise ValueError(f'Image not found or outside its images folder: {value}')
    if path.suffix.lower() not in {'.jpg','.jpeg','.png','.webp','.gif'}:
        raise ValueError('Blog images must be JPG, PNG, WebP or GIF')
    return '/' + path.relative_to(site.resolve()).as_posix()


def read_post(path, site):
    raw = path.read_text(encoding='utf-8-sig')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z', raw, re.S)
    if not match:
        raise ValueError(f'{path.name}: start with YAML metadata between --- lines')
    data = yaml.load(match[1], Loader=UniqueLoader)
    if not isinstance(data, dict):
        raise ValueError(f'{path.name}: metadata must be a mapping')
    for key in ('title','slug','author','authorId','description','excerpt','category','seoTitle','seoDescription'):
        data[key] = text_field(data, key, path.name)
    if not SLUG.fullmatch(data['slug']) or not SLUG.fullmatch(data['authorId']):
        raise ValueError(f'{path.name}: slug and authorId need lowercase words separated by hyphens')
    for key in ('date','lastModified'):
        try:
            data[key] = dt.date.fromisoformat(str(data[key]))
        except (KeyError, ValueError, TypeError):
            raise ValueError(f'{path.name}: {key} must be YYYY-MM-DD')
    if data['lastModified'] < data['date']:
        raise ValueError(f'{path.name}: lastModified cannot be before date')
    for key in ('draft','featured'):
        if type(data.get(key)) is not bool:
            raise ValueError(f'{path.name}: {key} must be true or false')
    if not isinstance(data.get('tags'), list) or not all(isinstance(tag,str) and tag.strip() for tag in data['tags']):
        raise ValueError(f'{path.name}: tags must be a list of text')
    article_dir = path.parent if path.parent.parent == site / 'blog' else None
    if article_dir is not None and (path.name != 'index.md' or path.parent.name != data['slug']):
        raise ValueError(f'{path}: use blog/{data["slug"]}/index.md so folder and slug match')
    if data.get('image'):
        data['image'] = local_image(data['image'], site, article_dir)
        text_field(data, 'imageAlt', path.name)
    author_path = site / '_blog/authors' / (data['authorId'] + '.yml')
    if not author_path.is_file():
        raise ValueError(f'{path.name}: add author profile _blog/authors/{data["authorId"]}.yml')
    author = yaml.load(author_path.read_text(encoding='utf-8'), Loader=UniqueLoader)
    if not isinstance(author, dict):
        raise ValueError(f'{author_path.name}: profile must be a mapping')
    for key in ('name','bio'):
        author[key] = text_field(author, key, author_path.name)
    if author['name'] != data['author']:
        raise ValueError(f'{path.name}: author must match the name in the author profile')
    if author.get('image'):
        author['image'] = local_image(author['image'], site)
    if author.get('website'):
        url = urlsplit(author['website'])
        if url.scheme != 'https' or not url.netloc:
            raise ValueError(f'{author_path.name}: website must be a full HTTPS URL')
    body = match[2].strip()
    if not body:
        raise ValueError(f'{path.name}: add the article below the metadata')
    # Sanitize after Markdown rendering so angle brackets in code remain readable.
    rendered = markdown.markdown(body, extensions=['fenced_code','tables','sane_lists'])
    rendered = bleach.clean(rendered, tags=TAGS, attributes={'a':['href','title'], 'img':['src','alt','title'], 'code':['class']}, protocols=['https','http','mailto'], strip=True)
    # Markdown images follow the same local-image contract as covers, with useful alt text.
    from html.parser import HTMLParser
    image_replacements = {}
    class ImageCheck(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'img':
                attrs = dict(attrs)
                attrs['src'] = local_image(attrs.get('src'), site, article_dir)
                if not attrs.get('alt','').strip():
                    raise ValueError(f'{path.name}: every article image needs alt text')
                image_replacements[self.get_starttag_text()] = '<img ' + ' '.join(f'{key}="{esc(value)}"' for key, value in attrs.items()) + '>'
    ImageCheck().feed(rendered)
    for original, replacement in image_replacements.items():
        rendered = rendered.replace(original, replacement)
    data.update(body=rendered, profile=author)
    return data


def write_changed(path, value):
    encoded = value.encode('utf-8')
    if not path.exists() or path.read_bytes() != encoded:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(encoded)


def build(site=SITE):
    source = site / '_blog'
    posts = []
    slugs = set()
    paths = list((source / 'posts').glob('*.md')) + list((site / 'blog').glob('*/*.md'))
    for path in sorted(paths):
        try:
            post = read_post(path, site)
        except Exception as error:
            raise ValueError(f'{path.name}: {error}') from error
        if post['slug'] in slugs:
            raise ValueError(f'Duplicate slug: {post["slug"]}')
        slugs.add(post['slug'])
        if not post['draft']:
            posts.append(post)
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)
    shell = Template((source / 'templates/page.html').read_text(encoding='utf-8'))
    article = Template((source / 'templates/article.html').read_text(encoding='utf-8'))

    def page(title, description, path, main, article_meta=''):
        return shell.substitute(title=esc(title), description=esc(description), url=DOMAIN+path, main=main, article_meta=article_meta)

    cards = []
    for post in posts:
        url = '/blog/' + post['slug'] + '/'
        image = f'<img class="post-cover" src="{esc(post["image"])}" alt="{esc(post["imageAlt"])}" loading="lazy">' if post.get('image') else ''
        profile = post['profile']
        portrait = f'<img class="author-photo" src="{esc(profile["image"])}" alt="{esc(profile["name"])}" loading="lazy">' if profile.get('image') else ''
        website = f'<a href="{esc(profile["website"])}" rel="author noopener">Find {esc(profile["name"])} online</a>' if profile.get('website') else ''
        published = post['date'].strftime('%d %B %Y').lstrip('0')
        modified = f'<span>Updated {post["lastModified"].strftime("%d %B %Y").lstrip("0")}</span>' if post['lastModified'] != post['date'] else ''
        main = article.substitute(title=esc(post['title']), category=esc(post['category']), author=esc(post['author']), date=post['date'].isoformat(), published=published, modified=modified, description=esc(post['description']), image=image, body=post['body'], tags=''.join(f'<span>{esc(tag)}</span>' for tag in post['tags']), portrait=portrait, bio=esc(profile['bio']), website=website)
        schema = {'@context':'https://schema.org', '@type':'BlogPosting', 'headline':post['title'], 'description':post['seoDescription'], 'datePublished':str(post['date']), 'dateModified':str(post['lastModified']), 'author':{'@type':'Person','name':post['author']}, 'url':DOMAIN+url}
        if post.get('image'):
            schema['image'] = DOMAIN + post['image']
        meta = (f'<meta property="og:image" content="{DOMAIN}{esc(post["image"])}"><meta property="og:image:alt" content="{esc(post["imageAlt"])}">' if post.get('image') else '')
        meta += '<meta property="og:type" content="article"><script type="application/ld+json">'+json.dumps(schema).replace('<','\\u003c')+'</script>'
        write_changed(site / url.lstrip('/') / 'index.html', page(post['seoTitle'], post['seoDescription'], url, main, meta))
        featured = '<span class="featured-label">Featured</span>' if post['featured'] else ''
        thumb = f'<img src="{esc(post["image"])}" alt="{esc(post["imageAlt"])}" loading="lazy">' if post.get('image') else ''
        cards.append(f'<article class="blog-card">{thumb}<div><p class="post-meta">{esc(post["category"])} {featured}</p><h2><a href="{url}">{esc(post["title"])}</a></h2><p>{esc(post["excerpt"])}</p><p class="post-meta">Written by {esc(post["author"])} · <time datetime="{post["date"]}">{published}</time></p></div></article>')
    # The Markdown guide is the single source for GitHub and website readers.
    guide_source = (site / 'contribution.md').read_text(encoding='utf-8')
    guide_source = guide_source.split('## Maintainer notes', 1)[0]
    guide_source = re.sub(r'\A# [^\n]+\n+', '', guide_source)
    # Python-Markdown's fenced_code expects top-level fences; preserve the
    # nested GitHub source while rendering these command examples as real blocks.
    import textwrap
    guide_source = re.sub(r'(?ms)^ {3}```[^\n]*\n.*?^ {3}```[ \t]*$', lambda match: textwrap.dedent(match[0]), guide_source)
    guide_html = markdown.markdown(guide_source, extensions=['fenced_code', 'tables', 'sane_lists', 'toc'])
    guide_html = bleach.clean(guide_html, tags=TAGS, attributes={'a':['href','title'], 'h2':['id'], 'h3':['id'], 'ol':['start'], 'code':['class']}, protocols=['https','http','mailto'], strip=True)
    def guide_link(match):
        href = html.unescape(match[1])
        if not href.startswith(('https://','http://','mailto:','#','/')):
            href = 'https://github.com/PlatformExplorers/platformexplorerswebsite/blob/main/' + href
        return 'href="' + esc(href) + '"'
    guide_html = re.sub(r'href="([^"]+)"', guide_link, guide_html)
    jumps = '<nav class="guide-jumps" aria-label="Contribution guide sections"><a href="#what-you-need">What you need</a><a href="#option-a-contribute-using-vs-code">Using VS Code</a><a href="#option-b-contribute-directly-on-github">Using GitHub</a><a href="#open-a-pull-request-both-methods">Open a pull request</a></nav>'
    guide_main = '<article class="contribution-guide wrap"><a class="blog-back" href="/blog.html">All articles</a><header class="article-heading"><h1>Contribute a blog</h1></header>' + jumps + '<div class="article-body">' + guide_html + '</div></article>'
    write_changed(site / 'contribute.html', page('Contribute a blog | Platform Explorers', 'How to contribute a blog using VS Code or GitHub: fork the repository, add your article and author profile, and open a pull request.', '/contribute.html', guide_main))

    listing = ''.join(cards)
    main = '<section class="blog-heading wrap"><p class="blog-kicker">THE COMMUNITY BLOG</p><h1>Learning, shared.</h1><p>Ideas, practical guides and experiences from the Platform Explorers community.</p><a class="blog-contribute" href="/contribute.html">Contribute a blog</a></section><section class="blog-list wrap" aria-label="Community articles">'+listing+'</section>'
    write_changed(site / 'blog.html', page('Blog | Platform Explorers', 'Practical guides, projects and career experiences from the Platform Explorers community.', '/blog.html', main))
    # Only remove files this generator owns (deleted posts or posts returned to draft).
    manifest = site / '_blog/generated.json'
    current = ['blog.html', 'contribute.html'] + [f'blog/{p["slug"]}/index.html' for p in posts]
    previous = json.loads(manifest.read_text()) if manifest.exists() else []
    for name in set(previous) - set(current):
        if re.fullmatch(r'blog/[a-z0-9-]+/index\.html', name):
            (site / name).unlink(missing_ok=True)
    write_changed(manifest, json.dumps(current, indent=2)+'\n')
    # Preserve all non-blog sitemap entries, and replace only generated blog URLs.
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    sitemap = site / 'sitemap.xml'
    tree = ET.parse(sitemap)
    root = tree.getroot()
    for entry in list(root):
        loc = entry.find(f'{{{ns}}}loc')
        if loc is not None and (loc.text in (DOMAIN+'/blog.html', DOMAIN+'/contribute.html') or (loc.text or '').startswith(DOMAIN+'/blog/')):
            root.remove(entry)
    for name in current:
        entry = ET.SubElement(root, f'{{{ns}}}url')
        ET.SubElement(entry, f'{{{ns}}}loc').text = DOMAIN + '/' + name.removesuffix('index.html')
    ET.indent(tree, space='  ')
    write_changed(sitemap, '<?xml version="1.0" encoding="utf-8"?>\n'+ET.tostring(root, encoding='unicode')+'\n')
    return len(posts)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=SITE)
    args = parser.parse_args()
    try:
        print(f'Blog built: {build(args.site.resolve())} published articles.')
    except Exception as error:
        sys.exit(f'Blog build failed: {error}')
