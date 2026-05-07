<script>
  export let label;
  export let value = '';
  export let removable = true;
  export let dark = false;
  export let onRemove = () => {};
</script>

<span class="filter-chip" class:dark>
  <span>{label}{value ? `: ${value}` : ''}</span>
  {#if removable}
    <button type="button" aria-label={`Remove ${label}`} onclick={onRemove}>x</button>
  {/if}
</span>

<style>
  .filter-chip {
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
    min-height: 2rem;
    padding: 0 var(--space-1);
    color: var(--fg-on-light-strong);
    background: var(--bg-paper);
    border: 1px solid var(--rule-on-light);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
    line-height: var(--type-small-line);
  }

  .filter-chip.dark {
    color: var(--fg-on-dark-strong);
    background: transparent;
    border-color: var(--fg-on-dark-mute);
  }

  button {
    display: inline-grid;
    width: 1.5rem;
    height: 1.5rem;
    place-items: center;
    border: 0;
    color: currentColor;
    background: transparent;
    cursor: pointer;
  }

  button:hover {
    color: var(--accent-primary);
  }
</style>
