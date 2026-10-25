import { error } from '@sveltejs/kit';
import { characters } from '$lib/characters';
export function load({ params }) {
	const character = characters.find((c) => c.key === params.agent);
	if (!character) error(404, 'Character not found');
	return { character };
}
