import type { RequestHandler } from './$types';
import { WebStandardStreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js';
import { createJaxxtiesMcpServer } from '$lib/server/mcp.js';
import { isAllowedOrigin, parseTrustedOrigins } from '$lib/server/origin.js';
import { env } from '$env/dynamic/private';

const corsHeaders: Record<string, string> = {
	'Access-Control-Allow-Origin': '*',
	'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
	'Access-Control-Allow-Headers': 'Content-Type, Authorization, Mcp-Session-Id',
	'Access-Control-Expose-Headers': 'Mcp-Session-Id'
};

async function handle(request: Request, sameOrigin: string): Promise<Response> {
	const origin = request.headers.get('Origin');
	if (!isAllowedOrigin(origin, sameOrigin, parseTrustedOrigins(env.JAXXTIES_TRUSTED_ORIGINS))) {
		return new Response('Forbidden — origin not allowed.', {
			status: 403,
			headers: { 'Content-Type': 'text/plain; charset=utf-8' }
		});
	}

	const server = createJaxxtiesMcpServer(sameOrigin);
	const transport = new WebStandardStreamableHTTPServerTransport({});
	await server.connect(transport);

	const response = await transport.handleRequest(request);

	// Layer CORS headers on top of the transport's response.
	const headers = new Headers(response.headers);
	for (const [k, v] of Object.entries(corsHeaders)) headers.set(k, v);

	return new Response(response.body, {
		status: response.status,
		statusText: response.statusText,
		headers
	});
}

export const GET: RequestHandler = ({ request, url }) => handle(request, url.origin);
export const POST: RequestHandler = ({ request, url }) => handle(request, url.origin);

export const OPTIONS: RequestHandler = () =>
	new Response(null, { status: 204, headers: corsHeaders });

/**
 * Don't prerender the MCP endpoint — it's dynamic.
 */
export const prerender = false;
