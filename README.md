# The Pooch Parlor Mobile Pet Spa — website prototype

A static, clickable prototype of a new site for **The Pooch Parlor Mobile Pet Spa**,
a mobile dog groomer working out of Wake Forest, NC. Built to be shown to the owner
before any commitment, then ported to WordPress and handed over.

This is **not live** and is not affiliated with the business yet. Every price, review
and photograph in it is a marked placeholder.

## Running it

```bash
./scripts/serve.py            # http://localhost:8000, opens a browser
./scripts/serve.py --port 3000
./scripts/serve.py --no-open
```

Live reload is on — save any file under `site/` and the open tab refreshes. Clean URLs
work (`/services` serves `site/services.html`), so the link structure already matches
what it will be in WordPress.

Python 3 only. No npm, no build tools, works offline apart from Google Fonts.

## Editing it

Pages are generated so the header, nav, footer and action bar are defined once:

```bash
./scripts/build.py            # regenerates all nine pages into site/
```

Edit content in `scripts/build.py`, then rebuild. The generated HTML in `site/` is
committed and standalone — the build script is a convenience, not a runtime dependency.

Styling lives in one file, `site/assets/css/main.css`, organised by section with the
design tokens at the top.

## Publishing it to GitHub Pages

The repo isn't a git repo yet, so:

```bash
git init && git add -A && git commit -m "Pooch Parlor prototype"
gh repo create PoochParlor --private --source=. --push
```

Then in **Settings → Pages**, set *Source* to **GitHub Actions**. The workflow in
`.github/workflows/pages.yml` builds and deploys on every push to `main`. It works out
the base path itself — no base for a `owner.github.io` user site, `/RepoName` for a
project site.

Note that GitHub Pages is **public even from a private repo** unless you're on
Enterprise. That is why the prototype ships with `<meta name="robots" content="noindex,
nofollow">` on every page and a disallow-all `robots.txt`: it presents as a real
business that has not agreed to it, and it must not be indexed or turn up in front of
her customers ahead of her actual site. **Remove both only when it genuinely goes
live.** Tell her the link exists before sharing it.

The form still sends nothing. On a public URL that matters more than it did locally —
anyone who finds it gets a success message that says explicitly that nothing was sent,
which is honest but not a booking. Wire up Formspree before showing it to customers.

To build for a subdirectory by hand:

```bash
./scripts/build.py --base /PoochParlor
./scripts/build.py                     # back to root-relative for local work
```

## Layout

```
scripts/serve.py         local preview server, live reload, clean URLs
scripts/build.py         page generator — shared chrome + per-page content
site/index.html          home
site/<slug>/index.html   the other pages, as directory indexes so extensionless
                         URLs work on any static host
site/404.html            GitHub Pages serves this for unknown paths
site/robots.txt          disallow-all while this is a demo
site/assets/css/main.css design system and all component styles
site/assets/js/main.js   mobile nav, ZIP checker, form handling, lightbox
site/assets/img/         brand assets derived from her van photo
docs/brand-brief.md      brand decisions, open questions, WordPress plan
```

## Before this goes anywhere near live

Read `docs/brand-brief.md`. It lists what still has to come from the owner —
real prices, real photographs, real reviews, and several factual questions that were
deliberately left unanswered rather than guessed at.
