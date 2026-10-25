import { json } from '@sveltejs/kit';
import catalog from '$lib/catalog.json';
export const GET = () => json(catalog, { headers: { 'Cache-Control': 'public, max-age=300' } });
