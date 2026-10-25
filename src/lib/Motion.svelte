<script lang="ts">
	import { onMount } from 'svelte';
	import { mountPackedAlphaLoop } from './packed-alpha-loop';
	type Clip = {
		id: string;
		agent: string;
		variant: string;
		poster: string;
		page: string;
		dark: string;
		source: string;
		packed: string | null;
		webm: string | null;
		frames: number;
		duration: number;
		width: number;
		height: number;
		reviewSheets: string[];
		reviewFramesPerSheet: number;
		reviewReport: string;
	};
	let { agent }: { agent: string } = $props();
	let clips = $state<Clip[]>([]),
		error = $state(false),
		background = $state('light');
	onMount(async () => {
		try {
			const r = await fetch('/motion/manifest.json');
			if (!r.ok) throw Error();
			clips = (await r.json()).filter((c: Clip) => c.agent === agent);
		} catch {
			error = true;
		}
	});
	function mount(node: HTMLElement) {
		return { destroy: mountPackedAlphaLoop(node) };
	}
</script>

<div class="motion-toolbar">
	<span class="caption">Preview background</span>{#each ['light', 'dark', 'checker'] as bg}<button
			class="quiet"
			aria-pressed={background === bg}
			onclick={() => (background = bg)}>{bg}</button
		>{/each}
</div>
{#if error}<p>Motion is unavailable. Please reload or use the repository exports.</p>{/if}
<div class="motion-grid">
	{#each clips as clip}<article>
			<div
				class="motion-stage"
				data-surface={background}
				style:aspect-ratio={clip.width / clip.height}
			>
				{#if clip.packed}<div use:mount>
						<img src={clip.poster} alt={agent + ' ' + clip.variant + ' motion poster'} /><canvas
							aria-label={agent + ' ' + clip.variant + ' animation'}
						></canvas><video data-src={clip.packed} muted loop playsinline preload="none"
						></video><button aria-pressed="false">Play animation</button><span
							class="status sr-only"
							aria-live="polite"
						></span>
					</div>{:else}<video
						class="opaque-video"
						src={clip.page}
						poster={clip.poster}
						controls
						loop
						muted
						playsinline
						preload="metadata"
						aria-label={agent + ' ' + clip.variant + ' animation'}
					></video>{/if}
			</div>
			<div class="asset-caption">
				<div>
					<h3>{clip.variant === 'page' ? 'Page version' : clip.variant}</h3>
					<p>{clip.duration.toFixed(2)}s · {clip.frames} frames · {clip.width} × {clip.height}</p>
				</div>
			</div>
			<div class="download-row">
				{#if clip.webm}<a href={clip.webm} download>Alpha WebM ↓</a><a href={clip.packed!} download
						>Packed MP4 ↓</a
					>{/if}<a href={clip.page} download>Ivory MP4 ↓</a><a href={clip.dark} download
					>Dark MP4 ↓</a
				><a href={clip.poster} download>Poster ↓</a>
			</div>
			<details>
				<summary>Frame review & source</summary>
				<p class="caption">
					Every frame on light and dark. Generated from the character reference with its XX tool
					detail.
				</p>
				<div class="review-links">
					{#each clip.reviewSheets as sheet, i}<a href={sheet} target="_blank" rel="noreferrer"
							>Frames {i * clip.reviewFramesPerSheet}–{Math.min(
								clip.frames - 1,
								(i + 1) * clip.reviewFramesPerSheet - 1
							)} ↗</a
						>{/each}
				</div>
				<div class="download-row">
					<a href={clip.reviewReport}>Review data ↗</a><a href={clip.source} download
						>Original green-screen MP4 ↓</a
					>
				</div>
			</details>
		</article>{/each}
</div>
