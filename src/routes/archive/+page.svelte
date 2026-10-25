<script lang="ts">
	import { onMount } from 'svelte';
	type Asset = {
		id: string;
		name: string;
		agent: string;
		category: string;
		status: string;
		url: string;
		format: string;
		bytes: number;
	};
	let assets = $state<Asset[]>([]),
		query = $state(''),
		agent = $state('all'),
		limit = $state(60),
		failed = $state(false);
	onMount(async () => {
		try {
			const r = await fetch('/library/dashies-archive.json');
			if (!r.ok) throw Error();
			assets = (await r.json()).assets;
		} catch {
			failed = true;
		}
	});
	const results = $derived(
		assets.filter(
			(a) =>
				(agent === 'all' || a.agent === agent) &&
				`${a.name} ${a.category} ${a.status}`.toLowerCase().includes(query.toLowerCase())
		)
	);
</script>

<svelte:head><title>Dashies archive — Jaxxties</title></svelte:head>
<section class="page-intro">
	<p class="eyebrow">THE ORIGINAL COLLECTION</p>
	<h1>Nothing <em>lost.</em></h1>
	<p class="lede">
		The complete Dashies catalog: masters, videos, studies, frames, prompts and review history.
		Original files remain in their source repository at a fixed revision.
	</p>
	<p class="caption">
		These are historical Dash.fi assets, not Jaxxton-ready artwork. GitHub access may be required.
	</p>
</section>
<section class="archive-list">
	<div class="filters">
		<label
			>Search the archive<input
				type="search"
				placeholder="Paper, shipping, pose…"
				bind:value={query}
				oninput={() => (limit = 60)}
			/></label
		><label
			>Character<select bind:value={agent} onchange={() => (limit = 60)}
				><option value="all">All characters</option
				>{#each ['shipping', 'ads', 'tariff', 'token', 'family'] as k}<option value={k}>{k}</option
					>{/each}</select
			></label
		>
		<p aria-live="polite">{results.length} records</p>
	</div>
	{#if failed}<p>
			Could not load the archive. <a href="/library/dashies-archive.json">Download the index</a>.
		</p>{:else if !assets.length}<p>Loading archive…</p>{/if}
	<div class="archive-rows">
		{#each results.slice(0, limit) as a}<a href={a.url} target="_blank" rel="noreferrer"
				><div><strong>{a.name}</strong><span>{a.category} · {a.agent} · {a.status}</span></div>
				<span class="mono">{a.format.toUpperCase()} ↗</span></a
			>{/each}
	</div>
	{#if results.length > limit}<button class="button quiet" onclick={() => (limit += 60)}
			>Show more</button
		>{/if}
</section>
