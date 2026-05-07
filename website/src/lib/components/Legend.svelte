<script>
  export let mode = 'categorical';
  export let items = [];
  export let minLabel = '';
  export let midLabel = '';
  export let maxLabel = '';
  export let caption = '';
  export let dark = false;
</script>

<div class="legend" class:dark aria-label={caption || 'Chart legend'}>
  {#if mode === 'sequential'}
    <div class="ramp" aria-hidden="true"></div>
    <div class="ramp-labels">
      <span>{minLabel}</span>
      {#if midLabel}<span>{midLabel}</span>{/if}
      <span>{maxLabel}</span>
    </div>
  {:else}
    <div class="chips">
      {#each items as item}
        <span class="legend-item">
          <span class="swatch" style:background={item.color}></span>
          <span>{item.label}</span>
        </span>
      {/each}
    </div>
  {/if}
  {#if caption}
    <p>{caption}</p>
  {/if}
</div>

<style>
  .legend {
    color: var(--fg-on-light-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
    line-height: var(--type-small-line);
  }

  .legend.dark {
    color: var(--fg-on-dark-mute);
  }

  .ramp {
    width: min(18rem, 100%);
    height: 0.75rem;
    background: linear-gradient(90deg, var(--seq-0), var(--seq-1), var(--seq-2), var(--seq-3), var(--seq-4));
  }

  .ramp-labels {
    display: flex;
    justify-content: space-between;
    width: min(18rem, 100%);
    margin-top: 0.25rem;
    font-family: var(--font-mono);
    font-size: var(--type-small-size);
    font-variant-numeric: tabular-nums;
  }

  .chips {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
  }

  .legend-item {
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
  }

  .swatch {
    width: 0.75rem;
    height: 0.75rem;
    border: 1px solid currentColor;
  }

  p {
    margin: var(--space-1) 0 0;
  }
</style>
