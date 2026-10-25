/**
 * Origin validation for the public `/mcp` endpoint.
 *
 * Not an auth boundary — the server is stateless, read-only, and
 * unauthenticated. This validates the browser `Origin` header per the MCP
 * transport security guidance (DNS-rebinding hardening on HTTP transports).
 * Non-browser clients (curl, the MCP inspector, server-to-server callers)
 * omit `Origin`, so the check only constrains browser-originated requests.
 *
 * Policy:
 * - No `Origin` header → allow (non-browser client).
 * - `Origin` equals the request's own origin → allow. Derived from the
 *   request, so a same-origin browser request works on ANY deploy domain
 *   (the deployed Jaxxties domain, Vercel preview URLs, localhost)
 *   without hardcoding one. Browsers DO send `Origin` on same-origin POSTs,
 *   so this is the case that actually matters.
 * - `Origin` matches a trusted cross-origin client → allow (claude.ai /
 *   claude.com web clients, plus exact origins in `JAXXTIES_TRUSTED_ORIGINS`).
 * - Otherwise → deny.
 *
 * No global wildcard: extra trusted origins are exact-match only, so arbitrary
 * preview domains are not implicitly trusted.
 */

/** Trusted cross-origin browser clients, beyond the request's own origin. */
const DEFAULT_TRUSTED_ORIGIN_PATTERNS: RegExp[] = [
	/^https:\/\/([a-z0-9-]+\.)*claude\.ai$/,
	/^https:\/\/([a-z0-9-]+\.)*claude\.com$/,
	// Local development.
	/^https?:\/\/localhost(:\d+)?$/,
	/^https?:\/\/127\.0\.0\.1(:\d+)?$/
];

/**
 * Parse extra trusted origins from a comma/whitespace-separated config value
 * (e.g. `JAXXTIES_TRUSTED_ORIGINS="https://staging.example.com https://x.dev"`).
 * Exact strings only — no patterns — to avoid trusting arbitrary domains.
 */
export function parseTrustedOrigins(raw: string | null | undefined): string[] {
	if (!raw) return [];
	return raw
		.split(/[\s,]+/)
		.map((s) => s.trim())
		.filter(Boolean);
}

/**
 * True if a request carrying this `Origin` should be allowed through.
 *
 * @param origin       the request's `Origin` header, or `null` if absent
 * @param sameOrigin   the request's own origin (SvelteKit `url.origin`)
 * @param extraTrusted exact-match trusted origins from configuration
 */
export function isAllowedOrigin(
	origin: string | null,
	sameOrigin: string,
	extraTrusted: string[] = []
): boolean {
	if (origin === null) return true;
	if (origin === sameOrigin) return true;
	if (extraTrusted.includes(origin)) return true;
	return DEFAULT_TRUSTED_ORIGIN_PATTERNS.some((pattern) => pattern.test(origin));
}
