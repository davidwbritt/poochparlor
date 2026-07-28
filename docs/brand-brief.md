# The Pooch Parlor Mobile Pet Spa — brand and handover brief

Everything here was derived from two sources: the existing Wix site
(`poochplanetgroomin.wixsite.com/thepoochparlor`) and a photograph of her van.
The van won every disagreement between the two, on the principle that the van *is*
the business — it is her most visible asset and the most expensive one to change.

---

## 1. The name

Three different names are currently in use:

| Where | Name |
|---|---|
| The van | The Pooch Parlor — **Mobile Pet Spa** |
| Facebook | The Pooch Parlor Mobile Pet **Salon** |
| Wix site | The Pooch Parlor |

**This prototype standardises on "The Pooch Parlor Mobile Pet Spa"**, matching the van.
"Spa" also does more positioning work than "salon". Worth confirming with her, and
worth fixing the Facebook page name either way — three names across three surfaces
costs her search visibility and looks careless.

## 2. Tagline

**"Quality Grooming At Your Doorstep."** Already on the van, in script, and used as
the site's hero headline. It is hers, it is specific, and it beats anything invented.

## 3. Palette

Sampled directly from the van photograph. The photo was shot in shade, so the white
van body read `#CCCFD7` — everything was desaturated and blue-shifted. Colours below
are white-balance corrected against that body, then checked for contrast.

| Token | Hex | Role | Contrast on `--paper` |
|---|---|---|---|
| `--pink` | `#E2647E` | Her signature pink. Accents, rules, fills, large text | 3.17 |
| `--rose` | `#A82A4B` | Text, links, **all** button fills | 6.51 |
| `--rose-deep` | `#8A1F3C` | Button hover | — |
| `--blush` | `#FBEAEE` | Section backgrounds | 1.11 |
| `--sky` | `#7BC4E0` | The blue bone on her poodle. Secondary accent | 1.86 |
| `--teal` | `#2B6E82` | Text-safe version of the blue | 5.52 |
| `--ink` | `#1E1A1C` | Headings, dark sections | 16.54 |
| `--ink-soft` | `#4A4247` | Body copy | 9.33 |
| `--paper` | `#FCFAF8` | Page background | — |

**The one rule that matters:** her pink is *never* a button fill and never small text.
White on `#E2647E` measures **3.30:1**, which fails WCAG AA. Buttons use `--rose`
(6.78:1 with white). Keep this rule when adding anything new — a lot of her clients
are older, and pink-on-white body text would be genuinely hard for them to read.

## 4. Typography

| Role | Face | Why |
|---|---|---|
| Wordmark | **Yellowtail** | Nearest free match to the retro brush script on her van |
| Headings | **Fraunces** | Warm, slightly wonky serif — premium without being cold |
| Body | **Karla** | Highly legible, a little character, starts at 17px |

The script is used for the wordmark **only**. It is charming at six feet on a van and
illegible at 16px. Never use it for headings or body copy.

## 5. Logo

`site/assets/img/poodle-mark.svg` — her decal redrawn as clean vector art: black body,
pink poms, light-blue bone bow, plus an eye that her decal does not have. The eye was
added because without it the mark reads as ambiguous at small sizes; it is the one
deliberate departure from her artwork.

`favicon.svg` is the same mark cropped to the head, where it stays legible at 32px.

A photographic cutout of the actual decal was tried first and rejected — shot at an
angle, on a curved surface, with JPEG artefacts and reflections. Unusable as a logo.

**Her van photo is now the site's hero image**, white-balance corrected and cropped
tight on the lettering. The tight crop is deliberate: it reads as craft, where a wide
shot of a well-used van reads as an old van.

## 6. Voice

The site speaks in the **first person plural — "we"**. Talking to the site is talking to
the groomer, so third-person copy ("she reads every one and comes back to you") was
removed throughout; it read like someone describing her rather than her addressing a
customer. Contractions are used freely ("we'll", "we've") to keep it warm.

Note the one place this does *not* apply: the placeholder and open-question notes
addressed to whoever is building the site stay in the third person, so the two voices
can never be confused for one another.

Since the business is one person, **"I" would arguably be warmer and more honest than
"we"** — worth revisiting with her. It is a single pass through `scripts/build.py` to
change.

## 7. What her reviews actually say

Worth reading before writing any more copy. Three things came out of the fourteen:

**Her differentiator is not convenience — it is patience with difficult dogs.** Google's
own extracted topic is "nervous dogs". Reba's review is entirely about an anxious cocker;
Michele's says she *"takes her time when dogs are nervous"* and that she **found lumps
during a groom and sent the owner to a vet**. Every mobile groomer sells convenience.
Almost none can evidence that.

**Dogs are pleased to see her.** Karen's corgi "runs to greet her"; Barbara's two "love
her". That is unusually specific praise for a groomer and hard to fake.

**Her one negative review is about communication.** Christopher Smith: *"Cant say much.
Never got back to me."* One complaint in fourteen, and it is a response-time complaint —
which is exactly what the request form plus a reliable notification to her phone exists
to fix. This is the strongest practical argument for wiring up SMS notification rather
than relying on email alone.

The site currently leads on convenience. Leading on careful handling of nervous, elderly
and difficult dogs would match what her customers actually value, and is a stronger
position because far fewer competitors can claim it.

## 8. Design motif

One decorative device only: the **scalloped edge**, which is her pom shape abstracted
into a section divider (`.edge-scallop`, pure CSS mask). It appears between sections
and nowhere else.

The paw-print confetti scattered across her van and the Wix site was deliberately
dropped. Scattered paw prints are the single strongest signal of a cheap pet-business
template, and cutting them is most of what separates this from her current site.

---

## 9. What is still needed from her

Nothing below was guessed at. Anything uncertain is flagged in the page itself with a
`Sample content` or `Needs answering` badge, so nothing incorrect can go out under her
name by accident.

### Blocking — the site should not go live without these

- [ ] **Real prices.** Every figure is invented. Placeholder rates are plausible
      Triangle-area numbers, nothing more.
- [ ] **Real photographs.** Before/after pairs matter most — same angle, same spot,
      good light. Also worth having: the van exterior, the tub, her at work.
- [x] **Real reviews — done.** Nine quotes taken from her Google Business Profile
      (4.7 from 14 reviews), with names as the reviewer left them. Longer ones are
      shortened with an ellipsis; no wording was changed. Rating and count are shown
      on the reviews page and will need updating by hand as they change.
- [ ] **Confirm the service area.** The town and ZIP list is an educated guess based on
      Wake Forest. Her actual route, and any travel charge beyond a set distance, must
      replace it. ZIPs live in one place: `data-zips` on the ZIP-check form.
- [x] **Google Business Profile — exists**, 4.7 from 14 reviews. Still worth pushing
      review count up: 4.7 across 40 outranks 4.7 across 14 in local search.

### Factual questions left open in the FAQ

- [ ] Does she need the client's water or electricity? The van looks self-contained
      (rooftop AC, generator) but this was not assumed.
- [ ] Does she groom cats? The van says "pet spa", not "dog spa".
- [ ] How does she take payment — cash, cheque, card, app?
- [ ] What is her cancellation policy?
- [ ] Her own words about how she started and what she likes about the work. The About
      page currently paraphrases her Wix copy, which is thin. Ten minutes of her
      talking would produce something far better.

---

## 10. Booking

Built as a **request form, not a live booking calendar** — a mobile groomer's route and
drive times make hard self-service booking actively harmful, and it avoids a monthly fee.

The form collects owner contact, service address and ZIP, per-dog details (breed, size,
coat condition, age, temperament notes), service wanted, and two or three preferred
day/time windows.

The request page reserves a slot for a live scheduler so one can be dropped in later
without redesigning the page. If she ever wants real self-service booking, Square
Appointments embeds cleanly there.

**The prototype form does not send anything.** `main.js` validates it and then shows a
success message that says explicitly that nothing was sent. To make it real:

- Static hosting → point it at Formspree and delete the marked block in `main.js`
- WordPress → Fluent Forms or WPForms, and delete the handler entirely

## 11. WordPress plan

**Recommendation: a mainstream block theme plus block patterns, not a custom theme.**

Use **Kadence** or **GeneratePress**, rebuild this design as block patterns, and set the
palette and type in theme.json / global styles. Deliberate reasoning: she can edit her
own prices and photographs in the native editor, and if you become unavailable, any
WordPress person in Wake Forest can pick it up. A bespoke theme looks better in a
portfolio and is a liability on handover.

Mapping:

| Prototype | WordPress |
|---|---|
| `header()` / `footer()` in `build.py` | Template parts, or block theme header/footer patterns |
| Each entry in `PAGES` | A real Page |
| `main.css` tokens | `theme.json` palette + typography |
| `.ph` placeholders | Real images in the Media Library |
| Request form | Fluent Forms / WPForms, emailing her |
| ZIP check | Small snippet, or drop it and keep the town list |
| FAQ `<details>` | Native details block (no plugin needed) |

Also worth setting up at handover: Google Business Profile, `LocalBusiness` schema
(not yet added), a real domain, and analytics if she wants it.

## 12. Hosting

Deployable to GitHub Pages via `.github/workflows/pages.yml`. Pages are emitted as
directory indexes (`services/index.html`) so extensionless URLs work on any static host,
and `--base` handles a project site served from `/RepoName/`.

**While it is a demo it carries `noindex` on every page and a disallow-all
`robots.txt`.** It presents as a real business that has not adopted it; it must not be
indexed, and it must not appear in front of her customers ahead of her real site. Both
come off only at genuine launch — at which point the `LocalBusiness` schema in §12
should go on.

## 13. Known gaps in the prototype

- No `LocalBusiness` structured data yet — worth adding before launch for local search.
- The poodle's muzzle merges slightly into the head at the current outline weight.
  Recognisable, but a designer would redraw the head as a single path.
- Google Fonts is loaded from a CDN. Self-host if she wants to avoid the third-party
  request.
- Hours are taken from the Wix site and have not been confirmed as current.
