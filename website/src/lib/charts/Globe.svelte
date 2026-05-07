<script>
  import { onDestroy, onMount } from 'svelte';
  import { geoCentroid, geoGraticule10, geoOrthographic, geoPath } from 'd3-geo';
  import { interpolate } from 'd3-interpolate';
  import { feature } from 'topojson-client';
  import { worldAtlasIdToIso3 } from '../data/worldIso3.js';
  import { filters, setSelectedCountry } from '../stores/filters.js';

  let { countryByDecade = [], step = 0 } = $props();

  const width = 760;
  const height = 760;
  const topThree = new Set(['USA', 'FRA', 'DEU']);

  let countries = $state([]);
  let rotation = $state([-35, -20]);
  let dragging = $state(false);
  let dragStart = null;
  let rotateStart = null;
  let frame = 0;
  let reduceMotion = false;

  let projection = $derived(
    geoOrthographic()
      .scale(350)
      .translate([width / 2, height / 2])
      .clipAngle(90)
      .rotate(rotation),
  );
  let path = $derived(geoPath(projection));
  let graticulePath = $derived(path(geoGraticule10()));
  let range = $derived($filters.decadeRange);
  let selectedCountry = $derived($filters.selectedCountry);
  let countByIso = $derived(buildCounts(countryByDecade, range));
  let maxCount = $derived(Math.max(1, ...Object.values(countByIso)));

  function buildCounts(rows, decadeRange) {
    const counts = {};
    for (const row of rows) {
      if (row.decade === null || row.decade < decadeRange[0] || row.decade > decadeRange[1]) continue;
      counts[row.iso3] = (counts[row.iso3] || 0) + row.n;
    }
    return counts;
  }

  function fillFor(iso3) {
    const n = countByIso[iso3] || 0;
    if (n === 0) return 'transparent';
    if (step >= 2 && topThree.has(iso3)) return 'var(--accent-primary)';
    if (step === 0) return 'var(--seq-0)';
    const bucket = Math.min(4, Math.max(0, Math.floor((Math.log10(n) / Math.log10(maxCount)) * 4)));
    return `var(--seq-${bucket})`;
  }

  function showTooltip(event, country) {
    const iso3 = worldAtlasIdToIso3[String(country.id).padStart(3, '0')];
    const count = countByIso[iso3] || 0;
    if (!iso3 || count === 0) return;
    window.dispatchEvent(
      new CustomEvent('darts:tooltip', {
        detail: {
          x: event.clientX,
          y: event.clientY,
          content: `<strong>${country.properties.name}</strong><br><span class="num">${count.toLocaleString()}</span> credited works`,
        },
      }),
    );
  }

  function hideTooltip() {
    window.dispatchEvent(new CustomEvent('darts:tooltip-hide'));
  }

  function ease(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function centerCountry(country) {
    const iso3 = worldAtlasIdToIso3[String(country.id).padStart(3, '0')];
    if (!iso3 || !countByIso[iso3]) return;
    setSelectedCountry(iso3);
    const [lon, lat] = geoCentroid(country);
    const target = [-lon, -lat];
    if (reduceMotion) {
      rotation = target;
      return;
    }
    const start = rotation;
    const interp = interpolate(start, target);
    const started = performance.now();
    cancelAnimationFrame(frame);
    const tick = (now) => {
      const t = Math.min(1, (now - started) / 900);
      rotation = interp(ease(t));
      if (t < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
  }

  function onPointerDown(event) {
    dragging = true;
    dragStart = [event.clientX, event.clientY];
    rotateStart = rotation;
    event.currentTarget.setPointerCapture(event.pointerId);
  }

  function onPointerMove(event) {
    if (!dragging || !dragStart || !rotateStart) return;
    const dx = event.clientX - dragStart[0];
    const dy = event.clientY - dragStart[1];
    rotation = [rotateStart[0] + dx * 0.35, Math.max(-65, Math.min(65, rotateStart[1] - dy * 0.35))];
  }

  function onPointerUp() {
    dragging = false;
  }

  onMount(async () => {
    reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const response = await fetch('./topology/world-110m.json');
    const topology = await response.json();
    countries = feature(topology, topology.objects.countries).features;
  });

  onDestroy(() => cancelAnimationFrame(frame));
</script>

<figure class="globe-figure" aria-label="Orthographic globe showing credited works by artist country">
  <svg viewBox={`0 0 ${width} ${height}`}>
    <title>Orthographic globe of credited works by artist country</title>
    <defs>
      <filter id="globe-rim" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur" />
        <feOffset in="blur" dx="0" dy="0" result="offset" />
        <feMerge>
          <feMergeNode in="offset" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>
    <circle class="sphere" cx={width / 2} cy={height / 2} r="350" filter="url(#globe-rim)" />
    <path class="graticule" d={graticulePath} />
    <g
      class="countries"
      class:dragging
      role="application"
      aria-label="Drag to rotate the globe"
      onpointerdown={onPointerDown}
      onpointermove={onPointerMove}
      onpointerup={onPointerUp}
      onpointercancel={onPointerUp}
    >
      {#each countries as country}
        {@const iso3 = worldAtlasIdToIso3[String(country.id).padStart(3, '0')]}
        <path
          d={path(country)}
          fill={fillFor(iso3)}
          class:selected={selectedCountry === iso3}
          class:clickable={Boolean(iso3 && countByIso[iso3])}
          onpointermove={(event) => showTooltip(event, country)}
          onpointerleave={hideTooltip}
          onclick={() => centerCountry(country)}
          onkeydown={(event) => {
            if (event.key === 'Enter' || event.key === ' ') {
              event.preventDefault();
              centerCountry(country);
            }
          }}
          role="button"
          tabindex={iso3 && countByIso[iso3] ? 0 : -1}
          aria-label={`${country.properties.name}: ${(countByIso[iso3] || 0).toLocaleString()} credited works`}
          aria-disabled={!iso3 || !countByIso[iso3]}
        />
      {/each}
    </g>
  </svg>
</figure>

<style>
  .globe-figure {
    margin: 0;
    width: min(90vh, 100%);
  }

  svg {
    display: block;
    width: 100%;
    height: auto;
  }

  .sphere {
    fill: var(--bg-dark);
    stroke: var(--fg-on-dark-mute);
    stroke-width: 0.5;
    opacity: 0.9;
  }

  .graticule {
    fill: none;
    stroke: var(--fg-on-dark-mute);
    stroke-width: 0.35;
    opacity: 0.35;
    pointer-events: none;
  }

  .countries {
    cursor: grab;
  }

  .countries.dragging {
    cursor: grabbing;
  }

  path {
    stroke: var(--bg-dark);
    stroke-width: 0.35;
    transition:
      fill 450ms var(--ease-inout),
      stroke 180ms var(--ease-out);
  }

  path.clickable {
    cursor: pointer;
  }

  path.clickable:hover,
  path.selected {
    stroke: var(--fg-on-dark-strong);
    stroke-width: 1.2;
  }

  @media (prefers-reduced-motion: reduce) {
    path {
      transition: none;
    }
  }
</style>
