export function mountPackedAlphaLoop(root: HTMLElement): () => void {
	const canvas = root.querySelector('canvas');
	const video = root.querySelector('video');
	const button = root.querySelector('button');
	const status = root.querySelector<HTMLElement>('.status');
	const cleanup = () => undefined;
	if (!canvas || !video || !button || !status) return cleanup;
	const gl = canvas.getContext('webgl', {
		alpha: true,
		antialias: false,
		depth: false,
		premultipliedAlpha: true,
		preserveDrawingBuffer: true
	});
	if (!gl) {
		button.hidden = true;
		status.textContent = 'Still preview — animation is unavailable in this browser.';
		return cleanup;
	}
	const compile = (type: number, source: string) => {
		const shader = gl.createShader(type);
		if (!shader) return null;
		gl.shaderSource(shader, source);
		gl.compileShader(shader);
		if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
			gl.deleteShader(shader);
			return null;
		}
		return shader;
	};
	const vertex = compile(
		gl.VERTEX_SHADER,
		`
    attribute vec2 p;
    varying vec2 uv;
    void main() {
      uv = vec2(p.x * .5 + .5, .5 - p.y * .5);
      gl_Position = vec4(p, 0., 1.);
    }
  `
	);
	const fragment = compile(
		gl.FRAGMENT_SHADER,
		`
    precision mediump float;
    uniform sampler2D tex;
    varying vec2 uv;
    void main() {
      float a = texture2D(tex, vec2(uv.x * .5, uv.y)).r;
      vec3 rgb = texture2D(tex, vec2(uv.x * .5 + .5, uv.y)).rgb;
      gl_FragColor = vec4(rgb * a, a);
    }
  `
	);
	const program = gl.createProgram();
	if (!vertex || !fragment || !program) return cleanup;
	gl.attachShader(program, vertex);
	gl.attachShader(program, fragment);
	gl.linkProgram(program);
	if (!gl.getProgramParameter(program, gl.LINK_STATUS)) return cleanup;
	gl.useProgram(program);
	const buffer = gl.createBuffer();
	gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
	gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
	const attribute = gl.getAttribLocation(program, 'p');
	gl.enableVertexAttribArray(attribute);
	gl.vertexAttribPointer(attribute, 2, gl.FLOAT, false, 0, 0);
	const texture = gl.createTexture();
	gl.bindTexture(gl.TEXTURE_2D, texture);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
	const motion = matchMedia('(prefers-reduced-motion: reduce)');
	const connection = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection;
	let wanted = !motion.matches && !connection?.saveData;
	let visible = false;
	let disposed = false;
	let frame = 0;
	let lastTime = -1;
	const draw = () => {
		if (disposed || video.readyState < 2) return;
		if (canvas.width !== video.videoWidth / 2) canvas.width = video.videoWidth / 2;
		if (canvas.height !== video.videoHeight) canvas.height = video.videoHeight;
		gl.viewport(0, 0, canvas.width, canvas.height);
		gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, video);
		gl.drawArrays(gl.TRIANGLES, 0, 3);
		root.setAttribute('data-ready', '');
	};
	const tick = () => {
		if (disposed || video.paused) return;
		if (video.currentTime !== lastTime) {
			draw();
			lastTime = video.currentTime;
		}
		frame = requestAnimationFrame(tick);
	};
	const sync = () => {
		button.textContent = wanted ? 'Pause animation' : 'Play animation';
		button.setAttribute('aria-pressed', String(wanted));
		if (!wanted || !visible || document.hidden) {
			video.pause();
			cancelAnimationFrame(frame);
			return;
		}
		if (!video.getAttribute('src')) video.src = video.dataset.src ?? '';
		void video
			.play()
			.then(() => {
				if (disposed || !wanted || !visible || document.hidden) {
					video.pause();
					return;
				}
				cancelAnimationFrame(frame);
				tick();
			})
			.catch(() => {
				wanted = false;
				button.textContent = 'Play animation';
				button.setAttribute('aria-pressed', 'false');
			});
	};
	const toggle = () => {
		wanted = !wanted;
		sync();
	};
	const reduce = () => {
		if (motion.matches) {
			wanted = false;
			sync();
		}
	};
	const error = () => {
		wanted = false;
		sync();
		root.removeAttribute('data-ready');
		status.textContent = 'Showing the still preview. The animation could not load.';
	};
	const observer = new IntersectionObserver(([entry]) => {
		visible = entry.isIntersecting;
		sync();
	});
	observer.observe(root);
	button.addEventListener('click', toggle);
	video.addEventListener('seeked', draw);
	video.addEventListener('error', error);
	motion.addEventListener('change', reduce);
	document.addEventListener('visibilitychange', sync);
	return () => {
		disposed = true;
		cancelAnimationFrame(frame);
		observer.disconnect();
		button.removeEventListener('click', toggle);
		video.removeEventListener('seeked', draw);
		video.removeEventListener('error', error);
		motion.removeEventListener('change', reduce);
		document.removeEventListener('visibilitychange', sync);
		video.pause();
		video.removeAttribute('src');
		video.load();
		gl.deleteTexture(texture);
		gl.deleteBuffer(buffer);
		gl.deleteProgram(program);
		gl.deleteShader(vertex);
		gl.deleteShader(fragment);
	};
}
