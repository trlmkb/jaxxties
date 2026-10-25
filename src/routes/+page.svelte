<script lang="ts">
	import { characters } from '$lib/characters';
</script>

<section class="intro">
	<div>
		<p class="eyebrow">JAXXTON / THE CHARACTER COLLECTION</p>
		<h1>Same character.<br /><em>New signature.</em></h1>
		<p class="lede">
			Four familiar specialists. Oxblood, ink navy, warm brass and muted plum. The original eyes,
			with a quiet XX on the tools.
		</p>
		<a class="text-link" href="#characters">Explore the collection ↓</a>
	</div>
	<div class="intro-art">
		<img
			src="/family/family-hero-v3.png"
			alt="The four Jaxxton agents together"
			fetchpriority="high"
		/>
	</div>
</section>
<section class="collection" id="characters">
	<div class="section-heading">
		<h2>The agents</h2>
		<span class="eyebrow">01 — 04 / REFERENCES · POSES · MOTION</span>
	</div>
	<div class="character-grid">
		{#each characters as c, i}<a class="character-card" href={'/characters/' + c.key}
				><div class="card-top">
					<span class="eyebrow">0{i + 1}</span><span class="status"
						>{c.key === 'shipping' ? 'Selected direction' : 'Candidate'}</span
					>
				</div>
				<img src={'/characters/' + c.key + '/' + c.master} alt={c.name + ' agent'} loading="lazy" />
				<div class="card-bottom">
					<div>
						<h3>{c.name}</h3>
						<p>{c.role}</p>
					</div>
					<span aria-hidden="true">↗</span>
				</div></a
			>{/each}
	</div>
</section>
<section class="note-band">
	<h2>A small change.<br /><em>A familiar face.</em></h2>
	<div>
		<p>
			The character comes first: narrow eyes, rounded limbs, familiar tools and the original role
			markings. The rebrand lives in the materials and a discreet XX engraving.
		</p>
		<a class="text-link" href="/guide">Read the character guide ↗</a>
	</div>
</section>
