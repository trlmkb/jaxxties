# Jaxxties

The Jaxxton character library, adapted from Dashies with the selected direction C: original narrow eyes, recognizable object characters and discreet XX tool details through the character artwork and new motion references.

## Four characters, four colors

| Character | Primary finish | Role detail |
| --- | --- | --- |
| Shipping | Oxblood `#7B2E3B` | Ivory tape, barcode and scanner |
| Ads | Ink navy `#1F3A5F` | Target, cursor and filter tool |
| Tariff | Warm brass `#A27C3E` | Champagne globe, paper and stamp |
| Token | Muted plum `#6B4D78` | Ivory receipt and brass magnifier |

Brass and plum extend the mascot palette to distinguish the four roles. These are material directions, not flat pixel colors: highlights, texture and shadows vary.

## Collection and status

- Four master references, seven poses and two transparent family compositions.
- Five reviewed Seedance 2.5 movies: calm for all four agents and playful for Ads. Each is 145 frames at 24 fps (6.042 seconds); 725 active frames total.
- Every movie includes alpha VP9 WebM, packed-alpha H.264, ivory and dark H.264, a transparent poster, the original green-screen source and numbered frame-review sheets.
- 43 active downloadable files, including the five source movies, indexed with SHA-256 checksums and review status.
- Searchable index of all 1,731 historical Dashies records at an immutable source revision. Historical media is not relabeled as Jaxxton artwork.
- Original comparisons, light/dark/checker previews, pause controls, reduced-motion handling, JSON registry and read-only MCP tools.

**Remaining work:** the playful Shipping, Tariff and Token movies are withheld. Shipping's scanner changes hands; Tariff's raised paper and Token's lifted magnifier clip their source frames. Their rejected takes and review evidence are preserved under `static/history/motion/rejected` and `static/reviews/final-v1`. Replacement requests could not be submitted because Higgsfield reported exhausted credits. Exact pending prompts are in `docs/generation/final-v1`.

Shipping direction C was selected. The other stills remain candidates; `reviewed-export` records the technical/visual review of new movies, not user approval or production readiness in every layout. Small generated texture and engraving variations may remain. Source artwork is the identity authority.

No production website integration or automatic merge is performed. Generated PNGs and movies are raster media, not editable meshes or rigs.

## Run and validate

```sh
pnpm install --frozen-lockfile
pnpm dev
pnpm mascots:check
pnpm check
pnpm format:check
pnpm build
```

The app uses SvelteKit with the Vercel adapter. Deploy feature branches as previews; review before merging.

## Asset layout

- `static/characters/`: current versioned master references and poses.
- `static/family/`: current hero and lineup compositions.
- `static/motion/manifest.json`: clip paths, source hashes, dimensions, frame counts, duration, crop and limitations.
- `static/reviews/final-v1/`: numbered contact sheets and metrics for every exported source frame. Sheets use a light/dark split, 24 consecutive frames per sheet, preserving the export aspect ratio. Enlarged samples supplement this review.
- `static/history/`: superseded Jaxxton candidates, retained without overwriting them.
- `static/references/`: original Dashies masters for comparison.
- `static/library/catalog.json`: active file registry, mirrored into `src/lib/catalog.json` for server use.
- `static/library/dashies-archive.json`: historical source index. GitHub permission may be needed to open source links.
- `docs/*prompts.json`: exact recorded image-edit prompts and original generation paths. Those local paths record the generation environment; use the asset index for current repository files.
- `docs/PROVENANCE.json`: source revision and checksums for current, original and historical assets.

Packed MP4 layout is **alpha on the left, RGB on the right**. Use the included packed-alpha player; a normal video element shows both halves. Use ivory MP4 on `#F7F6F4`, dark MP4 on `#1C090C`, and WebM where alpha decoding is supported.

## Reproduce the movie exports

Exact prompts, model settings, job IDs and result URLs are recorded in `docs/generation/final-v1`. All new movies use Seedance 2.5 from the corresponding master reference. Sources are stored with the exports; hashes bind each source to its frame report.

The finishing script requires NumPy, OpenCV, Pillow and FFmpeg with libx264 and libvpx-vp9. Place a source in `output/final-v1/<agent>-<variant>-source.mp4`, then run:

```sh
python scripts/finish-motion.py ads-calm
node scripts/register.mjs
pnpm mascots:check
```

The script estimates the green stage color and solves alpha only within a six-pixel edge band, without spatial or temporal filtering of the character interior. It applies a fixed crop over the entire motion envelope and premultiplied resampling. Generated records start as `pending-review`: inspect every frame and confirm no source-border clipping before adding them to the active manifest with `reviewed-export` status. Encoding is lossy.

Set `MOTION_VERSION` and `SOURCE_VERSION` for new versions; preserve prior files before exporting. Old palette-only studies and the historical Dashies archive remain intact. The archive baseline is `trlmkb/dashies` revision `dc1319d1beeb0d00b85eeec85b1e5cb179fa2e3e`.

## Read-only integration

- `GET /api/marketing/mascots.json`: active registry, including review status.
- `/mcp`: Streamable HTTP MCP endpoint, with `marketing_list_mascots` and `marketing_get_mascot`.
- Optional `JAXXTIES_TRUSTED_ORIGINS`: additional trusted origins, as parsed by `src/lib/server/origin.ts`.

Consumers must honor candidate/reviewed-export status instead of treating registry presence as production approval.

## Fonts

Cormorant Garamond, Inter Tight and Geist Mono are bundled locally under the SIL Open Font License. Notices and source links are in `static/fonts/licenses/`.
