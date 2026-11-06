# UNTITLED — Design Thesis & Master Prompt
Events and Ticketing Engine · COMP 3540 Part 2 · UI only (no DB, PHP or backend) · web application, general events

---

## 1. Design thesis: "Quiet Stage"

Untitled treats every screen like a gallery wall in front of a stage curtain. The interface is calm, white-to-pale-grey, Swiss in its grid, and almost silent in its type. All emotion is delegated to one thing: a single art panel per page, made from ribbed (reeded) glass gradients, dot-matrix spheres, halftone/dither and film grain. The UI never competes with the art, and the art never explains the UI.

**What the 16 references share (measured):**
- Canvas `#DEDEDE`–`#E2E2E2`, cards `#FFFFFF`, ink `#0D0F05`. Chrome stays neutral; colour lives only inside art panels and tiny state accents.
- Split layout for auth: form left (white card, generous radius ~24px), art right (full-bleed reeded gradient or halftone).
- Accents: magenta `#E23693`, coral `#E46564`, copper `#D09472`, ember orange `#DC7336` on midnight `#0F1207`/`#2B2025`.
- Type: grotesk sans (Inter / Inter Display), mono for metadata (Geist Mono / DM Mono), very large light-weight display lines, tiny uppercase labels, pill tags and pill nav.
- Layout: bento grids, date-cards, tier cards with pill tags, sidebar + stat tiles for dashboards, seat map with summary panel and hold timer.
- Texture: grain on every gradient, never flat vector fills; ribbed glass with chromatic fringing; dither only in black/white.

**Rules**
1. One art panel per page, max. UI around it is white.
2. Seat and ticket states are always text + colour (accessibility rule from the proposal).
3. Text inside art is mono, small, and sparse. No marketing sentences.
4. General events only: concerts, sport, theatre, conferences, festivals. No venue-type lock-in, no planes/trains/hotels/cinema.
5. Web, not mobile: art is landscape (3:2, 16:10) or wide panel (4:5 for auth halves).

## 2. Reference library and how I refer to it

Folder: `Illustrative designs/` — each file is `UNT-REF-<CODE>-<nn>_<slug>`.

| Code | Folder | Use it for |
|---|---|---|
| AUTH-01…04 | 01_Auth | Login, sign up, reset: split layout, halftone / dot-grid / reeded / peach art |
| LIST-01…02 | 02_Event-Listing | Discover, calendar list, date cards |
| CARD-01…03 | 03_Cards-and-Editorial | Ticket tiers, image cards, press columns |
| HERO-01…02, TYPE-01 | 04_Hero-and-Type | Landing hero, pill nav, mono display type |
| SEAT-01 | 05_Seat-Selection | Seat map, summary, timer |
| DASH-01 | 06_Dashboard | Organiser + admin sidebar, stat tiles, chart |
| PROOF-01 | 07_Social-Proof | Testimonial bento |
| ART-01 | 08_Art-Backgrounds | Midnight/orange reeded wallpaper |

When prompting, write: `use UNT-REF-AUTH-03 for panel style` and I will open that file by name from the folder (or the numbered working copy) before generating.

## 3. Page set (17)

| # | Page | Group | Art direction (ref) |
|---|---|---|---|
| P01 | Landing / Home | Public | Ember reeded + stage beams (HERO-01, ART-01) |
| P02 | Login | Auth | Reeded gradient (AUTH-03) |
| P03 | Sign up | Auth | Peach gradient (AUTH-04) |
| P04 | Password reset | Auth | Dot grid pink (AUTH-02) |
| P05 | Discover events | Customer | Calendar dots (LIST-01) |
| P06 | Event details | Customer | Arena halftone (AUTH-01, HERO-01) |
| P07 | Seat selection | Customer | Seat map (SEAT-01) |
| P08 | Checkout | Customer | Ticket stub + summary |
| P09 | Order confirmation | Customer | Ticket stack |
| P10 | My tickets | Customer | Ticket wallet |
| P11 | Profile | Customer | Dot sphere (AUTH-02) |
| P12 | Create event | Organiser | Mesh gradient, form steps |
| P13 | Custom ticket types | Organiser | Tier cards (CARD-01) |
| P14 | Event dashboard | Organiser | Stat tiles + chart (DASH-01) |
| P15 | Payout details | Organiser | Dot-matrix bars, ledger (kept) |
| P16 | Admin overview | Admin | Heat grid (DASH-01) |
| P17 | Admin users & moderation | Admin | Glitch stripe / ink |

Variants: A = light/peach, B = ember/dark, C = magenta/halftone.

## 4. Master prompt (paste this)

> **Project: Untitled — Events and Ticketing Engine (web, UI only).**
> 1. Read the folder `Illustrative designs/`. Use the `UNT-REF-*` names as the only way to refer to references. If I add images, analyse them (palette, layout, type, texture), rename to `UNT-REF-<CODE>-<nn>_<slug>`, and file them in the matching numbered subfolder.
> 2. Apply the "Quiet Stage" thesis (section 1 of `UNTITLED_Design-Thesis-and-Master-Prompt.md`).
> 3. Generate illustrations for P01–P17 in variants A/B/C. Output names: `UNT-ILL-Pxx_<page>_<variant>.png`, in `Untitled illustrations/Pxx_<page>/`. Size 1600×1000 unless the page needs a 4:5 auth half.
> 4. Verify each with a contact sheet: no text clipped, no overlaps, states readable without colour, grain visible, palette within the set.
> 5. Rebuild the reference board with these illustrations replacing all existing images, keep the white bento design and the lightbox, keep the same URL, and update the Claude Doc.
> 6. Only then move to Figma, using the illustrations as image fills.
> Constraints: no DB/PHP/backend; no mobile mockups; general events; never enter credentials for me; ask before downloads from third parties.

## 5. Process and tooling

Procedural Python engine (numpy, OpenCV, Pillow) with: mesh gradients, reeded glass remap with chromatic fringe, dot-matrix spheres, Bayer dither, grain, seat maps, ticket stubs, stat tiles. Fonts: Inter, Inter Display, Geist Mono, Instrument Sans, Bricolage Grotesque (OFL, from Anthropic's `canvas-design` fonts). Method follows the `canvas-design` skill: philosophy first, then expression, then a refinement pass.
