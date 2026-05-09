<script>
  import { line, scaleLinear } from 'd3';
  import Annotation from '../components/Annotation.svelte';
  import { filters } from '../stores/filters.js';

  export let data = [];
  export let annotations = [];

  const width = 760;
  const height = 420;
  const margin = { top: 24, right: 32, bottom: 48, left: 56 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  const decades = Array.from({ length: 17 }, (_, i) => 1860 + i * 10);

  $: range = $filters.decadeRange;
  $: x = scaleLinear().domain([1860, 2020]).range([0, innerWidth]);
  $: y = scaleLinear().domain([0, 0.6]).range([innerHeight, 0]);
  $: pointByDecade = new Map(data.map((d) => [d.decade, d]));
  $: pathD = line()
    .x((d) => x(d.decade))
    .y((d) => y(d.femaleShare))(data);
  $: areaD = `${pathD || ''} L ${x(data.at(-1)?.decade ?? 2020)} ${innerHeight} L ${x(data[0]?.decade ?? 1860)} ${innerHeight} Z`;
  $: plottedAnnotations = annotations.map(positionAnnotation).filter(Boolean);

  function positionAnnotation(note) {
    if (Number.isFinite(note.x) && Number.isFinite(note.y)) return note;
    const point = pointByDecade.get(note.decade);
    const share = Number.isFinite(note.femaleShare) ? note.femaleShare : point?.femaleShare;
    if (!Number.isFinite(note.decade) || !Number.isFinite(share)) return null;
    return { ...note, x: x(note.decade), y: y(share) };
  }

  function showTooltip(event, d) {
    window.dispatchEvent(
      new CustomEvent('darts:tooltip', {
        detail: {
          x: event.clientX,
          y: event.clientY,
          content: `<strong>${d.decade}s</strong><br><span class="num">${(d.femaleShare * 100).toFixed(1)}%</span> female-credited<br><span class="num">n=${d.n.toLocaleString()}</span>${d.n < 30 ? '<br>small sample' : ''}`,
        },
      }),
    );
  }

  function hideTooltip() {
    window.dispatchEvent(new CustomEvent('darts:tooltip-hide'));
  }
</script>

<figure class="line-chart" aria-label="Female-credited share by decade from 1860 to 2020">
  <svg viewBox={`0 0 ${width} ${height}`}>
    <title>Female-credited share by decade</title>
    <g transform={`translate(${margin.left},${margin.top})`}>
      <g class="grid">
        {#each [0, 0.25, 0.5, 0.6] as tick}
          <line x1="0" x2={innerWidth} y1={y(tick)} y2={y(tick)} />
          <text x="-10" y={y(tick)}>{(tick * 100).toFixed(0)}%</text>
        {/each}
      </g>
      <line class="parity" x1="0" x2={innerWidth} y1={y(0.5)} y2={y(0.5)} />
      <text class="parity-label" x={innerWidth - 48} y={y(0.5) - 8}>parity</text>
      <rect
        class="range-band"
        x={x(range[0])}
        y="0"
        width={Math.max(1, x(range[1]) - x(range[0]))}
        height={innerHeight}
      />
      <path class="area" d={areaD} />
      <path class="series draw" d={pathD} />
      {#each plottedAnnotations as note}
        <Annotation {...note} />
      {/each}
      {#each data as d}
        <circle
          cx={x(d.decade)}
          cy={y(d.femaleShare)}
          r="4"
          class:small={d.n < 30}
          onpointermove={(event) => showTooltip(event, d)}
          onpointerleave={hideTooltip}
          role="img"
          aria-label={`${d.decade}s: ${(d.femaleShare * 100).toFixed(1)} percent female-credited, n ${d.n}`}
        />
      {/each}
      {#each decades.filter((d) => d % 20 === 0) as decade}
        <text class="x-label" x={x(decade)} y={innerHeight + 30}>{decade}</text>
      {/each}
      <text class="axis-title y" x={-innerHeight / 2} y="-42">female-credited share</text>
      <text class="axis-title x" x={innerWidth / 2} y={innerHeight + 46}>artwork decade</text>
    </g>
  </svg>
  <table class="sr-only">
    <caption>Female-credited share by decade</caption>
    <thead><tr><th>Decade</th><th>Female percent</th><th>Credited works</th></tr></thead>
    <tbody>
      {#each data as d}
        <tr><td>{d.decade}</td><td>{(d.femaleShare * 100).toFixed(1)}</td><td>{d.n}</td></tr>
      {/each}
    </tbody>
  </table>
</figure>

<style>
  .line-chart {
    margin: 0;
    padding: var(--space-1);
    background: var(--bg-paper);
    border: 1px solid var(--rule-on-light);
  }

  svg {
    width: 100%;
    height: auto;
    display: block;
    background: var(--bg-paper);
  }

  .grid line {
    stroke: var(--rule-on-light);
    stroke-width: 1;
    opacity: 0.45;
  }

  .grid text,
  .x-label,
  .axis-title,
  .parity-label {
    fill: var(--fg-on-light-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
  }

  .grid text {
    text-anchor: end;
    dominant-baseline: middle;
  }

  .x-label {
    text-anchor: middle;
  }

  .axis-title {
    text-anchor: middle;
  }

  .axis-title.y {
    rotate: -90deg;
  }

  .parity {
    stroke: var(--fg-on-light-mute);
    stroke-dasharray: 4 4;
    stroke-width: 1;
  }

  .range-band {
    fill: var(--accent-primary);
    opacity: 0.06;
  }

  .area {
    fill: var(--gender-female);
    opacity: 0.12;
  }

  .series {
    fill: none;
    stroke: var(--gender-female);
    stroke-width: 3;
    stroke-linejoin: round;
    stroke-linecap: round;
  }

  .draw {
    stroke-dasharray: 1200;
    stroke-dashoffset: 1200;
    animation: draw-line var(--duration-draw) var(--ease-out) forwards;
  }

  circle {
    fill: var(--bg-paper);
    stroke: var(--gender-female);
    stroke-width: 2;
    transition:
      r var(--duration-tooltip-in) var(--ease-out),
      fill var(--duration-tooltip-in) var(--ease-out);
  }

  circle:hover,
  circle:focus-visible {
    r: 6;
    fill: var(--gender-female);
  }

  circle.small {
    opacity: 0.35;
  }

  @keyframes draw-line {
    to {
      stroke-dashoffset: 0;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .draw {
      animation: none;
      stroke-dashoffset: 0;
    }
  }
</style>
