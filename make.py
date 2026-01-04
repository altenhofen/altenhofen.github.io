#!/usr/bin/env python3

# heavily inspired by https://github.com/brilee/modern-descartes-v2/blob/master/make.py

from collections import defaultdict, namedtuple
import atexit
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import subprocess
import feedgenerator
import datetime

BLOG_URL="altenhofen.github.io"
BLOG_NAME="Augusto Altenhofen's personal page"

OUT_DIR="./compiled"
ARTICLE_DIR="./articles"
STATIC_DIR="./static"
TEMPLATE_DIR="./templates"
CUSTOM_PAGE_DIR="./custom"


ARTICLE_URI="blog"

ALLOWED_EXTENSIONS = ('.md', '.txt', '.html')

PAGES = (
    '404.html'
    'index.html'
)

JINJA_ENV = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml']))

Article = namedtuple('article', ['slug', 'title', 'date', 'content', 'tags'])

def get_article(article_path):
    article_shortname = os.path.splitext(os.path.basename(article_path))[0]
    with open(article_path, 'r') as f:
        article_longname = f.readline().rstrip('\n')
        year, month, day = f.readline().rstrip('\n').split('/')
        tags = list(filter(bool, f.readline().rstrip('\n').split(',')))
        article_date = datetime.date(year=int(year), month=int(month),
            day=int(day))
        article_content = f.read()
    result = subprocess.run(
        "pandoc -f markdown -t html --mathjax --shift-heading-level-by=1",
        stdout=subprocess.PIPE,
        input=article_content.encode('utf8'),
        shell=True)
    article_content = result.stdout.decode('utf8')
    return Article(slug=article_shortname, title=article_longname,
                 date=article_date, content=article_content, tags=tags)

def render_html(template_name, **context):
    default_context = {"ARTICLE_URI": ARTICLE_URI }
    default_context.update(**context)
    template = JINJA_ENV.get_template(template_name)
    compiled = template.render(**default_context)
    return compiled

def compile_page(template_name: str, output_fn: str, **context):
    compiled = render_html(template_name, **context);
    output_path = os.path.join(OUT_DIR, output_fn)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(compiled)

def compile_article(article_path) -> list[Article]:
    try:
        article = get_article(article_path)
        compile_page('article_post.html',
            '{}/{}/index.html'.format(ARTICLE_URI, article.slug), article=article)
        return [article]
    except Exception as e:
        print('Failed to process {}'.format(article_path))
        print(type(e), e)
    return []

def compile_custom_pages():
    for dirpath, _, filenames in os.walk(CUSTOM_PAGE_DIR):
        for filename in filenames:
            fn = os.path.splitext(filename)[0]
            ar = get_article(os.path.join(dirpath, filename))
            compile_page('custom.html', os.path.join("{}.html".format(fn)), article=ar)

# ik this is bad, but its ok. the whole code is a mess
def get_custom_pages() -> list[Article]:
    pages = []
    for dirpath, _, filenames in os.walk(CUSTOM_PAGE_DIR):
        for filename in filenames:
            fn = os.path.splitext(filename)[0]
            ar = get_article(os.path.join(dirpath, filename))
            # hacky hack
            ar = Article(slug=fn, title=ar.title,
                 date=ar.date, content=ar.content, tags=[])
            pages.append(ar) 

    return pages

def copy_static():
    subprocess.run('cp -r -p {static} {outdir}/{static}'.format(static=STATIC_DIR, outdir=OUT_DIR), shell=True)

def compile_articles() -> list[Article]:
    print("Processing articles...")
    all_articles = []
    for dirpath, _, filenames in os.walk(ARTICLE_DIR):
        for filename in filenames:
            all_articles.extend(compile_article(os.path.join(dirpath, filename)))

    print("compiled {} articles".format(len(all_articles)))
    return all_articles

def make_rss(compiled_articles: list[Article]):
    feed = feedgenerator.Atom1Feed(
        title="Augusto Altenhofen",
        link=os.path.join(BLOG_URL, ARTICLE_URI),
        description="survival notes")

    pages = []
    pages.extend(get_custom_pages())
    pages.extend(compiled_articles[:10])

    pages = sorted(pages, key=lambda x: x.date, reverse=True)

    for article in pages:
        if article.slug == "index": 
            continue
        feed.add_item(
            title=article.title,
            link=os.path.join(BLOG_URL, ARTICLE_URI, article.slug),
            description=render_html('rss_item.txt', article=article),
            pubdate=article.date)


    with open(os.path.join(OUT_DIR, ARTICLE_URI, 'rss.xml'), 'w') as f:
        feed.write(f, 'utf-8')
def make_all():
    subprocess.run('rm -rf {}'.format(OUT_DIR), shell=True)
    os.makedirs(os.path.join(OUT_DIR, ARTICLE_URI), exist_ok=True)
    copy_static()
    # compile_page('index.html', 'index.html') # its a custom page now
    compile_page('404.html', '404.html')
    compile_custom_pages()
    all_articles = compile_articles()
    articles_sorted = sorted(all_articles, key=lambda e: e.date, reverse=True)
    articles_by_tag = defaultdict(list)
    for article in articles_sorted:
        for tag in article.tags:
            if "_" in tag:
                print("WARNING: tag {} in {} should use a space, not underscore".format(tag, article.title))
            articles_by_tag[tag].append(article)
    compile_page('article_index.html', '{}/index.html'.format(ARTICLE_URI),
        articles_sorted=articles_sorted, tags=articles_by_tag)
    for tag, articles_with_tag in articles_by_tag.items():
        compile_page('article_tag.html', 'tags/{}/index.html'.format(tag.replace(' ', '_')),
            tag=tag, articles_with_tag=articles_with_tag)
    make_rss(articles_sorted)

def main():
    make_all() 
    subprocess.run('python -m http.server 8000 --directory {}'.format(OUT_DIR), shell=True)


if __name__ == "__main__":
     main()
