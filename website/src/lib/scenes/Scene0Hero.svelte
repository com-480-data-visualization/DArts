<script>
  import { onDestroy, onMount } from 'svelte';

  export let summary;

  const DOT_COUNT = 600;
  let canvas;
  let section;
  let frame = 0;
  let width = 0;
  let height = 0;
  let dots = [];
  let ctx;
  let visible = true;
  let reduceMotion = false;
  let seq2 = [201, 168, 95];
  let seq3 = [142, 107, 44];

  function hexToRgb(hex) {
    const clean = hex.trim().replace('#', '');
    const value = Number.parseInt(clean, 16);
    return [(value >> 16) & 255, (value >> 8) & 255, value & 255];
  }

  function seededRandom(seed) {
    let value = seed;
    return () => {
      value = (value * 1664525 + 1013904223) % 4294967296;
      return value / 4294967296;
    };
  }

  function resize() {
    if (!canvas || !ctx) return;
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    width = section?.clientWidth || window.innerWidth;
    height = section?.clientHeight || window.innerHeight;
    canvas.width = Math.floor(width * ratio);
    canvas.height = Math.floor(height * ratio);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  }

  function buildDots() {
    const random = seededRandom(480);
    dots = Array.from({ length: DOT_COUNT }, () => ({
      x: random() * width,
      y: random() * height,
      vx: (random() - 0.5) * 0.18,
      vy: (random() - 0.5) * 0.18,
      radius: 0.7 + random() * 1.8,
      mix: random(),
    }));
  }

  function draw() {
    if (!ctx || !canvas) return;
    ctx.clearRect(0, 0, width, height);
    for (const dot of dots) {
      if (!reduceMotion) {
        dot.x = (dot.x + dot.vx + width) % width;
        dot.y = (dot.y + dot.vy + height) % height;
      }
      const rgb = seq2.map((value, index) => Math.round(value + (seq3[index] - value) * dot.mix));
      ctx.beginPath();
      ctx.fillStyle = `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, 0.35)`;
      ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
      ctx.fill();
    }
    if (visible && !reduceMotion) frame = requestAnimationFrame(draw);
  }

  function start() {
    cancelAnimationFrame(frame);
    if (visible && !reduceMotion) frame = requestAnimationFrame(draw);
    else draw();
  }

  onMount(() => {
    ctx = canvas.getContext('2d', { alpha: true });
    reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const styles = getComputedStyle(document.documentElement);
    seq2 = hexToRgb(styles.getPropertyValue('--seq-2'));
    seq3 = hexToRgb(styles.getPropertyValue('--seq-3'));
    resize();
    buildDots();
    start();

    const observer = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      start();
    });
    observer.observe(section);
    window.addEventListener('resize', resize);

    return () => {
      observer.disconnect();
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(frame);
    };
  });

  onDestroy(() => cancelAnimationFrame(frame));
</script>

<section class="hero-scene" bind:this={section} aria-label="DArts introduction">
  <canvas bind:this={canvas} aria-hidden="true"></canvas>
  <p class="mark">DArts</p>
  <div class="hero-copy" aria-live="polite">
    <p class="line l1"><span class="num">{summary.n_artworks_total.toLocaleString()}</span> works.</p>
    <p class="line l2"><span class="num">{summary.n_artists_total.toLocaleString()}</span> artists.</p>
    <p class="line l3">One question:</p>
    <h1 class="line l4">Who's actually in there?</h1>
  </div>
  <div class="scroll-cue" aria-hidden="true">
    <span>Scroll</span>
    <span class="caret"></span>
  </div>
</section>

<style>
  .hero-scene {
    position: relative;
    min-height: 100vh;
    overflow: hidden;
    display: grid;
    place-items: center;
    color: var(--fg-on-dark-strong);
    background: var(--bg-dark);
  }

  canvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
  }

  .mark {
    position: absolute;
    top: var(--space-4);
    left: var(--space-4);
    margin: 0;
    color: var(--fg-on-dark-strong);
    font-family: var(--font-display);
    font-size: var(--type-h3-size);
    font-weight: 600;
  }

  .hero-copy {
    position: relative;
    z-index: 1;
    width: min(58rem, calc(100vw - var(--space-4)));
    text-align: center;
  }

  .line {
    margin: 0;
    opacity: 0;
    translate: 0 0.75rem;
    animation: hero-line 900ms var(--ease-out) forwards;
  }

  .l1,
  .l2,
  .l3 {
    color: var(--fg-on-dark-mute);
    font-family: var(--font-ui);
    font-size: clamp(1.25rem, 4vw, var(--type-h2-size));
    font-weight: 600;
    line-height: var(--type-h2-line);
  }

  .l2 {
    animation-delay: 650ms;
  }

  .l3 {
    animation-delay: 1300ms;
  }

  .l4 {
    margin-top: var(--space-2);
    color: var(--fg-on-dark-strong);
    font-family: var(--font-display);
    font-size: clamp(2.75rem, 9vw, var(--type-display-size));
    font-weight: 600;
    line-height: var(--type-display-line);
    animation-delay: 2100ms;
  }

  .num {
    color: var(--seq-1);
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
  }

  .scroll-cue {
    position: absolute;
    bottom: var(--space-4);
    left: 50%;
    z-index: 1;
    display: grid;
    gap: var(--space-1);
    justify-items: center;
    color: var(--fg-on-dark-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
    translate: -50% 0;
    animation: cue-bob 1600ms var(--ease-inout) infinite;
  }

  .caret {
    width: 0.625rem;
    height: 0.625rem;
    border-right: 1px solid currentColor;
    border-bottom: 1px solid currentColor;
    rotate: 45deg;
  }

  @keyframes hero-line {
    to {
      opacity: 1;
      translate: 0 0;
    }
  }

  @keyframes cue-bob {
    50% {
      translate: -50% 0.375rem;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .line {
      opacity: 1;
      translate: 0 0;
      animation: none;
    }

    .scroll-cue {
      animation: none;
    }
  }
</style>
