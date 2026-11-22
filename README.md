# Platform Explorers website

The website is published at https://platformexplorers.com using GitHub Pages.

## Contribute a blog

Read [contribution.md](contribution.md) for step-by-step instructions using VS Code
or GitHub in your browser. The same guide is published at
https://platformexplorers.com/contribute.html.

Each article lives in `blog/<slug>/index.md`, with its images in an `images/`
folder beside it. Reusable author profiles are in `_blog/authors/`. Start with
the templates in `_blog/templates/`. Submit your contribution through a pull
request. Do not edit generated HTML.

## Build and maintain

The `Build blog and publish website` workflow validates pull requests. On `main`,
it builds the blog and deploys the public website with GitHub Pages. The Pages
source must be GitHub Actions. The custom domain remains platformexplorers.com.

For a manual build, install Python 3.10 or newer, then run:

```shell
python -m pip install -r requirements-blog.txt
python -m unittest discover -s tests -v
python tools/build_blog.py
```

The build generates `blog.html`, `contribute.html`, article HTML and sitemap entries.
The guide webpage comes from `contribution.md`; maintainers' notes remain in the
Markdown file only. Shared blog HTML templates are in `_blog/templates/` and
styles are in `blog.css`. The deployment artifact excludes Markdown sources,
tests and build tools. Blog dates are metadata; use `draft: true` to hide a post.

The repository root contains the website files. In the owner's local project,
these files live inside `dist/`, and `python dev.py --open` runs the live preview.
