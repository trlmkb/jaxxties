import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root = new URL('../', import.meta.url).pathname;
const assets = [];
const walk = (dir) =>
	fs
		.readdirSync(dir, { withFileTypes: true })
		.flatMap((e) => (e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]));
for (const folder of ['characters', 'family', 'motion'])
	for (const file of walk(root + 'static/' + folder)) {
		if (!/\.(png|webp|webm|mp4)$/.test(file)) continue;
		const url = file.slice((root + 'static').length);
		const agent =
			folder === 'family'
				? 'family'
				: folder === 'characters'
					? url.split('/')[2]
					: path.basename(file).split('-')[0];
		assets.push({
			id: url.slice(1).replaceAll('/', '--'),
			name: path.basename(file),
			agent,
			category:
				folder === 'characters'
					? /master-v\d+\.png$/.test(file)
						? 'Reference'
						: 'Pose'
					: folder === 'family'
						? 'Family'
						: 'Motion',
			status:
				folder === 'motion'
					? 'palette-study'
					: file.endsWith('/shipping/master-v1.png')
						? 'selected-direction'
						: 'candidate',
			url,
			format: path.extname(file).slice(1),
			bytes: fs.statSync(file).size,
			sha256: crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
		});
	}
const catalog = {
	schemaVersion: 1,
	brand: 'Jaxxton',
	direction: 'C: narrow eyes, discreet XX tool engravings',
	sourceRevision: 'dc1319d1beeb0d00b85eeec85b1e5cb179fa2e3e',
	archive: '/library/dashies-archive.json',
	motionLimitations:
		'Palette studies preserve original actions and defects. XX tracking is pending; not approved final motion.',
	assets
};
const data = JSON.stringify(catalog, null, '\t') + '\n';
fs.writeFileSync(root + 'src/lib/catalog.json', data);
fs.writeFileSync(root + 'static/library/catalog.json', data);
console.log(`Registered ${assets.length} assets`);
