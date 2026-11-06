# Untitled: Events and Ticketing Engine, design reference board

COMP 3540 Part 2 (UI only). A web app for general events: concerts, sport, theatre, conferences, festivals.

**Open `index.html`** (or the GitHub Pages link for this repo) to browse the board.

- 17 pages, 41 segments, 174 images. Each segment has three white, minimal directions: Grid, Cards, Type.
- `images/` the board images (web-size JPEG)
- `UNTITLED_Design-Thesis-and-Master-Prompt.md` design thesis and the reusable prompt
- `src/illustration-engine` Python that draws the full-page art (ribbed glass, dot-matrix, halftone, grain)
- `src/segments` HTML/CSS templates and the renderer for the segment designs
- `src/board` the script that builds `index.html`

The scripts were written against local working folders, so paths inside them point there. They are included for reference.
Names, emails and card numbers in the designs are placeholders.
