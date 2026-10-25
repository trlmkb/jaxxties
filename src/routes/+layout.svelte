<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';
	let { children } = $props();
</script>

<svelte:head
	><title>Jaxxties — Jaxxton character library</title><meta
		name="description"
		content="The Jaxxton character library: references, poses, family artwork and motion."
	/></svelte:head
>
<a class="skip" href="#main">Skip to content</a>
<header>
	<a class="wordmark" href="/">ja<span>xx</span>ties<span class="edition">01</span></a>
	<nav aria-label="Main navigation">
		{#each [['/', 'Characters'], ['/family', 'Family'], ['/archive', 'Archive'], ['/guide', 'Guide']] as [href, label]}<a
				{href}
				aria-current={page.url.pathname === href ? 'page' : undefined}>{label}</a
			>{/each}
	</nav>
	<a class="repo-link" href="https://github.com/trlmkb/jaxxties">Repository ↗</a>
</header>
<main id="main">{@render children()}</main>
<footer>
	<span>JAXXTON / CHARACTER LIBRARY</span><span>Original character. New signature.</span><a
		href="/api/marketing/mascots.json">Asset index ↗</a
	>
</footer>
