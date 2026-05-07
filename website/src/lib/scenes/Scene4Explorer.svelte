<script>
  import { clearSelectedCountry, filters, resetFilters, toggleDepartment, toggleRegion } from '../stores/filters.js';
  import DecadeSlider from '../components/DecadeSlider.svelte';
  import FilterChip from '../components/FilterChip.svelte';
  import Legend from '../components/Legend.svelte';
  import SceneTitle from '../components/SceneTitle.svelte';
  import MediumExplorer from '../charts/MediumExplorer.svelte';

  let { data = [], countrySummary = [], timeline = [] } = $props();

  const regions = [
    'North America',
    'Latin America & Caribbean',
    'Europe',
    'Africa',
    'Western & Central Asia',
    'East Asia',
    'South & Southeast Asia',
    'Oceania',
  ];
  const genderLegend = [
    { label: 'female', color: 'var(--gender-female)' },
    { label: 'male', color: 'var(--gender-male)' },
    { label: 'non-binary', color: 'var(--gender-nonbinary)' },
    { label: 'unknown', color: 'var(--gender-unknown)' },
  ];

  let departments = $derived([...new Set(data.map((d) => d.department))].sort());
  let countryName = $derived(
    countrySummary.find((d) => d.iso3 === $filters.selectedCountry)?.country_name ?? $filters.selectedCountry,
  );
</script>

<section class="scene-explorer" aria-labelledby="scene-4-title">
  <div class="inner">
    <SceneTitle
      kicker="Scene 4"
      title="Diversity isn't evenly distributed across mediums."
      subline="Each panel uses two 100% stacked bars: gender first, region second. Length is the quantitative channel."
    />
    <div class="filter-bar" aria-label="Explorer filters">
      <DecadeSlider {timeline} ariaLabel="Filter medium explorer by decade range" />
      <div class="chip-row">
        {#each departments as department}
          <button
            type="button"
            class:active={$filters.selectedDepartments.has(department)}
            onclick={() => toggleDepartment(department)}>{department}</button
          >
        {/each}
      </div>
      <div class="chip-row">
        {#each regions as region}
          <button type="button" class:active={$filters.selectedRegions.has(region)} onclick={() => toggleRegion(region)}
            >{region}</button
          >
        {/each}
      </div>
      <div class="applied">
        {#if $filters.selectedCountry}
          <FilterChip label="Country" value={countryName} onRemove={clearSelectedCountry} />
        {/if}
        <button type="button" class="reset" onclick={resetFilters}>Reset filters</button>
      </div>
    </div>
    <Legend mode="categorical" items={genderLegend} caption="Unknown gender is retained as its own bucket." />
    <MediumExplorer {data} />
  </div>
</section>

<style>
  .scene-explorer {
    background: var(--bg-light);
    color: var(--fg-on-light-strong);
  }

  .inner {
    width: min(var(--max-content), calc(100% - var(--space-4)));
    margin: 0 auto;
    padding: var(--space-10) 0;
  }

  .filter-bar {
    position: sticky;
    top: 0;
    z-index: 10;
    display: grid;
    gap: var(--space-2);
    margin: var(--space-4) 0 var(--space-3);
    padding: var(--space-2);
    background: color-mix(in srgb, var(--bg-light) 92%, transparent);
    border: 1px solid var(--rule-on-light);
    backdrop-filter: blur(8px);
  }

  .chip-row,
  .applied {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
  }

  button {
    border: 1px solid var(--rule-on-light);
    padding: 0.375rem 0.5rem;
    color: var(--fg-on-light-strong);
    background: var(--bg-paper);
    cursor: pointer;
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
  }

  button:hover,
  button.active {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .reset {
    margin-left: auto;
  }
</style>
