<script>
  let { timelineData, selectedDecade = $bindable(null) } = $props();

  let decades = $derived(
    timelineData
      .map(d => d.decade)
      .sort((a, b) => a - b)
      .filter(d => d >= 1860 && d <= 2020)
  );

  let minIdx = $state(0);
  let maxIdx = $state(0);

  // Initialize maxIdx when decades load
  $effect(() => {
    if (decades.length > 0 && maxIdx === 0) {
      maxIdx = decades.length - 1;
    }
  });

  let rangeActive = $derived(minIdx !== 0 || maxIdx !== decades.length - 1);

  // Expose the selected range as selectedDecade = { min, max } or null
  $effect(() => {
    if (decades.length === 0) return;
    if (!rangeActive) {
      selectedDecade = null;
    } else {
      selectedDecade = { min: decades[minIdx], max: decades[maxIdx] };
    }
  });

  let trackEl = $state(null);
  let dragging = $state(null); // 'min' | 'max' | null

  function pctFromIdx(idx) {
    return decades.length > 1 ? (idx / (decades.length - 1)) * 100 : 0;
  }

  function idxFromPct(pct) {
    const raw = (pct / 100) * (decades.length - 1);
    return Math.round(Math.max(0, Math.min(decades.length - 1, raw)));
  }

  function getPctFromEvent(e) {
    if (!trackEl) return 0;
    const rect = trackEl.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    return Math.max(0, Math.min(100, ((clientX - rect.left) / rect.width) * 100));
  }

  function onPointerDown(handle, e) {
    e.preventDefault();
    dragging = handle;
    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerup', onPointerUp);
  }

  function onPointerMove(e) {
    if (!dragging) return;
    const pct = getPctFromEvent(e);
    const idx = idxFromPct(pct);
    if (dragging === 'min') {
      minIdx = Math.min(idx, maxIdx);
    } else {
      maxIdx = Math.max(idx, minIdx);
    }
  }

  function onPointerUp() {
    dragging = null;
    window.removeEventListener('pointermove', onPointerMove);
    window.removeEventListener('pointerup', onPointerUp);
  }

  function reset() {
    minIdx = 0;
    maxIdx = decades.length - 1;
  }
</script>

<div class="range-slider">
  <div class="slider-header">
    <div class="slider-label">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
      </svg>
      <span>Filter by period</span>
    </div>
    <div class="slider-value">
      {#if rangeActive}
        <span class="range-display">{decades[minIdx]}s – {decades[maxIdx]}s</span>
        <button class="reset-btn" onclick={reset}>Show all</button>
      {:else}
        <span class="all-label">All periods</span>
      {/if}
    </div>
  </div>

  {#if decades.length > 0}
    <div class="track-wrapper">
      <div class="track" bind:this={trackEl}>
        <!-- Inactive track background -->
        <div class="track-bg"></div>

        <!-- Active range fill -->
        <div
          class="track-fill"
          style="left: {pctFromIdx(minIdx)}%; right: {100 - pctFromIdx(maxIdx)}%"
        ></div>

        <!-- Tick marks -->
        {#each decades as decade, i}
          <div
            class="tick"
            class:in-range={i >= minIdx && i <= maxIdx}
            style="left: {pctFromIdx(i)}%"
          >
            <div class="tick-mark"></div>
            {#if i % 3 === 0 || i === decades.length - 1}
              <span class="tick-label">{decade}</span>
            {/if}
          </div>
        {/each}

        <!-- Min handle -->
        <div
          class="handle handle-min"
          class:active={dragging === 'min'}
          style="left: {pctFromIdx(minIdx)}%"
          onpointerdown={(e) => onPointerDown('min', e)}
          role="slider"
          aria-label="Start decade"
          aria-valuemin={decades[0]}
          aria-valuemax={decades[maxIdx]}
          aria-valuenow={decades[minIdx]}
          tabindex="0"
        >
          <div class="handle-knob"></div>
          <div class="handle-tooltip">{decades[minIdx]}s</div>
        </div>

        <!-- Max handle -->
        <div
          class="handle handle-max"
          class:active={dragging === 'max'}
          style="left: {pctFromIdx(maxIdx)}%"
          onpointerdown={(e) => onPointerDown('max', e)}
          role="slider"
          aria-label="End decade"
          aria-valuemin={decades[minIdx]}
          aria-valuemax={decades[decades.length - 1]}
          aria-valuenow={decades[maxIdx]}
          tabindex="0"
        >
          <div class="handle-knob"></div>
          <div class="handle-tooltip">{decades[maxIdx]}s</div>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .range-slider {
    background: var(--color-surface);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem 2.5rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--color-border);
    position: sticky;
    top: 1rem;
    z-index: 50;
  }

  .slider-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .slider-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--color-text-muted);
  }

  .slider-value {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .range-display {
    font-family: var(--font-heading);
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-primary);
  }

  .reset-btn {
    background: none;
    border: 1px solid var(--color-border);
    padding: 0.25rem 0.8rem;
    border-radius: 100px;
    cursor: pointer;
    font-size: 0.75rem;
    font-family: var(--font-body);
    font-weight: 500;
    color: var(--color-text-muted);
    transition: all 0.2s;
  }
  .reset-btn:hover {
    border-color: var(--color-primary);
    color: var(--color-primary);
  }

  .all-label {
    color: var(--color-text-light);
    font-size: 0.82rem;
    font-style: italic;
  }

  .track-wrapper {
    padding: 0 14px;
  }

  .track {
    position: relative;
    height: 6px;
    margin-top: 0.5rem;
    touch-action: none;
    user-select: none;
  }

  .track-bg {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: var(--color-surface-alt);
    border-radius: 3px;
    border: 1px solid var(--color-border);
  }

  .track-fill {
    position: absolute;
    top: 0;
    height: 6px;
    background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
    border-radius: 3px;
    z-index: 1;
  }

  .tick {
    position: absolute;
    top: 0;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 2;
    pointer-events: none;
  }

  .tick-mark {
    width: 2px;
    height: 10px;
    background: var(--color-border);
    border-radius: 1px;
    margin-top: 10px;
  }
  .tick.in-range .tick-mark {
    background: var(--color-primary-light);
    opacity: 0.5;
  }

  .tick-label {
    font-size: 0.65rem;
    color: var(--color-text-light);
    margin-top: 4px;
    white-space: nowrap;
  }
  .tick.in-range .tick-label {
    color: var(--color-text-muted);
    font-weight: 500;
  }

  .handle {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
    cursor: grab;
    touch-action: none;
  }
  .handle.active {
    cursor: grabbing;
    z-index: 11;
  }

  .handle-knob {
    width: 22px;
    height: 22px;
    background: var(--color-surface);
    border: 3px solid var(--color-primary);
    border-radius: 50%;
    box-shadow: 0 2px 6px rgba(193,68,14,0.2);
    transition: transform 0.15s, box-shadow 0.15s;
  }
  .handle:hover .handle-knob,
  .handle.active .handle-knob {
    transform: scale(1.15);
    box-shadow: 0 3px 10px rgba(193,68,14,0.3);
  }

  .handle-tooltip {
    position: absolute;
    bottom: calc(100% + 6px);
    left: 50%;
    transform: translateX(-50%);
    background: var(--color-text);
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    white-space: nowrap;
    opacity: 0;
    transition: opacity 0.15s;
    pointer-events: none;
  }
  .handle-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 4px solid transparent;
    border-top-color: var(--color-text);
  }
  .handle:hover .handle-tooltip,
  .handle.active .handle-tooltip {
    opacity: 1;
  }
</style>
