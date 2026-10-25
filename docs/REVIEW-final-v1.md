# Motion and artwork review — 2026-10-25

## Retained set

Shipping calm, Ads calm and playful, Tariff calm, and Token calm: five Seedance 2.5 performances, 145 frames each at 24 fps. All 725 frames were inspected in numbered, consecutive light/dark split contact sheets. Enlarged samples including the final frame supplement that review. This is contact-sheet review of every frame, not a claim that every frame was inspected at native resolution.

- Shipping calm retains the scanner on the reference side, narrow eyes, tape and barcode, and scanner XX.
- Ads retains the target, cursor, three browser dots, filter and XX detail in both performances.
- Tariff calm retains the globe, narrow eyes, top paper and stamp XX. Its paper stays inside the frame throughout.
- Token calm retains the receipt, arrows, chip and magnifier. The hand partly occludes the tool handle; the XX is not continuously visible.
- All active frames have zero alpha on the source border and at least 40 pixels of clear export margin. Background removal solves only a narrow edge band; no temporal or spatial smoothing was applied to interior details.
- Encoded WebM alpha was decoded with libvpx-vp9 and checked in every frame for transparent background, opaque interior and clear borders. FFprobe confirms duration, dimensions and frame counts for every active source and export. See `ENCODED-REVIEW-final-v1.json`.

The loop endpoints are generated return poses, not a mathematical first/last-frame identity guarantee. Small material and engraving variations can remain. Review in the intended final placement before production use.

## Withheld takes and remaining work

1. Shipping playful v3 changed scanner hands and introduced a broken light beam. The v4 retry still changes hands despite explicit prompt constraints. Both remain rejected.
2. Tariff playful v3 clips the raised paper against the source top border at frames 53–58 and 120–131.
3. Token playful v3 clips the lifted magnifier against the source right border at frames 100–102. Its eye shape also bends during the raised pose.

Widening the export canvas would not recover those missing source pixels, so the clipped takes are not included in the active manifest. Seedance video-edit correction requests for Tariff and Token were rejected before submission because the workspace has no remaining credits. Exact requests and responses are preserved in `generation/final-v1/*-reframe-pending.json`. Shipping needs another handedness-preserving take, preferably driven from the correct calm source or a fixed start frame. The full eight-performance scope is not complete.

Rejected exports, sources and frame reports are retained for traceability. None are advertised as finished downloads.

## Stills and family

Four masters and seven poses retain the selected narrow eyes, four distinct finishes and characteristic tools. Family hero v4 corrects the earlier Ads tool-side issue and fits all four bodies and tools. The horizontal lineup remains v3. Earlier family candidates are preserved under history. The upstream Dashies archive is unchanged.

## Library checks

All eight library routes checked at 1440px and 390px: no horizontal overflow or broken images. All four motion pages visually inspected at mobile size and desktop playback inspected. Pause works; light/dark/checker surfaces switch; reduced-motion prevents autoplay. All active download URLs and the JSON registry are checked, with MCP discovery verified separately.

Required repository checks: asset hashes and frame reports, Svelte diagnostics, formatting and production build pass. These checks do not constitute user approval or live-site integration.
