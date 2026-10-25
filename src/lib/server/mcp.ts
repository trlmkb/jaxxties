import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { z } from 'zod';
import catalog from '$lib/catalog.json';
export function createJaxxtiesMcpServer(origin: string) {
	const server = new McpServer({ name: 'jaxxties', version: '1.0.0' });
	const result = (data: unknown) => ({
		content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }]
	});
	server.registerTool(
		'marketing_list_mascots',
		{
			description:
				'List Jaxxton character assets, paths, checksums and approval status. Motion palette studies are not final branded motion.',
			inputSchema: { agent: z.enum(['shipping', 'ads', 'tariff', 'token', 'family']).optional() }
		},
		async ({ agent }) =>
			result({ origin, assets: catalog.assets.filter((a) => !agent || a.agent === agent) })
	);
	server.registerTool(
		'marketing_get_mascot',
		{
			description: 'Retrieve one Jaxxton asset by its exact ID, including download URL and status.',
			inputSchema: { id: z.string() }
		},
		async ({ id }) => {
			const asset = catalog.assets.find((a) => a.id === id);
			return asset
				? result({ ...asset, downloadUrl: origin + asset.url })
				: { isError: true, ...result({ error: 'Asset not found' }) };
		}
	);
	return server;
}
