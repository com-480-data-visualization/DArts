<script>
  import { hierarchy, treemap, treemapSquarify } from 'd3-hierarchy';
  import Annotation from '../components/Annotation.svelte';

  export let data = [];
  export let highlighted = [];
  export let annotation = null;
  export let lockedMedium = '';
  export let onLock = () => {};

  const width = 760;
  const height = 560;
  const labelArea = 15000;

  $: root = hierarchy({ children: data })
    .sum((d) => d.n ?? 0)
    .sort((a, b) => (b.value ?? 0) - (a.value ?? 0));
  $: layout = treemap().size([width, height]).paddingInner(1).tile(treemapSquarify)(root);
  $: leaves = layout.leaves().map((leaf, index) => ({ ...leaf, rank: index }));
  $: activeSet = new Set(lockedMedium ? [lockedMedium] : highlighted);
  $: activeLeaf = leaves.find((leaf) => activeSet.has(leaf.data.medium));

  function showTooltip(event, leaf) {
    const pct = Number(leaf.data.pct).toFixed(1);
    window.dispatchEvent(
      new CustomEvent('darts:tooltip', {
        detail: {
          x: event.clientX,
          y: event.clientY,
          content: `<strong>${leaf.data.medium}</strong><br><span class="num">${leaf.data.n.toLocaleString()}</span> works<br><span class="num">${pct}%</span> of cleaned collection`,
        },
      }),
    );
  }

  function hideTooltip() {
    window.dispatchEvent(new CustomEvent('darts:tooltip-hide'));
  }

  function motifLines(leaf) {
    const w = leaf.x1 - leaf.x0;
    const h = leaf.y1 - leaf.y0;
    const pad = Math.max(8, Math.min(w, h) * 0.08);
    if (w < 42 || h < 42) return [];
    if (leaf.rank % 3 === 0) {
      return Array.from({ length: 5 }, (_, i) => ({
        x1: leaf.x0 + pad,
        y1: leaf.y0 + pad + i * ((h - pad * 2) / 4),
        x2: leaf.x1 - pad,
        y2: leaf.y0 + pad + i * ((h - pad * 2) / 4) + (i % 2 ? -8 : 8),
      }));
    }
    if (leaf.rank % 3 === 1) {
      return Array.from({ length: 6 }, (_, i) => ({
        x1: leaf.x0 + pad + i * ((w - pad * 2) / 6),
        y1: leaf.y1 - pad,
        x2: leaf.x0 + pad + i * ((w - pad * 2) / 6) + Math.min(32, w * 0.16),
        y2: leaf.y0 + pad,
      }));
    }
    return Array.from({ length: 4 }, (_, i) => ({
      x1: leaf.x0 + pad + i * ((w - pad * 2) / 4),
      y1: leaf.y0 + pad,
      x2: leaf.x0 + pad + i * ((w - pad * 2) / 4) + Math.min(44, w * 0.18),
      y2: leaf.y1 - pad,
    }));
  }
</script>

<figure class="treemap" aria-label="Treemap of MoMA collection areas by number of works">
  <svg viewBox={`0 0 ${width} ${height}`}>
    <title>Treemap of MoMA collection areas by number of works</title>
    <defs>
      {#each leaves as leaf}
        <clipPath id={`leaf-clip-${leaf.rank}`}>
          <rect x={leaf.x0} y={leaf.y0} width={leaf.x1 - leaf.x0} height={leaf.y1 - leaf.y0} />
        </clipPath>
      {/each}
    </defs>
    {#each leaves as leaf}
      {@const leafWidth = leaf.x1 - leaf.x0}
      {@const leafHeight = leaf.y1 - leaf.y0}
      {@const area = leafWidth * leafHeight}
      <g class="leaf" style:--rank={leaf.rank}>
        <rect
          class="mark"
          x={leaf.x0}
          y={leaf.y0}
          width={leafWidth}
          height={leafHeight}
          class:highlight={activeSet.has(leaf.data.medium)}
          onpointermove={(event) => showTooltip(event, leaf)}
          onpointerleave={hideTooltip}
          onclick={() => onLock(leaf.data.medium)}
          onkeydown={(event) => {
            if (event.key === 'Enter' || event.key === ' ') {
              event.preventDefault();
              onLock(leaf.data.medium);
            }
          }}
          role="button"
          tabindex="0"
          aria-label={`${leaf.data.medium}: ${leaf.data.n} works, ${Number(leaf.data.pct).toFixed(1)} percent`}
        />
        <rect
          class="inner-frame"
          x={leaf.x0 + 5}
          y={leaf.y0 + 5}
          width={Math.max(0, leafWidth - 10)}
          height={Math.max(0, leafHeight - 10)}
        />
        <g class="motif" clip-path={`url(#leaf-clip-${leaf.rank})`}>
          {#each motifLines(leaf) as line}
            <line x1={line.x1} y1={line.y1} x2={line.x2} y2={line.y2} />
          {/each}
        </g>
        {#if area >= labelArea}
          <text x={leaf.x0 + 10} y={leaf.y0 + 24}>
            <tspan>{leaf.data.medium}</tspan>
            <tspan x={leaf.x0 + 10} dy="18">{Number(leaf.data.pct).toFixed(1)}%</tspan>
          </text>
        {/if}
      </g>
    {/each}
    {#if activeLeaf && annotation}
      <Annotation
        x={(activeLeaf.x0 + activeLeaf.x1) / 2}
        y={(activeLeaf.y0 + activeLeaf.y1) / 2}
        dx={annotation.dx}
        dy={annotation.dy}
        value={annotation.value}
        label={annotation.label}
        emphasis="strong"
        width={annotation.width}
      />
    {/if}
  </svg>
  <table class="sr-only">
    <caption>MoMA collection area totals</caption>
    <thead>
      <tr><th>Area</th><th>Works</th><th>Percent</th></tr>
    </thead>
    <tbody>
      {#each data as item}
        <tr><td>{item.medium}</td><td>{item.n}</td><td>{item.pct}</td></tr>
      {/each}
    </tbody>
  </table>
</figure>

<style>
  .treemap {
    margin: 0;
    width: 100%;
  }

  svg {
    width: 100%;
    height: auto;
    display: block;
    padding: var(--space-1);
    background: var(--bg-paper);
    border: 1px solid var(--rule-on-light);
  }

  .mark {
    fill: var(--seq-1);
    stroke: var(--bg-light);
    stroke-width: 1;
    cursor: pointer;
    transform-box: fill-box;
    transform-origin: center;
    animation: grow-leaf 900ms var(--ease-out) both;
    animation-delay: calc(var(--rank) * 35ms);
    transition: fill var(--duration-tooltip-in) var(--ease-out);
  }

  .mark.highlight {
    fill: var(--accent-primary);
  }

  .mark:hover,
  .mark:focus-visible {
    fill: var(--seq-2);
    outline: none;
  }

  .mark.highlight:hover,
  .mark.highlight:focus-visible {
    fill: var(--accent-primary);
  }

  .inner-frame,
  .motif {
    pointer-events: none;
  }

  .inner-frame {
    fill: none;
    stroke: color-mix(in srgb, var(--fg-on-light-strong) 20%, transparent);
    stroke-width: 1;
  }

  .motif line {
    stroke: color-mix(in srgb, var(--fg-on-light-strong) 16%, transparent);
    stroke-width: 1.2;
    stroke-linecap: round;
  }

  .leaf:has(.mark.highlight) .motif line,
  .leaf:has(.mark.highlight) .inner-frame {
    stroke: color-mix(in srgb, var(--fg-on-dark-strong) 42%, transparent);
  }

  text {
    fill: var(--fg-on-light-strong);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
    font-weight: 600;
    pointer-events: none;
  }

  tspan + tspan {
    fill: var(--fg-on-light-mute);
    font-family: var(--font-mono);
    font-weight: 500;
    font-variant-numeric: tabular-nums;
  }

  @keyframes grow-leaf {
    from {
      scale: 0;
    }
    to {
      scale: 1;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    rect {
      animation: none;
      transition: none;
    }
  }
</style>
