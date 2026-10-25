<script lang="ts">
	import Stage from '$lib/Stage.svelte';
</script>

<svelte:head><title>Family artwork — Jaxxties</title></svelte:head>
<section class="page-intro">
	<p class="eyebrow">BETTER TOGETHER</p>
	<h1>The whole <em>family.</em></h1>
	<p class="lede">
		Two compositions for the full collection. No baked-in background, glow or headline.
	</p>
</section>
<section class="family-grid">
	{#each [['family-hero-v3', 'Hero group', 'Compact two-row composition. Mostly forward gaze, a subtle leftward Shipping angle.'], ['family-lineup-v3', 'At work', 'A wider lineup for section introductions and supporting illustrations.']] as [id, title, description]}<article
		>
			<Stage src={'/family/' + id + '.png'} alt={title} large />
			<div class="asset-caption">
				<div>
					<h2>{title}</h2>
					<p>{description}</p>
				</div>
				<a class="button quiet" href={'/family/' + id + '.png'} download>PNG ↓</a>
			</div>
			<p class="caption">
				Candidate · transparent background · generated from original family artwork
			</p>
		</article>{/each}
</section>
