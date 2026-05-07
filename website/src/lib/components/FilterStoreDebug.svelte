<script>
  import {
    clearSelectedCountry,
    filters,
    resetFilters,
    setDecadeRange,
    setSelectedCountry,
    toggleDepartment,
    toggleRegion,
  } from '../stores/filters.js';
</script>

<aside class="filter-debug" aria-label="Filter store debug panel">
  <h2>Filter Store Debug</h2>
  <pre>{JSON.stringify({
    decadeRange: $filters.decadeRange,
    selectedCountry: $filters.selectedCountry,
    selectedDepartments: [...$filters.selectedDepartments],
    selectedRegions: [...$filters.selectedRegions],
    activeScene: $filters.activeScene,
    activeStep: $filters.activeStep,
  }, null, 2)}</pre>
  <div class="debug-actions">
    <button type="button" onclick={() => setDecadeRange([1900, 1980])}>Set 1900-1980</button>
    <button type="button" onclick={() => setSelectedCountry('USA')}>Country USA</button>
    <button type="button" onclick={clearSelectedCountry}>Clear country</button>
    <button type="button" onclick={() => toggleDepartment('Photography')}>Photography</button>
    <button type="button" onclick={() => toggleRegion('Europe')}>Europe</button>
    <button type="button" onclick={resetFilters}>Reset</button>
  </div>
</aside>

<style>
  .filter-debug {
    position: fixed;
    right: var(--space-2);
    bottom: var(--space-2);
    z-index: 1000;
    width: min(24rem, calc(100vw - var(--space-4)));
    max-height: calc(100vh - var(--space-4));
    overflow: auto;
    padding: var(--space-2);
    color: var(--fg-on-dark-strong);
    background: var(--bg-dark);
    border: 1px solid var(--fg-on-dark-mute);
    font-family: var(--font-ui);
  }

  .filter-debug h2 {
    margin-bottom: var(--space-1);
    color: var(--fg-on-dark-strong);
    font-size: var(--type-h3-size);
  }

  .filter-debug pre {
    margin: 0 0 var(--space-2);
    font-family: var(--font-mono);
    font-size: var(--type-small-size);
    white-space: pre-wrap;
  }

  .debug-actions {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
  }

  .debug-actions button {
    border: 1px solid var(--fg-on-dark-mute);
    padding: 0.375rem 0.5rem;
    color: var(--fg-on-dark-strong);
    background: transparent;
    cursor: pointer;
  }

  .debug-actions button:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }
</style>
