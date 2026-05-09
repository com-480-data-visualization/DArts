<script>
  import { onDestroy, onMount } from 'svelte';
  import { geoCentroid, geoGraticule10, geoOrthographic, geoPath } from 'd3-geo';
  import { interpolate } from 'd3-interpolate';
  import { feature } from 'topojson-client';
  import { worldAtlasIdToIso3 } from '../data/worldIso3.js';
  import { filters, setSelectedCountry } from '../stores/filters.js';
  import {
    closestRotationStart,
    easeInOutCubic,
    buildIsoCounts,
    globeFillFor,
    IDLE_DEGREES_PER_MS,
    IDLE_RESUME_DELAY,
    TOP_THREE_HOLD_DELAY,
    TOP_THREE_ROTATION,
  } from '../utils/globeMotion.js';
  import './globe.css';

  let { countryByDecade = [], step = 0, active = false } = $props();

  const width = 760;
  const height = 760;

  let countries = $state([]);
  let rotation = $state([-35, -20]);
  let dragging = $state(false);
  let scripted = $state(false);
  let dragStart = null;
  let rotateStart = null;
  let pointerDownCountryIndex = null;
  let pointerMoved = false;
  let motionFrame = 0;
  let idleFrame = 0;
  let idleLast = 0;
  let idlePausedUntil = 0;
  let lastFocusedStep = -1;
  let reduceMotion = $state(false);

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
  let countByIso = $derived(buildIsoCounts(countryByDecade, range));
  let maxCount = $derived(Math.max(1, ...Object.values(countByIso)));

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

  function pauseIdle(duration = IDLE_RESUME_DELAY) {
    idlePausedUntil = performance.now() + duration;
    idleLast = 0;
  }

  function cancelMotion() {
    cancelAnimationFrame(motionFrame);
    motionFrame = 0;
    scripted = false;
  }

  function animateRotationTo(target, duration = 900, holdDelay = 0) {
    pauseIdle(duration + holdDelay);
    cancelMotion();
    if (reduceMotion) {
      rotation = target;
      return;
    }
    scripted = true;
    const start = closestRotationStart(rotation, target);
    const interp = interpolate(start, target);
    const started = performance.now();
    const tick = (now) => {
      const t = Math.min(1, (now - started) / duration);
      rotation = interp(easeInOutCubic(t));
      if (t < 1) {
        motionFrame = requestAnimationFrame(tick);
      } else {
        rotation = target;
        scripted = false;
        motionFrame = 0;
      }
    };
    motionFrame = requestAnimationFrame(tick);
  }

  function startIdleLoop() {
    if (idleFrame || reduceMotion) return;
    idleFrame = requestAnimationFrame(idleTick);
  }

  function stopIdleLoop() {
    cancelAnimationFrame(idleFrame);
    idleFrame = 0;
    idleLast = 0;
  }

  function idleTick(now) {
    idleFrame = requestAnimationFrame(idleTick);
    if (!active || reduceMotion) return;
    const elapsed = idleLast ? Math.min(40, now - idleLast) : 0;
    idleLast = now;
    if (!elapsed || dragging || scripted || selectedCountry || now < idlePausedUntil) return;
    rotation = [rotation[0] + elapsed * IDLE_DEGREES_PER_MS, rotation[1]];
  }

  function focusTopThreeCountries() {
    animateRotationTo(TOP_THREE_ROTATION, 900, TOP_THREE_HOLD_DELAY);
  }

  function centerCountry(country) {
    const iso3 = worldAtlasIdToIso3[String(country.id).padStart(3, '0')];
    if (!iso3 || !countByIso[iso3]) return;
    setSelectedCountry(iso3);
    const [lon, lat] = geoCentroid(country);
    const target = [-lon, -lat];
    animateRotationTo(target, 900, IDLE_RESUME_DELAY);
  }

  function onPointerDown(event) {
    cancelMotion();
    pauseIdle();
    dragging = true;
    dragStart = [event.clientX, event.clientY];
    rotateStart = rotation;
    pointerMoved = false;
    pointerDownCountryIndex = event.target?.dataset?.countryIndex ?? null;
    event.currentTarget.setPointerCapture(event.pointerId);
  }

  function onPointerMove(event) {
    if (!dragging || !dragStart || !rotateStart) return;
    const dx = event.clientX - dragStart[0];
    const dy = event.clientY - dragStart[1];
    if (Math.hypot(dx, dy) > 4) pointerMoved = true;
    rotation = [rotateStart[0] + dx * 0.35, Math.max(-65, Math.min(65, rotateStart[1] - dy * 0.35))];
  }

  function onPointerUp(event) {
    const countryIndex = pointerDownCountryIndex;
    const shouldSelect = dragging && !pointerMoved && countryIndex !== null;
    dragging = false;
    pointerDownCountryIndex = null;
    if (event.currentTarget.hasPointerCapture?.(event.pointerId))
      event.currentTarget.releasePointerCapture(event.pointerId);
    pauseIdle();
    if (shouldSelect) centerCountry(countries[Number(countryIndex)]);
  }

  $effect(() => {
    if (active && !reduceMotion) {
      startIdleLoop();
    } else {
      stopIdleLoop();
    }
  });

  $effect(() => {
    if (active && step === 2 && lastFocusedStep !== 2 && !selectedCountry) focusTopThreeCountries();
    lastFocusedStep = step;
  });

  onMount(async () => {
    reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const response = await fetch('./topology/world-110m.json');
    const topology = await response.json();
    countries = feature(topology, topology.objects.countries).features;
  });

  onDestroy(() => {
    cancelMotion();
    stopIdleLoop();
  });
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
      {#each countries as country, index}
        {@const iso3 = worldAtlasIdToIso3[String(country.id).padStart(3, '0')]}
        <path
          d={path(country)}
          data-country-index={index}
          data-iso3={iso3}
          fill={globeFillFor(iso3, countByIso[iso3] || 0, maxCount, step)}
          class:selected={selectedCountry === iso3}
          class:clickable={Boolean(iso3 && countByIso[iso3])}
          onpointermove={(event) => showTooltip(event, country)}
          onpointerleave={hideTooltip}
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
