# Jaxxties

The Jaxxton character library, adapted from Dashies with the selected direction C: original narrow eyes, recognizable object characters and discreet XX tool details in the still artwork.

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
- Eight motion color studies, with 994 source frames in total. Exports include transparent VP9 WebM, packed-alpha H.264 MP4, ivory MP4 and posters as applicable.
- 43 active downloadable files, indexed with SHA-256 checksums and review status.
- A searchable index of all 1,731 historical Dashies records, linked to the immutable source revision. Historical media is not duplicated or relabeled as Jaxxton artwork.
- Original comparison, light/dark/checker previews, pause controls, reduced-motion handling, downloads, JSON registry and read-only MCP tools.

Shipping direction C was selected. Other masters, poses, family artwork and motion remain review candidates. **Motion is a palette study, not finished branded animation:** original motion and edge defects may remain, and XX tool engravings have not been tracked into the clips. The still references are the identity authority. The old Shipping calm source remains in the archive; this release rebuilds the eight available selected exports, not every historical experiment.

No production website integration or automatic promotion is performed by this library. Generated PNGs are raster artwork, not editable meshes or rigs.

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
- `static/reviews/motion/`: numbered contact sheets and metrics for every exported source frame. Sheets use a light/dark split; thumbnails are inspection aids, not the export aspect ratio.
- `static/history/`: superseded Jaxxton candidates, retained without overwriting them.
- `static/references/`: original Dashies masters for comparison.
- `static/library/catalog.json`: active file registry, mirrored into `src/lib/catalog.json` for server use.
- `static/library/dashies-archive.json`: historical source index. GitHub permission may be needed to open source links.
- `docs/*prompts.json`: exact recorded image-edit prompts and original generation paths. Those local paths record the generation environment; use the asset index for current repository files.
- `docs/PROVENANCE.json`: source revision and checksums for current, original and historical assets.

Packed MP4 layout is **alpha on the left, RGB on the right**. Use the included packed-alpha player; a normal video element shows both halves. Use the ivory MP4 for opaque placement on `#F7F6F4`, and WebM where alpha decoding is supported.

## Regenerate motion studies

The source baseline is `trlmkb/dashies` at `dc1319d1beeb0d00b85eeec85b1e5cb179fa2e3e`, which includes the approved Tariff page v4 absent from the older main snapshot. The upstream archive is unchanged.

The script requires Python with NumPy, OpenCV and Pillow, plus FFmpeg with libx264 and libvpx-vp9. Supply the source checkout's `static/mascots/motion` directory:

```sh
python scripts/rebrand-motion.py /path/to/dashies/static/mascots/motion
node scripts/register.mjs
pnpm mascots:check
```

The script changes palette without spatial or temporal blurring, retains source timing and uses a fixed crop over the complete motion envelope. Existing alpha is carried through before encoding; lossy video encoding can introduce small differences. Preserve old candidates before rerunning and increment versions for new releases.

## Read-only integration

- `GET /api/marketing/mascots.json`: active registry, including review status.
- `/mcp`: Streamable HTTP MCP endpoint, with `marketing_list_mascots` and `marketing_get_mascot`.
- Optional `JAXXTIES_TRUSTED_ORIGINS`: additional trusted origins, as parsed by `src/lib/server/origin.ts`.

Consumers must honor candidate/palette-study status instead of treating registry presence as production approval.

## Fonts

Cormorant Garamond, Inter Tight and Geist Mono are bundled locally under the SIL Open Font License. Notices and source links are in `static/fonts/licenses/`.
