<script lang="ts">
	import Stage from '$lib/Stage.svelte';
	import Motion from '$lib/Motion.svelte';
	import { characters } from '$lib/characters';
	let { data } = $props();
	const c = $derived(data.character);
	let original = $state(false);
</script>

<svelte:head><title>{c.name} — Jaxxties</title></svelte:head>
<div class="page-top">
	<a href="/">← All characters</a>
	<nav aria-label="Character sections">
		<a href="#reference">Reference</a><a href="#poses">Poses</a><a href="#motion">Motion</a>
	</nav>
</div>
<section class="character-hero" id="reference">
	<div>
		<p class="eyebrow">{c.role}</p>
		<h1>{c.name}<br /><em>Agent.</em></h1>
		<p class="lede">{c.description}</p>
		<p class="material">{c.material}</p>
		<div class="actions">
			<a class="button" href={'/characters/' + c.key + '/' + c.master} download>Download PNG ↓</a
			><button class="quiet" aria-pressed={original} onclick={() => (original = !original)}
				>{original ? 'Show Jaxxton' : 'Compare original'}</button
			>
		</div>
		<p class="caption">
			{original
				? 'Original Dashies reference'
				: c.key === 'shipping'
					? 'Selected direction C · transparent PNG'
					: 'Rebrand candidate · transparent PNG'}
		</p>
	</div>
	<Stage
		src={original
			? '/references/' + c.key + '-dashies.png'
			: '/characters/' + c.key + '/' + c.master}
		alt={c.name + ' reference'}
		large
	/>
</section>
<section class="identity">
	<p class="eyebrow">KEEP THE CHARACTER</p>
	<div>
		{#each c.locks as lock}<p>{lock}</p>{/each}
		<p>Narrow horizontal eyes. Never X eyes.</p>
	</div>
</section>
<section class="collection" id="poses">
	<div class="section-heading">
		<h2>Poses & gestures</h2>
		<span class="eyebrow">TRANSPARENT / CANDIDATES</span>
	</div>
	<div class="pose-grid">
		{#each c.poses as pose}<article>
				<Stage src={'/characters/' + c.key + '/' + pose + '.png'} alt={pose.replaceAll('-', ' ')} />
				<div class="asset-caption">
					<h3>{pose.split('-')[1]}</h3>
					<a href={'/characters/' + c.key + '/' + pose + '.png'} download>PNG ↓</a>
				</div>
			</article>{/each}
	</div>
</section>
<section class="collection" id="motion">
	<div class="section-heading">
		<h2>In motion</h2>
		<span class="eyebrow">ORIGINAL ACTION / NEW PALETTE</span>
	</div>
	<p class="section-copy">
		Color studies retain the original timing and silhouette. Review each clip before use; the still
		artwork defines the final materials and XX tool marks.
	</p>
	{#key c.key}<Motion agent={c.key} />{/key}
</section>
<section class="more-agents">
	<p class="eyebrow">THE REST OF THE FAMILY</p>
	{#each characters.filter((x) => x.key !== c.key) as other}<a href={'/characters/' + other.key}
			>{other.name} ↗</a
		>{/each}
</section>
