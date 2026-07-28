#!/usr/bin/env python3
"""Assemble the static site into ./site.

Header, nav, footer and the mobile action bar are defined once here and shared
by every page — hand-duplicating them across nine files is where markup drifts.
The output is plain HTML with no runtime dependency on this script, so the
prototype opens straight from disk.

    ./scripts/build.py

When this moves to WordPress, the shared pieces below map onto template parts
(header.php / footer.php, or block theme patterns) and PAGES becomes real pages.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"

# --- real business facts. Everything else on the site is placeholder. --------
BIZ = {
    "name": "The Pooch Parlor",
    "sub": "Mobile Pet Spa",
    "full": "The Pooch Parlor Mobile Pet Spa",
    "tagline": "Quality Grooming At Your Doorstep",
    "phone_display": "(919) 418-4773",
    "phone_href": "+19194184773",
    "email": "poochplanetgrooming@yahoo.com",
    "base": "Wake Forest, North Carolina",
    "years": "nearly 20 years",
}

ZIPS = "27587,27571,27596,27525,27549,27522,27508,27614,27616"

# Short labels — the full page titles live in PAGES. Long nav labels wrapped
# and made the header ragged at desktop widths.
NAV = [
    ("index", "Home"),
    ("services", "Services"),
    ("gallery", "Gallery"),
    ("reviews", "Reviews"),
    ("service-area", "Service Area"),
    ("about", "About"),
    ("faq", "FAQ"),
]

# --- tiny inline icon set ----------------------------------------------------
def icon(name, cls=""):
    p = {
        "phone": '<path d="M3 5.5A2.5 2.5 0 0 1 5.5 3h1A1.5 1.5 0 0 1 8 4.2l.5 2.2a1.5 1.5 0 0 1-.6 1.5l-.9.7a10 10 0 0 0 4.4 4.4l.7-.9a1.5 1.5 0 0 1 1.5-.6l2.2.5A1.5 1.5 0 0 1 17 13.5v1A2.5 2.5 0 0 1 14.5 17h-.3C8.6 16.6 3.4 11.4 3 5.8V5.5Z"/>',
        "calendar": '<path d="M6 2v2M14 2v2M3 7h14M4.5 4h11A1.5 1.5 0 0 1 17 5.5v10A1.5 1.5 0 0 1 15.5 17h-11A1.5 1.5 0 0 1 3 15.5v-10A1.5 1.5 0 0 1 4.5 4Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
        "badge": '<path d="M10 2.5 12 6l4 .6-2.8 2.8.6 4L10 11.6 6.2 13.4l.6-4L4 6.6 8 6l2-3.5Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
        "van": '<path d="M2 13V7.5A1.5 1.5 0 0 1 3.5 6H11l3 3h2.5A1.5 1.5 0 0 1 18 10.5V13h-2M6 13H2m14 0h-2m-8 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0Zm6 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
        "heart": '<path d="M10 16s-6-3.8-6-7.6A3.4 3.4 0 0 1 10 6.4a3.4 3.4 0 0 1 6 2C16 12.2 10 16 10 16Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
        "pin": '<path d="M10 17s5-4.6 5-8.4A5 5 0 0 0 5 8.6C5 12.4 10 17 10 17Zm0-6.6a1.9 1.9 0 1 0 0-3.8 1.9 1.9 0 0 0 0 3.8Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
        "star": '<path d="M10 1.8l2.5 5 5.5.8-4 3.9.9 5.5-4.9-2.6-4.9 2.6.9-5.5-4-3.9 5.5-.8 2.5-5Z"/>',
        "clock": '<path d="M10 5v5l3 2M17 10a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    }[name]
    classes = ("ico " + cls).strip()
    return f'<svg class="{classes}" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">{p}</svg>'


def stars(n=5):
    return f'<div class="stars" aria-label="{n} out of 5 stars">' + (icon("star") * n) + "</div>"


def ph(label, note="", mod="", lightbox=False):
    """A deliberately obvious photo placeholder."""
    lb = ' data-lightbox' if lightbox else ""
    small = f"<small>{note}</small>" if note else ""
    return (f'<div class="ph {mod}"{lb}><span>{label}</span>{small}</div>')


SAMPLE = '<span class="is-sample">Sample content</span>'


# --- shared chrome -----------------------------------------------------------
CURRENT = ' aria-current="page"'


def nav_link(slug, label, current):
    href = "/" if slug == "index" else f"/{slug}"
    mark = CURRENT if slug == current else ""
    return f'<a href="{href}"{mark}>{label}</a>'


def header(current):
    links = "".join(nav_link(s, l, current) for s, l in NAV)
    req_mark = CURRENT if current == "request" else ""
    mobile = links + f'<a href="/request"{req_mark}>Request an Appointment</a>'
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="/">
      <img src="/assets/img/poodle-mark.svg" alt="" width="42" height="38">
      <span class="brand__text">
        <span class="brand__name">The Pooch Parlor</span>
        <span class="brand__sub">Mobile Pet Spa</span>
      </span>
    </a>
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="header-actions">
      <a class="header-phone" href="tel:{BIZ['phone_href']}">{icon('phone')}{BIZ['phone_display']}</a>
      <a class="btn btn--primary" href="/request">Request an Appointment</a>
    </div>
    <div class="nav-toggle">
      <button type="button" data-nav-toggle aria-expanded="false" aria-controls="mobile-nav">Menu</button>
    </div>
  </div>
  <nav class="mobile-nav wrap" id="mobile-nav" data-nav-panel data-open="false" aria-label="Main">{mobile}</nav>
</header>"""


def footer():
    nav_links = "".join(f'<li><a href="/{s if s != "index" else ""}">{l}</a></li>' for s, l in NAV)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="site-footer__grid">
      <div>
        <a class="brand" href="/" style="margin-bottom:1rem">
          <img src="/assets/img/poodle-mark.svg" alt="" width="42" height="38">
          <span class="brand__text">
            <span class="brand__name">The Pooch Parlor</span>
            <span class="brand__sub">Mobile Pet Spa</span>
          </span>
        </a>
        <p style="max-width:26ch">{BIZ['tagline']} — serving {BIZ['base']} and the surrounding towns.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>{nav_links}<li><a href="/request">Request an Appointment</a></li></ul>
      </div>
      <div>
        <h4>Get in touch</h4>
        <ul>
          <li><a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></li>
          <li><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
          <li><a href="https://www.facebook.com/ThePoochParlorMobilePetSalon/">Facebook</a></li>
        </ul>
      </div>
      <div>
        <h4>Hours</h4>
        <dl class="hours">
          <div><dt>Mon – Fri</dt><dd>10am – 6pm</dd></div>
          <div><dt>Saturday</dt><dd>10am – 6pm</dd></div>
          <div><dt>Sunday</dt><dd>Closed</dd></div>
        </dl>
      </div>
    </div>
    <div class="site-footer__bottom">
      <span>&copy; 2026 {BIZ['full']}. All rights reserved.</span>
      <span>Demonstration site — not yet live.</span>
    </div>
  </div>
</footer>
<nav class="action-bar" aria-label="Quick actions">
  <a href="tel:{BIZ['phone_href']}">{icon('phone')}Call</a>
  <a href="/request">{icon('calendar')}Request</a>
</nav>
<script src="/assets/js/main.js" defer></script>"""


def layout(slug, title, description, body):
    full_title = f"{title} | {BIZ['full']}" if slug != "index" else f"{BIZ['full']} | {BIZ['tagline']} in Wake Forest, NC"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<!-- This is a demonstration site for a business that has not adopted it. Keeping it
     out of search stops it competing with the owner's real site and stops customers
     finding a booking form that goes nowhere. Remove when it genuinely goes live. -->
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="/assets/css/main.css">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
</head>
<body>
{header(slug)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""


# --- reusable page blocks ----------------------------------------------------
def page_head(title, lede, crumb):
    return f"""<section class="page-head">
  <div class="wrap">
    <p class="breadcrumb"><a href="/">Home</a> &rsaquo; {crumb}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""


def cta_band(heading="Ready to book the van?", body=None):
    body = body or (
        f"Tell us about your dog and when suits you. We confirm every appointment "
        f"personally, usually within a day."
    )
    return f"""<section class="section cta">
  <div class="wrap">
    <img class="cta__mark" src="/assets/img/poodle-mark.svg" alt="" width="72" height="65">
    <h2>{heading}</h2>
    <p class="lede">{body}</p>
    <div class="btn-row">
      <a class="btn btn--onink btn--lg" href="/request">Request an Appointment</a>
      <a class="btn btn--ghost btn--lg" style="border-color:rgba(252,250,248,.4);color:#FCFAF8" href="tel:{BIZ['phone_href']}">{icon('phone')}{BIZ['phone_display']}</a>
    </div>
  </div>
</section>"""


PLACEHOLDER_NOTICE = f"""<div class="notice" style="max-width:52rem">
  <strong>Placeholder content.</strong> Prices, photographs and reviews on this
  demonstration site are examples only, so the layout can be reviewed before real
  details are collected. Nothing here reflects {BIZ['full']}'s actual rates.
</div>"""


# --- pages -------------------------------------------------------------------
def home():
    return f"""<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <p class="hero__wordmark reveal">The Pooch Parlor</p>
      <p class="hero__sub reveal">Mobile Pet Spa</p>
      <h1 class="reveal">{BIZ['tagline']}</h1>
      <p class="lede reveal">A fully equipped grooming salon that drives to your door in
        Wake Forest. One dog at a time, no cages, no waiting room — just a calm bath
        and a good haircut without the car ride.</p>
      <div class="btn-row reveal" style="margin-top:1.75rem">
        <a class="btn btn--primary btn--lg" href="/request">Request an Appointment</a>
        <a class="btn btn--ghost btn--lg" href="/services">See Services &amp; Pricing</a>
      </div>
    </div>
    <div class="hero__media">
      <picture>
        <source srcset="/assets/img/van-branding.webp" type="image/webp">
        <img src="/assets/img/van-branding.jpg" width="1800" height="664"
             alt="The Pooch Parlor Mobile Pet Spa van, lettered with a pink poodle and the words Quality Grooming At Your Doorstep.">
      </picture>
    </div>
  </div>
</section>

<section class="trust">
  <div class="wrap trust__grid">
    <div class="trust__item">{icon('badge')}<span><b>{BIZ['years'].title()}</b>Grooming experience behind every cut</span></div>
    <div class="trust__item">{icon('heart')}<span><b>Cage-free, always</b>Your dog is the only one in the van</span></div>
    <div class="trust__item">{icon('van')}<span><b>Self-contained van</b>Parks at your kerb and gets to work</span></div>
    <div class="trust__item">{icon('pin')}<span><b>Wake Forest &amp; nearby</b>Rolesville, Youngsville, Franklinton and more</span></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">What we do</p>
      <h2>Three services, done properly</h2>
      <p class="lede">Every appointment is one-to-one, so the time goes into your dog
        rather than into managing a room full of them.</p>
    </div>
    <div class="grid grid--3">
      <article class="card">
        <h3>Full Groom</h3>
        <span class="card__price">from $75 {SAMPLE}</span>
        <p>Bath, blow-dry, full haircut to breed standard or your preference, nails,
          ears, and a sanitary trim. The works.</p>
      </article>
      <article class="card">
        <h3>Bath &amp; Tidy</h3>
        <span class="card__price">from $55 {SAMPLE}</span>
        <p>Bath, blow-dry, thorough brush-out, nails and ears, with a light tidy of
          face, feet and sanitary areas. No full haircut.</p>
      </article>
      <article class="card">
        <h3>Nail Trim</h3>
        <span class="card__price">from $20 {SAMPLE}</span>
        <p>A quick standalone visit for nails and a pad tidy — handy between grooms,
          and often the easiest first visit for a nervous dog.</p>
      </article>
    </div>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn--ghost" href="/services">Full pricing by size and coat</a>
    </div>
  </div>
</section>

<section class="section section--blush edge-scallop">
  <div class="wrap">
    <div class="section-head section-head--center">
      <p class="eyebrow eyebrow--center">How it works</p>
      <h2>Three steps, no car ride</h2>
    </div>
    <div class="steps">
      <div class="step">
        <h3>Ask for a time</h3>
        <p>Send a request with your dog's breed, size and coat, plus a couple of days
          that suit you. Or just call — we prefer the phone for first-timers.</p>
      </div>
      <div class="step">
        <h3>We confirm</h3>
        <p>You'll get a text or call back to lock in a slot, usually within a day, along
          with a firm quote once we know what we're working with.</p>
      </div>
      <div class="step">
        <h3>The van comes to you</h3>
        <p>We park outside, bring your dog in, and stay with them start to
          finish. Most grooms take one to two hours.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Our work</p>
      <h2>Before and after</h2>
      <p class="lede">The clearest argument for a groomer is the dog that walks back
        out. These slots are waiting on real photographs.</p>
    </div>
    <div class="gallery">
      {"".join(f'<figure>{ph("Before / After", "Photo needed", "ph--square", lightbox=True)}<figcaption>Placeholder {i} — awaiting a real photo</figcaption></figure>' for i in range(1, 5))}
    </div>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn--ghost" href="/gallery">See the full gallery</a>
    </div>
  </div>
</section>

<section class="section section--warm">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Reviews</p>
      <h2>What our clients say {SAMPLE}</h2>
      <p class="lede">The quotes below are written examples showing how real reviews
        will sit on the page. They are not from actual customers.</p>
    </div>
    <div class="grid grid--3">
      <figure class="quote">
        {stars()}
        <blockquote>“Example review text goes here — this is placeholder copy standing in
          for a real quote once real ones are collected from Google or Facebook.”</blockquote>
        <figcaption><b>Sample name</b>Wake Forest</figcaption>
      </figure>
      <figure class="quote">
        {stars()}
        <blockquote>“A second example, a little shorter, to show how quotes of differing
          length sit side by side without breaking the row.”</blockquote>
        <figcaption><b>Sample name</b>Rolesville</figcaption>
      </figure>
      <figure class="quote">
        {stars()}
        <blockquote>“A third example, longer than the others, demonstrating that a
          generous review still fits the card without crowding its neighbours or
          pushing the layout around.”</blockquote>
        <figcaption><b>Sample name</b>Youngsville</figcaption>
      </figure>
    </div>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn--ghost" href="/reviews">Read more reviews</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Where we go</p>
      <h2>Wake Forest and the towns around it</h2>
      <p>Our route covers Wake Forest and the surrounding communities. If you are just
        outside it, ask anyway — it often depends on the day.</p>
      <form class="field" data-zip-check data-zips="{ZIPS}" style="margin-top:1.5rem;max-width:22rem">
        <label for="zip-home">Check your ZIP code</label>
        <div style="display:flex;gap:.6rem">
          <input id="zip-home" name="zip" type="text" inputmode="numeric" pattern="\\d{{5}}"
                 maxlength="5" placeholder="27587" autocomplete="postal-code">
          <button class="btn btn--primary" type="submit">Check</button>
        </div>
        <p class="form-status" data-zip-result role="status"></p>
      </form>
    </div>
    <div>
      <ul class="towns">
        <li>Wake Forest <em>27587</em></li>
        <li>Rolesville <em>27571</em></li>
        <li>Youngsville <em>27596</em></li>
        <li>Franklinton <em>27525</em></li>
        <li>Louisburg <em>27549</em></li>
        <li>Creedmoor <em>27522</em></li>
        <li>Bunn <em>27508</em></li>
        <li>North Raleigh <em>27614</em></li>
        <li>Falls River / Wakefield <em>27616</em></li>
      </ul>
      <p class="card__note" style="margin-top:1rem">Service area is a placeholder list
        and needs confirming against her actual route.</p>
    </div>
  </div>
</section>

{cta_band()}"""


def services():
    def row(size, weight, full, bath):
        return f"<tr><th scope='row'>{size}<br><span class='card__note'>{weight}</span></th><td>{full}</td><td>{bath}</td></tr>"

    return f"""{page_head("Services &amp; Pricing",
        "Full grooms, baths and nail trims, priced by size and coat. Every quote is confirmed before we start.",
        "Services &amp; Pricing")}

<section class="section section--tight">
  <div class="wrap">{PLACEHOLDER_NOTICE}</div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grid grid--3">
      <article class="card">
        <h3>Full Groom</h3>
        <span class="card__price">from $75 {SAMPLE}</span>
        <p>Bath with a shampoo suited to the coat, blow-dry, full haircut, nail trim,
          ear clean, and sanitary trim. Around 1–2 hours for most dogs.</p>
      </article>
      <article class="card">
        <h3>Bath &amp; Tidy</h3>
        <span class="card__price">from $55 {SAMPLE}</span>
        <p>Bath, blow-dry and a full brush-out, plus nails, ears and a light tidy of the
          face, feet and sanitary areas. Best for short coats and between grooms.</p>
      </article>
      <article class="card">
        <h3>Nail Trim</h3>
        <span class="card__price">from $20 {SAMPLE}</span>
        <p>Nails clipped and smoothed, pads tidied. A short standalone visit, and often
          the gentlest introduction for an anxious dog.</p>
      </article>
    </div>
  </div>
</section>

<section class="section section--blush edge-scallop">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Pricing</p>
      <h2>By size and coat {SAMPLE}</h2>
      <p class="lede">Coat condition matters more than weight. Every figure below is a
        starting point — we confirm the exact price before any work begins.</p>
    </div>
    <div class="table-scroll">
      <table class="prices">
        <caption>Starting prices, placeholder figures pending her real rates</caption>
        <thead>
          <tr><th scope="col">Dog size</th><th scope="col">Full Groom</th><th scope="col">Bath &amp; Tidy</th></tr>
        </thead>
        <tbody>
          {row("Small", "up to 20 lb", "$75", "$55")}
          {row("Medium", "21 – 45 lb", "$90", "$65")}
          {row("Large", "46 – 75 lb", "$110", "$80")}
          {row("Extra large", "76 lb and up", "$135+", "$95+")}
        </tbody>
      </table>
    </div>

    <div class="table-scroll" style="margin-top:2.5rem">
      <table class="prices">
        <caption>Add-ons {SAMPLE}</caption>
        <thead><tr><th scope="col">Extra</th><th scope="col">Price</th><th scope="col">Notes</th></tr></thead>
        <tbody>
          <tr><th scope="row">De-shedding treatment</th><td>$15 – $30</td><td>By coat and size</td></tr>
          <tr><th scope="row">De-matting</th><td>$15 / 15 min</td><td>Charged only when needed, agreed first</td></tr>
          <tr><th scope="row">Medicated or flea shampoo</th><td>$10</td><td>Bring your own if prescribed</td></tr>
          <tr><th scope="row">Teeth brushing</th><td>$10</td><td>Freshen-up, not a dental clean</td></tr>
          <tr><th scope="row">Extra time for senior dogs</th><td>No charge</td><td>Older dogs set their own pace</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow prose">
    <h2>How quoting works</h2>
    <p>A price quoted over the phone is an estimate. Coat length, matting, shedding
      and how a dog behaves in the van all change how long a groom takes, so we
      confirm the final figure when we see your dog — before we start, never after.</p>
    <h3>Matting</h3>
    <p>Where a coat is badly matted, brushing it out can be painful and slow. We will
      always talk to you first and, if clipping short is kinder, we'll say so. Dog's
      comfort comes ahead of a particular haircut.</p>
    <h3>Cancellations</h3>
    <p>Life happens — let us know as early as you can so the slot can go to someone
      else. <span class="is-sample">Sample content</span> Her actual cancellation terms
      need adding here.</p>
  </div>
</section>

{cta_band("Not sure which service you need?", "Describe your dog and we'll tell you honestly which one fits — and what it will cost.")}"""


def gallery():
    cards = []
    labels = [
        ("Doodle, full groom", "Before / after pair"),
        ("Shih Tzu, face tidy", "Before / after pair"),
        ("Golden, de-shed", "Before / after pair"),
        ("Schnauzer, full groom", "Before / after pair"),
        ("Terrier, hand-strip", "Before / after pair"),
        ("Pomeranian, tidy", "Before / after pair"),
    ]
    for name, note in labels:
        cards.append(
            f'<figure><div class="ba" data-lightbox>'
            f'{ph("Before", "Photo needed", "ph--tall")}{ph("After", "Photo needed", "ph--tall")}'
            f'</div><figcaption>{name} — placeholder</figcaption></figure>'
        )
    singles = "".join(
        f'<figure>{ph("Van / at work", "Photo needed", "ph--square", lightbox=True)}'
        f'<figcaption>Placeholder — the van, the setup, work in progress</figcaption></figure>'
        for _ in range(4)
    )
    return f"""{page_head("Gallery",
        "Before and after photographs of dogs groomed in the van, plus a look inside the setup itself.",
        "Gallery")}

<section class="section section--tight">
  <div class="wrap">
    <div class="notice" style="max-width:52rem"><strong>Every image here is a placeholder.</strong> These slots
      show how her photographs will be laid out. Before-and-after pairs do the most
      work, so those are worth gathering first — ideally same angle, same spot, good light.</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Before &amp; after</p><h2>The difference a groom makes</h2></div>
    <div class="gallery">{"".join(cards)}</div>
  </div>
</section>

<section class="section section--blush edge-scallop">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">The van</p><h2>Where the work happens</h2>
      <p class="lede">Clients like seeing inside before they book — the tub, the table,
        and how calm it is with one dog in there.</p></div>
    <div class="gallery">{singles}</div>
  </div>
</section>

{cta_band()}"""


def reviews():
    def q(text, name, town, n=5):
        return f"""<figure class="quote">{stars(n)}
        <blockquote>“{text}”</blockquote>
        <figcaption><b>{name}</b>{town}</figcaption></figure>"""

    samples = [
        ("Example review copy sits here. Once her Google and Facebook reviews are collected, real quotes replace this text one for one.", "Sample name", "Wake Forest"),
        ("A shorter example, to show how a brief review looks beside a longer one.", "Sample name", "Rolesville"),
        ("A longer example that runs to several lines, demonstrating that a generous review still sits comfortably in its card without crowding the ones next to it or unbalancing the row.", "Sample name", "Youngsville"),
        ("Another example of placeholder review text, standing in until the real thing is available.", "Sample name", "Franklinton"),
        ("Example copy about a nervous dog and a patient groomer — the kind of review that persuades people, once a real one is in hand.", "Sample name", "North Raleigh"),
        ("A final example, kept short.", "Sample name", "Creedmoor"),
    ]
    return f"""{page_head("Reviews",
        "What clients say about grooming with The Pooch Parlor Mobile Pet Spa.",
        "Reviews")}

<section class="section section--tight">
  <div class="wrap">
    <div class="notice" style="max-width:52rem"><strong>These reviews are written examples, not real customers.</strong>
      They are placeholders showing how genuine reviews will look. Real quotes should be
      pulled from her Google Business Profile and Facebook page, with names as the
      reviewer left them.</div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grid grid--3">{"".join(q(*s) for s in samples)}</div>
  </div>
</section>

<section class="section section--blush edge-scallop">
  <div class="wrap wrap--narrow" style="text-align:center">
    <h2>Groomed with us before?</h2>
    <p class="lede" style="margin-inline:auto">A review is the single most useful thing a
      happy client can do for a small business. It takes two minutes.</p>
    <div class="btn-row" style="justify-content:center;margin-top:1.75rem">
      <a class="btn btn--primary" href="https://www.facebook.com/ThePoochParlorMobilePetSalon/">Review on Facebook</a>
      <a class="btn btn--ghost" href="#">Review on Google <span class="is-sample">Link needed</span></a>
    </div>
  </div>
</section>

{cta_band()}"""


def service_area():
    towns = [
        ("Wake Forest", "27587"), ("Rolesville", "27571"), ("Youngsville", "27596"),
        ("Franklinton", "27525"), ("Louisburg", "27549"), ("Creedmoor", "27522"),
        ("Bunn", "27508"), ("North Raleigh", "27614"), ("Falls River / Wakefield", "27616"),
    ]
    return f"""{page_head("Service Area",
        "The Pooch Parlor Mobile Pet Spa covers Wake Forest and the surrounding towns in north Wake and Franklin counties.",
        "Service Area")}

<section class="section">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Covered towns</p>
      <h2>Wake Forest and out from there</h2>
      <p>Our van works a regular route around Wake Forest, reaching into north Wake and
        southern Franklin county. Because we travel to you, the day of the week often
        decides how far out we can get.</p>
      <p><strong>Just outside the list? Ask anyway.</strong> A short hop beyond the usual
        route is frequently workable, particularly if you can be flexible on the day.</p>
      <form class="field" data-zip-check data-zips="{ZIPS}" style="margin-top:1.75rem;max-width:22rem">
        <label for="zip-area">Check your ZIP code</label>
        <div style="display:flex;gap:.6rem">
          <input id="zip-area" name="zip" type="text" inputmode="numeric" pattern="\\d{{5}}"
                 maxlength="5" placeholder="27587" autocomplete="postal-code">
          <button class="btn btn--primary" type="submit">Check</button>
        </div>
        <p class="form-status" data-zip-result role="status"></p>
      </form>
    </div>
    <div>
      <ul class="towns">{"".join(f"<li>{t} <em>{z}</em></li>" for t, z in towns)}</ul>
      <div class="notice" style="margin-top:1.5rem"><strong>Needs confirming.</strong>
        This town and ZIP list is an educated guess based on Wake Forest. Her real route,
        and any travel charge beyond a certain distance, should replace it.</div>
    </div>
  </div>
</section>

<section class="section section--blush edge-scallop">
  <div class="wrap">
    <div class="section-head section-head--center">
      <p class="eyebrow eyebrow--center">Getting parked</p>
      <h2>What we need at your kerb</h2>
    </div>
    <div class="grid grid--3">
      <article class="card"><h3>A parking space</h3>
        <p>Room for a high-top van near your door — a driveway is ideal, a legal kerb
          space is fine. Low branches are the usual obstacle.</p></article>
      <article class="card"><h3>Nothing from your house</h3>
        <p>The van carries its own water and power. <span class="is-sample">Confirm</span>
          — worth checking whether she ever needs an outside tap or outlet.</p></article>
      <article class="card"><h3>Your dog, and you nearby</h3>
        <p>Hand your dog over and get on with your day. Staying home is not required,
          though first-timers often prefer to.</p></article>
    </div>
  </div>
</section>

{cta_band("Think you're in range?", "Send a request with your address and we'll confirm whether we can reach you.")}"""


def about():
    return f"""{page_head("About",
        f"{BIZ['years'].capitalize()} of grooming experience, in a self-contained van that comes to your door in Wake Forest.",
        "About")}

<section class="section">
  <div class="wrap split split--center">
    <div class="prose">
      <p class="eyebrow">Our story</p>
      <h2>{BIZ['years'].capitalize()} of dogs</h2>
      <p>We've been grooming for {BIZ['years']}, and somewhere in that time worked out
        that the hardest part of the job was never the haircut. It was the waiting room —
        the barking, the crates, the car journey, the hours away from home.</p>
      <p>So we moved the salon into a van. Now there is one dog in it at a time. No cages,
        nothing to wait for, no other dogs to worry about. Just your dog, one groomer,
        and however long it takes to do the job properly.</p>
      <p><span class="is-sample">Sample content</span> This section is written from what
        the current website says. Her own words about how she started, and what she likes
        about the work, would be far better — and worth ten minutes of her time.</p>
    </div>
    <div>
      <picture>
        <source srcset="/assets/img/van-hero.webp" type="image/webp">
        <img src="/assets/img/van-hero.jpg" width="2200" height="1080"
             style="border-radius:10px;box-shadow:var(--shadow-md)"
             alt="The Pooch Parlor Mobile Pet Spa van parked on a residential street.">
      </picture>
      <p class="card__note" style="margin-top:.75rem">Our van, which doubles as the
        business's best advertising.</p>
    </div>
  </div>
</section>

<section class="section section--blush edge-scallop">
  <div class="wrap">
    <div class="section-head section-head--center">
      <p class="eyebrow eyebrow--center">How we work</p>
      <h2>Why one dog at a time matters</h2>
    </div>
    <div class="grid grid--3">
      <article class="card"><h3>No cages</h3>
        <p>Nothing to be shut into. Your dog is out, on the table or in the tub, from
          arrival to finish.</p></article>
      <article class="card"><h3>No other dogs</h3>
        <p>Reactive, elderly and anxious dogs do far better without a room full of
          strangers barking at them.</p></article>
      <article class="card"><h3>No waiting</h3>
        <p>Drop-off is your front door and pick-up is an hour or two later. No half-day
          in a salon.</p></article>
    </div>
  </div>
</section>

{cta_band()}"""


def faq():
    items = [
        ("Do you need my water or electricity?",
         "The van is self-contained and carries its own water and power. "
         "<span class='is-sample'>Confirm</span> — worth checking with her whether an "
         "outside tap or outlet is ever needed in hot or cold weather."),
        ("How long does a groom take?",
         "Most full grooms take one to two hours. A bath and tidy is quicker; a thick, "
         "long or matted coat takes longer. Because we work on one dog at a time, "
         "your dog is not waiting around for any of it."),
        ("Where does the van park?",
         "Anywhere legal and close to your door. A driveway is ideal. We need headroom "
         "for a high-top van, so low branches are the thing to watch for."),
        ("Do I need to be home?",
         "Not necessarily, as long as we can collect and return your dog. First-time "
         "clients usually prefer to be there, which is welcome."),
        ("My dog is anxious. Is mobile better?",
         "Usually, yes. No car journey, no unfamiliar building, no other dogs, and one "
         "person handling them throughout. For a very nervous dog, a standalone nail "
         "trim first is a gentle way to start."),
        ("Can you groom a senior dog?",
         "Yes, at their pace, with breaks as needed. Tell us about arthritis, "
         "deafness, sight loss, heart conditions or anything else on the request form."),
        ("What if my dog's coat is matted?",
         "We'll look and talk to you before starting. Brushing out heavy matting "
         "hurts, so where clipping short is the kinder option we'll say so and "
         "explain why. Comfort comes before a particular haircut."),
        ("Do you groom cats?",
         "<span class='is-sample'>Needs answering.</span> The van says pet spa rather "
         "than dog spa, so this is worth confirming either way."),
        ("How do I pay, and do you take cards?",
         "<span class='is-sample'>Needs answering.</span> Cash, cheque, card or an app — "
         "her actual arrangement should go here."),
        ("What is your cancellation policy?",
         "<span class='is-sample'>Needs answering.</span> Let us know as early as you "
         "can so the slot can be reused — the exact terms still need adding here."),
    ]
    body = "".join(
        f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in items
    )
    return f"""{page_head("Frequently Asked Questions",
        "Parking, timing, anxious dogs, matted coats and what mobile grooming actually involves.",
        "FAQ")}

<section class="section">
  <div class="wrap wrap--narrow">
    <div class="notice" style="margin-bottom:2rem"><strong>Some answers still need her input.</strong>
      Anything marked below is a genuine open question rather than a guess, so nothing
      incorrect goes out under her name.</div>
    <div class="faq">{body}</div>
  </div>
</section>

{cta_band("Still have a question?", "Call us. For anything specific to your dog, a two-minute conversation beats a form.")}"""


def request():
    def dog_fields(n, required=False):
        r = ' required' if required else ""
        star = ' <span class="req">*</span>' if required else ""
        opt = "" if required else " (optional)"
        return f"""<fieldset class="fieldset">
      <legend>Dog {n}{opt}</legend>
      <div class="field-row">
        <div class="field"><label for="dog{n}-name">Name{star}</label>
          <input id="dog{n}-name" name="dog_name" type="text"{r}></div>
        <div class="field"><label for="dog{n}-breed">Breed or mix{star}</label>
          <input id="dog{n}-breed" name="dog_breed" type="text"{r}></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="dog{n}-size">Rough weight{star}</label>
          <select id="dog{n}-size" name="dog_size"{r}>
            <option value="">Choose…</option>
            <option>Up to 20 lb</option><option>21 – 45 lb</option>
            <option>46 – 75 lb</option><option>76 lb and up</option>
          </select></div>
        <div class="field"><label for="dog{n}-age">Age</label>
          <input id="dog{n}-age" name="dog_age" type="text" placeholder="e.g. 7 years"></div>
        <div class="field"><label for="dog{n}-coat">Coat condition</label>
          <select id="dog{n}-coat" name="dog_coat">
            <option value="">Choose…</option>
            <option>Short and easy</option><option>Long but brushed out</option>
            <option>Some tangles</option><option>Matted in places</option>
            <option>Not sure</option>
          </select></div>
      </div>
      <div class="field"><label for="dog{n}-service">Service wanted{star}</label>
        <select id="dog{n}-service" name="dog_service"{r}>
          <option value="">Choose…</option>
          <option>Full Groom</option><option>Bath &amp; Tidy</option>
          <option>Nail Trim only</option><option>Not sure — please advise</option>
        </select></div>
      <div class="field"><label for="dog{n}-notes">Anything we should know
          <span class="hint">Anxiety, arthritis, deafness, sore spots, dislikes having
            feet or ears touched, bite history — all genuinely useful.</span></label>
        <textarea id="dog{n}-notes" name="dog_notes" rows="3"></textarea></div>
    </fieldset>"""

    return f"""{page_head("Request an Appointment",
        "Tell us about your dog and when suits you. We confirm every appointment personally.",
        "Request an Appointment")}

<section class="section">
  <div class="wrap split split--wide-first">
    <form class="form" data-request-form novalidate>
      <div class="notice"><strong>This is a request, not a booking.</strong> We read every
        one and come back to you — usually within a day — to confirm a time and a firm
        price. Nothing is locked in until we do.</div>

      <fieldset class="fieldset">
        <legend>You</legend>
        <div class="field-row">
          <div class="field"><label for="name">Your name <span class="req">*</span></label>
            <input id="name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="phone">Mobile number <span class="req">*</span>
              <span class="hint">We'll text you back on this.</span></label>
            <input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
        </div>
        <div class="field"><label for="email">Email</label>
          <input id="email" name="email" type="email" autocomplete="email"></div>
        <div class="field"><label for="address">Service address <span class="req">*</span>
            <span class="hint">Where the van will park.</span></label>
          <input id="address" name="address" type="text" autocomplete="street-address" required></div>
        <div class="field-row">
          <div class="field"><label for="city">Town <span class="req">*</span></label>
            <input id="city" name="city" type="text" autocomplete="address-level2" required></div>
          <div class="field"><label for="zipc">ZIP <span class="req">*</span></label>
            <input id="zipc" name="zip" type="text" inputmode="numeric" pattern="\\d{{5}}"
                   maxlength="5" autocomplete="postal-code" required></div>
        </div>
        <div class="field"><label for="parking">Parking notes</label>
          <input id="parking" name="parking" type="text"
                 placeholder="Driveway, kerb only, low branches, gated community code…"></div>
      </fieldset>

      {dog_fields(1, required=True)}
      {dog_fields(2)}

      <fieldset class="fieldset">
        <legend>When suits you</legend>
        <p class="card__note" style="margin-bottom:.5rem">Give us two or three options —
          we work a route, so flexibility gets you seen sooner.</p>
        <div class="field-row">
          <div class="field"><label for="pref1">First choice <span class="req">*</span></label>
            <input id="pref1" name="pref1" type="date" required></div>
          <div class="field"><label for="pref2">Second choice</label>
            <input id="pref2" name="pref2" type="date"></div>
          <div class="field"><label for="pref3">Third choice</label>
            <input id="pref3" name="pref3" type="date"></div>
        </div>
        <div class="field"><label>Time of day that works</label>
          <div class="checks">
            <label class="check"><input type="checkbox" name="window" value="morning"> Morning, 10am – 12pm</label>
            <label class="check"><input type="checkbox" name="window" value="midday"> Midday, 12pm – 3pm</label>
            <label class="check"><input type="checkbox" name="window" value="afternoon"> Afternoon, 3pm – 6pm</label>
            <label class="check"><input type="checkbox" name="window" value="any"> Any time we have free</label>
          </div></div>
      </fieldset>

      <fieldset class="fieldset">
        <legend>Anything else</legend>
        <div class="field"><label for="first">Have you used us before?</label>
          <select id="first" name="first_time">
            <option value="">Choose…</option>
            <option>No — first time</option><option>Yes — returning client</option>
          </select></div>
        <div class="field"><label for="heard">How did you hear about us?</label>
          <input id="heard" name="heard" type="text" placeholder="Saw the van, a friend, Facebook…"></div>
        <div class="field"><label for="notes">Anything else we should know</label>
          <textarea id="notes" name="notes" rows="3"></textarea></div>
      </fieldset>

      <p class="form-status" data-form-status role="status" aria-live="polite"></p>
      <div class="btn-row">
        <button class="btn btn--primary btn--lg" type="submit">Send Request</button>
        <a class="btn btn--ghost btn--lg" href="tel:{BIZ['phone_href']}">{icon('phone')}Rather call?</a>
      </div>
      <p class="card__note">We read these between appointments, so a reply may
        take until the end of the day. For anything urgent, ring us.</p>
    </form>

    <aside>
      <div class="card" style="margin-bottom:1.25rem">
        <h3>Prefer the phone?</h3>
        <p>For a first appointment, or a dog with complications, we would honestly rather
          talk to you.</p>
        <p><a class="btn btn--primary btn--block" href="tel:{BIZ['phone_href']}" style="margin-top:.75rem">{icon('phone')}{BIZ['phone_display']}</a></p>
        <dl class="hours" style="margin-top:1.25rem">
          <div><dt>Mon – Fri</dt><dd>10am – 6pm</dd></div>
          <div><dt>Saturday</dt><dd>10am – 6pm</dd></div>
          <div><dt>Sunday</dt><dd>Closed</dd></div>
        </dl>
      </div>
      <div class="card">
        <h3>What happens next</h3>
        <ol class="prose" style="padding-left:1.1rem;font-size:var(--t--1)">
          <li>We read your request between appointments.</li>
          <li>We text or ring to confirm a time and a firm price.</li>
          <li>The van arrives; we take your dog and get to work.</li>
          <li>One to two hours later, a clean dog comes back to your door.</li>
        </ol>
      </div>
      <div class="notice" style="margin-top:1.25rem"><strong>Live scheduler goes here.</strong>
        This section is built so a real booking calendar can drop straight in later
        without redesigning the page.</div>
    </aside>
  </div>
</section>"""


def not_found():
    return f"""<section class="section" style="text-align:center">
  <div class="wrap wrap--narrow">
    <img src="/assets/img/poodle-mark.svg" alt="" width="120" height="108" style="margin:0 auto 1.5rem">
    <h1>That page has wandered off</h1>
    <p class="lede" style="margin-inline:auto">The link may be old, or it may be our
      mistake. Either way, here is the way back.</p>
    <div class="btn-row" style="justify-content:center;margin-top:2rem">
      <a class="btn btn--primary btn--lg" href="/">Back to the start</a>
      <a class="btn btn--ghost btn--lg" href="tel:{BIZ['phone_href']}">{icon('phone')}{BIZ['phone_display']}</a>
    </div>
  </div>
</section>"""


PAGES = [
    ("index", "Home", "Mobile dog grooming in Wake Forest, NC. A fully equipped salon van comes to your door — cage-free, one dog at a time, nearly 20 years' experience.", home),
    ("services", "Services &amp; Pricing", "Full grooms, baths and nail trims priced by size and coat, with every quote confirmed before work starts.", services),
    ("gallery", "Gallery", "Before and after photographs of dogs groomed in the van, plus a look at the setup.", gallery),
    ("reviews", "Reviews", "What clients say about mobile grooming with The Pooch Parlor Mobile Pet Spa.", reviews),
    ("service-area", "Service Area", "Wake Forest, Rolesville, Youngsville, Franklinton, Louisburg, Creedmoor, Bunn and north Raleigh.", service_area),
    ("about", "About", "Nearly 20 years of grooming, in a self-contained van that comes to your door.", about),
    ("faq", "FAQ", "Parking, timing, anxious dogs, matted coats and what mobile grooming involves.", faq),
    ("request", "Request an Appointment", "Tell us about your dog and when suits you. We confirm every appointment personally.", request),
    ("404", "Page not found", "That page could not be found.", not_found),
]


ROBOTS = """# Demonstration site for a business that has not adopted it. Keeping it out of
# search stops it competing with the owner's real site. Delete when it goes live.
User-agent: *
Disallow: /
"""


def apply_base(html, base):
    """Prefix root-absolute URLs with a base path.

    A GitHub Pages project site is served from /RepoName/, where "/assets/..."
    would resolve against the domain root and 404. Left empty for local serving
    and for user sites or custom domains, which do serve from the root.
    """
    if not base:
        return html
    base = "/" + base.strip("/")
    for attr in ("href", "src", "srcset"):
        html = html.replace(f'{attr}="/', f'{attr}="{base}/')
    # the root link becomes "/base/" rather than "/base//"
    return html.replace(f'href="{base}//"', f'href="{base}/"')


def main():
    import argparse

    ap = argparse.ArgumentParser(description="Build the Pooch Parlor prototype.")
    ap.add_argument("--base", default="",
                    help='path prefix for a subdirectory deploy, e.g. "/PoochParlor". '
                         'Leave empty for local serving, user sites and custom domains.')
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    for slug, title, desc, fn in PAGES:
        html = apply_base(layout(slug, title, desc, fn()), args.base)
        # Directory indexes, so extensionless URLs work on any static host rather
        # than relying on a particular server's .html fallback. 404 stays at the
        # root because that is where GitHub Pages looks for it.
        if slug in ("index", "404"):
            path = OUT / f"{slug}.html"
        else:
            path = OUT / slug / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        written.append((str(path.relative_to(OUT)), len(html)))

    (OUT / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")  # GitHub Pages: skip Jekyll

    width = max(len(n) for n, _ in written)
    print(f"built {len(written)} pages into {OUT}" + (f"  (base: {args.base})" if args.base else ""))
    for name, size in written:
        print(f"  {name:<{width}}  {size/1024:5.1f} kB")


if __name__ == "__main__":
    main()
