import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const root = new URL('../', import.meta.url).pathname;
const text = fs.readFileSync(root + 'static/library/catalog.json', 'utf8');
assert.equal(text, fs.readFileSync(root + 'src/lib/catalog.json', 'utf8'));
const { assets } = JSON.parse(text);
const seen = new Set();
for (const a of assets) {
	assert(!seen.has(a.id), `Duplicate ${a.id}`);
	seen.add(a.id);
	const bytes = fs.readFileSync(root + 'static' + a.url);
	assert.equal(bytes.length, a.bytes);
	assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), a.sha256, a.url);
}
for (const agent of ['shipping', 'ads', 'tariff', 'token']) {
	assert(assets.some((a) => a.agent === agent && a.category === 'Reference'));
	assert(assets.some((a) => a.agent === agent && a.category === 'Pose'));
	assert(assets.some((a) => a.agent === agent && a.category === 'Motion'));
}
const archive = JSON.parse(fs.readFileSync(root + 'static/library/dashies-archive.json', 'utf8'));
assert.equal(archive.assets.length, 1731);
assert(archive.assets.every((a) => a.legacy && a.url.includes(archive.snapshotRevision)));
const motions = JSON.parse(fs.readFileSync(root + 'static/motion/manifest.json', 'utf8'));
for (const m of motions) {
	assert(Math.abs(m.duration - m.frames / m.fps) < 0.001);
	for (const k of ['poster', 'page', 'packed', 'webm'])
		if (m[k]) assert(fs.existsSync(root + 'static' + m[k]));
	const review = JSON.parse(
		fs.readFileSync(root + 'static/reviews/motion/' + m.id + '.json', 'utf8')
	);
	assert.equal(review.frameMetrics.length, m.frames);
	assert(review.frameMetrics.every((f) => f.alphaPreservedBeforeEncoding));
	for (const s of m.reviewSheets) assert(fs.existsSync(root + 'static' + s));
}
console.log(
	`Verified ${assets.length} checksums, ${motions.length} clips, ${motions.reduce((n, c) => n + c.frames, 0)} frame records and 1,731 archive entries`
);
