<script>
  import { onDestroy } from 'svelte';
  import { DECADE_MAX, DECADE_MIN, filters, setDecadeRange, syncToHash } from '../stores/filters.js';

  export let timeline = [];
  export let ariaLabel = 'Filter by decade range';

  const STEP = 10;
  const LARGE_STEP = 50;
  const MIN_SPAN = 10;
  const decades = Array.from({ length: (DECADE_MAX - DECADE_MIN) / STEP + 1 }, (_, index) => DECADE_MIN + index * STEP);

  let track;
  let dragging = null;

  $: range = $filters.decadeRange;
  $: minDecade = range[0];
  $: maxDecade = range[1];
  $: countByDecade = new Map(timeline.map((d) => [Number(d.decade), Number(d.n ?? d.count ?? 0)]));
  $: maxCount = Math.max(1, ...decades.map((decade) => countByDecade.get(decade) ?? 0));

  function percent(decade) {
    return ((decade - DECADE_MIN) / (DECADE_MAX - DECADE_MIN)) * 100;
  }

  function decadeFromClientX(clientX) {
    if (!track) return DECADE_MIN;
    const rect = track.getBoundingClientRect();
    const raw = (clientX - rect.left) / rect.width;
    const clamped = Math.min(1, Math.max(0, raw));
    return Math.round((DECADE_MIN + clamped * (DECADE_MAX - DECADE_MIN)) / STEP) * STEP;
  }

  function updateThumb(thumb, decade) {
    if (thumb === 'min') {
      setDecadeRange([Math.min(decade, maxDecade - MIN_SPAN), maxDecade]);
    } else {
      setDecadeRange([minDecade, Math.max(decade, minDecade + MIN_SPAN)]);
    }
  }

  function onPointerMove(event) {
    if (!dragging) return;
    updateThumb(dragging, decadeFromClientX(event.clientX));
  }

  function stopDragging() {
    dragging = null;
    window.removeEventListener('pointermove', onPointerMove);
    window.removeEventListener('pointerup', stopDragging);
    syncToHash();
  }

  function startDragging(thumb, event) {
    event.preventDefault();
    dragging = thumb;
    updateThumb(thumb, decadeFromClientX(event.clientX));
    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerup', stopDragging);
  }

  function onKey(thumb, event) {
    const step = event.shiftKey ? LARGE_STEP : STEP;
    let next = thumb === 'min' ? minDecade : maxDecade;
    if (event.key === 'ArrowLeft') next -= step;
    else if (event.key === 'ArrowRight') next += step;
    else if (event.key === 'Home') next = thumb === 'min' ? DECADE_MIN : minDecade + MIN_SPAN;
    else if (event.key === 'End') next = thumb === 'min' ? maxDecade - MIN_SPAN : DECADE_MAX;
    else return;
    event.preventDefault();
    updateThumb(thumb, next);
    syncToHash();
  }

  onDestroy(() => {
    window.removeEventListener('pointermove', onPointerMove);
    window.removeEventListener('pointerup', stopDragging);
  });
</script>

<div class="decade-slider" aria-label={ariaLabel}>
  <div class="slider-values type-mono">
    <span>{minDecade}</span>
    <span>{maxDecade}</span>
  </div>
  <div class="sparkline" aria-hidden="true">
    {#each decades as decade}
      <span style:height={`${((countByDecade.get(decade) ?? 0) / maxCount) * 100}%`}></span>
    {/each}
  </div>
  <div class="track" bind:this={track}>
    <div class="track-base"></div>
    <div class="track-fill" style:left={`${percent(minDecade)}%`} style:right={`${100 - percent(maxDecade)}%`}></div>
    {#each decades as decade}
      <span
        class="tick"
        class:major={(decade - DECADE_MIN) % 40 === 0}
        style:left={`${percent(decade)}%`}
      >
        {#if (decade - DECADE_MIN) % 40 === 0}
          <span>{decade}</span>
        {/if}
      </span>
    {/each}
    <button
      type="button"
      class="thumb"
      class:active={dragging === 'min'}
      style:left={`${percent(minDecade)}%`}
      role="slider"
      aria-label="Start decade"
      aria-valuemin={DECADE_MIN}
      aria-valuemax={maxDecade - MIN_SPAN}
      aria-valuenow={minDecade}
      onpointerdown={(event) => startDragging('min', event)}
      onkeydown={(event) => onKey('min', event)}
    >
      <span>{minDecade}</span>
    </button>
    <button
      type="button"
      class="thumb"
      class:active={dragging === 'max'}
      style:left={`${percent(maxDecade)}%`}
      role="slider"
      aria-label="End decade"
      aria-valuemin={minDecade + MIN_SPAN}
      aria-valuemax={DECADE_MAX}
      aria-valuenow={maxDecade}
      onpointerdown={(event) => startDragging('max', event)}
      onkeydown={(event) => onKey('max', event)}
    >
      <span>{maxDecade}</span>
    </button>
  </div>
</div>

<style>
  .decade-slider {
    display: grid;
    gap: var(--space-1);
    width: 100%;
    font-family: var(--font-ui);
  }

  .slider-values {
    display: flex;
    justify-content: space-between;
    color: var(--fg-on-light-strong);
  }

  .sparkline {
    display: flex;
    align-items: end;
    height: 2rem;
    gap: 0.125rem;
  }

  .sparkline span {
    flex: 1;
    min-height: 0.125rem;
    background: color-mix(in srgb, var(--fg-on-light-mute) 30%, transparent);
  }

  .track {
    position: relative;
    height: 3rem;
    touch-action: none;
  }

  .track-base,
  .track-fill {
    position: absolute;
    top: 0.75rem;
    height: 0.125rem;
  }

  .track-base {
    inset-inline: 0;
    background: var(--rule-on-light);
  }

  .track-fill {
    background: var(--accent-primary);
  }

  .tick {
    position: absolute;
    top: 0.5rem;
    width: 1px;
    height: 0.625rem;
    background: var(--rule-on-light);
  }

  .tick.major {
    height: 0.875rem;
  }

  .tick span {
    position: absolute;
    top: 1rem;
    left: 50%;
    translate: -50% 0;
    color: var(--fg-on-light-mute);
    font-family: var(--font-mono);
    font-size: 0.6875rem;
    font-variant-numeric: tabular-nums;
  }

  .thumb {
    position: absolute;
    top: 0.75rem;
    width: 1rem;
    height: 1rem;
    border: 2px solid var(--accent-primary);
    background: var(--bg-paper);
    translate: -50% -45%;
    cursor: grab;
  }

  .thumb.active {
    cursor: grabbing;
  }

  .thumb span {
    position: absolute;
    bottom: calc(100% + 0.25rem);
    left: 50%;
    translate: -50% 0;
    padding: 0 0.125rem;
    color: var(--fg-on-light-strong);
    background: var(--bg-paper);
    font-family: var(--font-mono);
    font-size: var(--type-small-size);
    font-variant-numeric: tabular-nums;
  }
</style>
