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
</script>

<figure class="treemap" aria-label="Treemap of MoMA collection areas by number of works">
  <svg viewBox={`0 0 ${width} ${height}`}>
    <title>Treemap of MoMA collection areas by number of works</title>
    {#each leaves as leaf}
      {@const leafWidth = leaf.x1 - leaf.x0}
      {@const leafHeight = leaf.y1 - leaf.y0}
      {@const area = leafWidth * leafHeight}
      <g class="leaf" style:--rank={leaf.rank}>
        <rect
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
    background: var(--bg-light);
  }

  rect {
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

  rect.highlight {
    fill: var(--accent-primary);
  }

  rect:hover,
  rect:focus-visible {
    fill: var(--seq-2);
    outline: none;
  }

  rect.highlight:hover,
  rect.highlight:focus-visible {
    fill: var(--accent-primary);
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
