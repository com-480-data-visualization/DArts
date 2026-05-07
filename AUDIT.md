# DArts Milestone 3 Repository Audit

Audit date: 2026-05-07  
Repository: `com-480-data-visualization/DArts`  
Current branch: `master` tracking `origin/master`  
Working tree before audit: clean, with ignored `website/node_modules/`, `website/dist/`, and `data/__pycache__/`

## Scope

I inspected the tracked source, configuration, documentation, notebook metadata, generated web JSON, and MoMA submodule metadata. Large raw MoMA CSV/JSON files were audited by file size, headers, row counts, and source documentation rather than line-by-line inspection.

## Current Repository Inventory

### Root

- `.gitignore` covers Python caches, virtualenvs, notebooks checkpoints, Node `node_modules/`, `dist/`, `.DS_Store`, and raw MoMA CSV/JSON files.
- `.gitmodules` points `data/moma-collection` to `https://github.com/MuseumofModernArt/collection`.
- `README.md` contains Milestones 1 and 2 text, team names/SCIPERs, dataset description, EDA summary, and prototype URL. It does not yet satisfy the final M3 README requirements.
- `Data_Visualization___Milestone_2.pdf` is present as the M2 report/sketch artifact.
- `setup_data.sh` and `setup_data.ps1` initialize the MoMA submodule.
- No root `LICENSE`.
- No `.github/workflows/` deployment action.
- No `process_book.pdf`, `process_book/`, `screencast/`, or `screencast.mp4`.

### Data

- `data/moma-collection/` is a Git submodule. Present raw files:
  - `Artworks.csv`: 160,248 rows, 30 columns, 72.5 MB.
  - `Artists.csv`: 15,803 rows, 9 columns, 1.0 MB.
  - `Artworks.json`: 144.0 MB.
  - `Artists.json`: 3.6 MB.
  - MoMA `README.md`, `LICENSE.md` (CC0), and `CONTRIBUTING.md`.
- `data/process_data.py` is the current preprocessing script.
- Missing M3-required `data/build_aggregates.py`.
- Missing M3-required `data/regions.json`.

### Notebook

- `notebooks/exploratory_analysis.ipynb` exists.
- It has 23 cells: 12 markdown and 11 code cells.
- It covers setup, data cleaning, gender distribution, geographic diversity, departments, classification, medium, temporal analysis, medium trends, prolificacy, and summary.

### Website

The frontend is in `website/`, using Svelte + Vite + D3.

- `website/package.json`
  - Scripts: `dev`, `build`, `preview`, `deploy`.
  - Dependencies: `d3`, `topojson-client`.
  - Dev dependencies: `@sveltejs/vite-plugin-svelte`, `svelte`, `vite`, `gh-pages`.
  - Missing `lint`, `format`, and test/accessibility scripts.
- `website/vite.config.js`
  - Uses Svelte plugin.
  - `base: '/DArts/'`, appropriate for GitHub Pages.
- `website/svelte.config.js`
  - Uses `vitePreprocess`.
- `website/index.html`
  - Basic mount shell.
  - Contains mojibake in title/favicon markup due encoding issues.
- `website/src/main.js`
  - Mounts `App.svelte` and imports `global.css`.
- `website/src/App.svelte`
  - Fetches generated JSON from `./data/*.json`.
  - Renders hero, decade slider, globe, gender, nationality, department, timeline, and footer sections.
  - Uses Svelte 5 runes in plain JS.
  - No single global filter store.
  - No scroll-driven narrative.
  - No Scene 1 treemap, Scene 4 medium explorer, Scene 5 quiz, or proper Scene 6 credits.
- `website/src/global.css`
  - Defines current visual theme, fonts, colors, cards, section layout.
  - Uses large rounded cards, shadows, gradients, and decorative blurred shapes that should be toned down for the final course-grounded design.

### Existing Components

- `Hero.svelte`
  - Useful starting point for team/project introduction.
  - Needs replacement with M3 Scene 0: dark full-viewport data-art hero, animated headline number, no slider, and no section nav.
- `DecadeSlider.svelte`
  - Implements two-handle decade range filtering from timeline data.
  - Useful interaction base.
  - Needs refactor into global state, fixed 1860-2020 domain, URL hash sync, keyboard handlers, `aria` improvements, and scene visibility rules.
- `GlobeChart.svelte`
  - Uses `d3.geoOrthographic`, which is correct and should be kept.
  - Uses TopoJSON via runtime CDN fetch from `world-atlas`.
  - Has drag rotation and click-to-spotlight artist.
  - Needs major M3 work: neutral sequential ramp, legend, top-3 accent, scroll states, selected-country store, linked filtering, deterministic/random sample handling, smooth rotation to country, cleanup on destroy, and no runtime dependency surprise if possible.
- `GenderChart.svelte`
  - Currently renders a donut and stacked area chart.
  - Must be replaced for M3 because pie/donut charts are explicitly banned and Scene 3 requires a line chart plus department small multiples.
  - Gender currently collapses missing/non-binary values into `other`; M3 requires `female`, `male`, `non-binary`, and `unknown` shown explicitly.
- `NationalityChart.svelte`
  - Currently renders a horizontal bar chart and a streamgraph.
  - Not part of the locked M3 narrative as a separate scene.
  - Uses many categorical hues, exceeding the course color constraints.
  - Potentially reusable only for helper calculations or internal reference, not as final UI.
- `DepartmentChart.svelte`
  - Current bar chart can inform department aggregation, but final M3 requires department gender small multiples in Scene 3 and medium explorer in Scene 4.
  - Uses gradients and rounded/shadowed card styling that should be removed.
- `TimelineChart.svelte`
  - Current decade bar chart is useful as a reference for range highlighting.
  - Not part of locked final narrative except possibly as a small inset or debugging reference.

### Current Generated Web Data

Generated files under `website/public/data/`:

- `summary.json`: object, 284 bytes.
- `timeline.json`: 17 records.
- `gender.json`: 3 records.
- `gender_by_decade.json`: 50 records.
- `department.json`: 8 records.
- `department_by_decade.json`: 96 records.
- `classification.json`: 15 records.
- `nationality.json`: 30 records.
- `nationality_by_decade.json`: 153 records.
- `globe_countries.json`: 84 records.
- `globe_artists.json`: 1,997 records, 428 KB.

Important mismatch:

- Current `summary.json` reports `total_artworks = 91,881`.
- M1/M3 expected cleaned artwork total is `144,149`.
- Current `summary.json` reports `total_artists = 11,879`, matching the expected artist total.
- The artwork mismatch is caused by `data/process_data.py` dropping many rows with missing fields and requiring numeric `Date`, then filtering to 1860-2020. M3 requires earliest reliable artwork date where available and birth-decade fallback for artist matching, not dropping the wider cleaned dataset silently.

## Build Status

`npm run build` in `website/` succeeds.

Production output:

- `dist/index.html`: 0.62 KB, gzip 0.42 KB.
- `dist/assets/index-*.css`: 12.67 KB, gzip 3.14 KB.
- `dist/assets/index-*.js`: 163.41 KB, gzip 56.81 KB.

The build success confirms the prototype is runnable, but it does not validate M3 narrative, accessibility, color, interaction, or data requirements.

## What To Keep

- Keep Svelte + Vite + D3 stack.
- Keep `website/` as the app root unless later deployment constraints require moving files.
- Keep `base: '/DArts/'` in Vite for GitHub Pages.
- Keep the MoMA submodule and setup scripts, with minor documentation cleanup.
- Keep `notebooks/exploratory_analysis.ipynb` as the EDA deliverable.
- Keep `Data_Visualization___Milestone_2.pdf` as source material for process-book sketches.
- Reuse the two-handle interaction logic from `DecadeSlider.svelte`.
- Reuse the orthographic projection and drag logic from `GlobeChart.svelte`.
- Reuse the current generated JSON only as a temporary prototype input, not as final M3 data.

## What To Refactor Or Replace

### Data Pipeline

- Replace or supersede `data/process_data.py` with M3-required `data/build_aggregates.py`.
- Generate final data to `static/data/` or adapt the Vite public path consistently if the app remains non-SvelteKit.
- Add `data/regions.json` with fixed ISO3 to collapsed UN M49 region buckets.
- Preserve and surface `unknown` gender rather than collapsing missing values into `other`.
- Generate the required final outputs:
  - `medium_totals.json`
  - `country_by_decade.json`
  - `gender_by_decade.json`
  - `gender_by_decade_department.json`
  - `medium_breakdown.json`
  - `artist_index.json`
- Verify aggregate totals against `144,149` artworks and `11,879` artists, and document any unavoidable exclusions.

### App Architecture

- Add `src/lib/stores/globalFilters.js` or `.ts` exposing:
  - `decadeRange`
  - `selectedCountry`
  - `selectedDepartments`
  - `selectedRegions`
- Add URL hash sync with 300 ms debounce.
- Split the app into final scene components under `src/lib/scenes/`.
- Add shared components:
  - `DecadeSlider`
  - `Tooltip`
  - `SceneTitle`
  - `Annotation`
  - `Legend`
- Add a scroll/intersection utility for the martini-glass narrative.

### Visualizations

- Replace donut/pie use in `GenderChart.svelte`; pies and donuts are prohibited.
- Replace many-hue nationality palette and streamgraph with locked Scene 2 globe narrative.
- Add Scene 1 treemap using `d3.treemap()` with proportional area.
- Build Scene 3 as female-share line chart plus department small multiples.
- Build Scene 4 as top-9 medium small multiples with 100% stacked bars for gender and region.
- Build Scene 5 quiz with deterministic underrepresented artist match.
- Add final footer/credits/disclaimer scene.

### Course Design Compliance

- Remove decorative chart gradients, excessive shadows, and card-heavy section styling where it reduces data-ink ratio.
- Replace current globe `d3.interpolateYlOrRd` ramp with a neutral sequential luminance ramp and pop-out top-3 accent.
- Keep quantitative values on position/length/area, not hue alone.
- Ensure every chart has title, units, legend, source, and `n`.
- Ensure all bar charts start at zero.
- Add hover/click details on demand with visible affordances.
- Respect `prefers-reduced-motion`.
- Add keyboard support and `aria-label` coverage for interactive controls.

### Deliverables

- Rewrite top-level `README.md` for final M3 with pitch, live URL, stack, install/build/deploy instructions, data sources, folder structure, team members + SCIPERs, and screenshot.
- Add root `LICENSE` with MIT license for project code.
- Add `.github/workflows/deploy.yml` to build and deploy to `gh-pages` on pushes to `main`.
- Note that the current branch is `master`; either create/use `main` or adjust deployment instructions explicitly.
- Add `process_book/main.tex` and compile `process_book.pdf` at repo root.
- Add `screencast/script.md` and `screencast/shotlist.md`.

## Risks And Blockers

- The raw `Artworks.json` is 144 MB and `Artworks.csv` is 72.5 MB. Final site must only ship compact aggregates.
- The current preprocessing undercounts artworks relative to the M3 expected cleaned total.
- The existing prototype violates hard rules through donut chart use and silent collapse of unknown/non-binary gender.
- There is no GitHub Actions deployment workflow and no `main` branch in the current local checkout.
- No linting, formatting, axe, Lighthouse, or cross-browser automation is configured yet.
- Runtime CDN fetching of world topology can hurt reliability and performance; bundling or local static TopoJSON should be considered.

## Recommended Next Step

Proceed to Step 2: implement `data/build_aggregates.py` and `data/regions.json`, then verify generated JSON totals against:

- `n = 144,149` cleaned artworks.
- `n = 11,879` cleaned artists.

The data pipeline should be fixed before final scene implementation because every M3 scene depends on the new aggregate schema.
