<script lang="ts">
	let { src, alt, large = false }: { src: string; alt: string; large?: boolean } = $props();
	let surface = $state('ivory');
</script>

<div class:large class="stage" data-surface={surface}>
	<img {src} {alt} loading="lazy" />
	<div class="surface-control" aria-label="Preview background">
		{#each ['ivory', 'dark', 'checker'] as bg}<button
				class:active={surface === bg}
				aria-pressed={surface === bg}
				onclick={() => (surface = bg)}
				>{bg === 'ivory' ? 'Light' : bg === 'dark' ? 'Dark' : 'Alpha'}</button
			>{/each}
	</div>
</div>
