export const characters = [
	{
		key: 'shipping',
		master: 'master-v1.png',
		name: 'Shipping',
		role: 'Parcel specialist',
		color: '#7B2E3B',
		material: 'Oxblood · ivory · graphite',
		tool: 'Scanner',
		description:
			'The familiar folded parcel, with its ivory tape and barcode intact. An oxblood finish and a discreet XX on the scanner carry the new identity.',
		locks: [
			'Continuous ivory tape',
			'Barcode and folded seams',
			'Graphite scanner with mint light'
		],
		poses: ['shipping-scan-v1']
	},
	{
		key: 'ads',
		master: 'master-v1.png',
		name: 'Ads',
		role: 'Click inspector',
		color: '#1F3A5F',
		material: 'Ink navy · ivory',
		tool: 'Traffic filter',
		description:
			'The original ad-window silhouette in ink navy. The cursor, target and three browser dots remain; the XX sits quietly on the filter tool.',
		locks: [
			'Three ivory browser dots',
			'Raised cursor and circular target',
			'Traffic filter paddle'
		],
		poses: ['ads-present-v1', 'ads-filter-v1']
	},
	{
		key: 'tariff',
		master: 'master-v2.png',
		name: 'Tariff',
		role: 'Classification specialist',
		color: '#A27C3E',
		material: 'Warm brass · champagne',
		tool: 'Stamp',
		description:
			'A layered document body in warm brass, with a lighter champagne globe and stamp. The paper tab and narrow eyes keep its original character.',
		locks: [
			'Layered document spine',
			'Paper tab with three rules',
			'Embossed globe and dark stamp pad'
		],
		poses: ['tariff-stamp-v2', 'tariff-present-v2']
	},
	{
		key: 'token',
		master: 'master-v2.png',
		name: 'Token',
		role: 'Usage inspector',
		color: '#6B4D78',
		material: 'Ivory · muted plum · brass',
		tool: 'Magnifier',
		description:
			'The ivory receipt stays central, framed by muted plum limbs and a brass magnifier. Its usage arrows, chip and torn edge remain recognizable.',
		locks: [
			'Curled ivory receipt',
			'Opposing usage arrows and chip',
			'Magnifier and sawtooth paper edge'
		],
		poses: ['token-inspect-v2', 'token-present-v2']
	}
];
export type Character = (typeof characters)[number];
