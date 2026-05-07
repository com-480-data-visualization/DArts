<script>
  import { filters, clearSelectedCountry } from '../stores/filters.js';
  import DecadeSlider from '../components/DecadeSlider.svelte';
  import FilterChip from '../components/FilterChip.svelte';
  import SceneTitle from '../components/SceneTitle.svelte';
  import ScrollStep from '../components/ScrollStep.svelte';
  import LineChart from '../charts/LineChart.svelte';
  import SmallMultiplesGender from '../charts/SmallMultiplesGender.svelte';

  let {
    genderByDecade = [],
    genderByDepartment = [],
    genderByCountry = [],
    countrySummary = [],
    timeline = [],
  } = $props();

  let step = $derived($filters.activeScene === 3 ? $filters.activeStep : 0);
  let selectedCountry = $derived($filters.selectedCountry);
  let countryName = $derived(countrySummary.find((d) => d.iso3 === selectedCountry)?.country_name ?? selectedCountry);
  let countryRows = $derived(selectedCountry ? genderByCountry.filter((d) => d.iso3 === selectedCountry) : []);
  let countryN = $derived(countryRows.reduce((sum, d) => sum + d.n, 0));
  let useCountry = $derived(selectedCountry && countryN >= 100);
  let lineRows = $derived(useCountry ? countryRows : genderByDecade);
  let lineData = $derived(toLineData(lineRows));
  let latest = $derived([...lineData].reverse().find((d) => d.n > 0) ?? { femaleShare: 0, decade: 2020, n: 0 });
  let annotations = $derived([
    { x: 210, y: 80, dx: -110, dy: -35, value: '1910s', label: 'brief opening in the early collection.', width: 180 },
    { x: 300, y: 108, dx: -80, dy: 58, value: '1930s', label: 'another spike, then a long plateau.', width: 185 },
    { x: 535, y: 170, dx: 48, dy: -72, value: '1980s', label: 'sustained rise begins.', width: 165 },
    { x: 685, y: 112, dx: -150, dy: -82, value: `${(latest.femaleShare * 100).toFixed(0)}%`, label: `in the ${latest.decade}s.`, width: 150 },
  ]);

  function toLineData(rows) {
    const grouped = new Map();
    for (const row of rows) {
      if (row.decade === null) continue;
      const item = grouped.get(row.decade) ?? { decade: row.decade, female: 0, total: 0 };
      item.total += row.n;
      if (row.gender === 'female') item.female += row.n;
      grouped.set(row.decade, item);
    }
    return Array.from({ length: 17 }, (_, i) => {
      const decade = 1860 + i * 10;
      const item = grouped.get(decade) ?? { female: 0, total: 0 };
      return { decade, femaleShare: item.total ? item.female / item.total : 0, n: item.total };
    });
  }
</script>

<section class="scene-gender" aria-labelledby="scene-3-title">
  <div class="scene-grid">
    <div class="sticky-chart">
      <SceneTitle
        kicker="Scene 3"
        title="Parity took a century."
        subline="The y-axis is fixed at 0-60% so changes remain comparable across filters and departments."
      />
      <div class="controls">
        <DecadeSlider {timeline} ariaLabel="Filter gender chart by decade range" />
        {#if selectedCountry}
          <FilterChip label="Country" value={countryName} onRemove={clearSelectedCountry} />
        {/if}
      </div>
      {#if selectedCountry && !useCountry}
        <p class="notice">Sample too small to plot reliably; showing global trend instead.</p>
      {/if}
      {#if step < 2}
        <LineChart data={lineData} {annotations} />
      {:else}
        <SmallMultiplesGender data={genderByDepartment} />
      {/if}
      <p class="source">Source: MoMA Collection. n = {lineData.reduce((sum, d) => sum + d.n, 0).toLocaleString()} credited works.</p>
    </div>
    <div class="text-rail">
      <ScrollStep scene={3} step={0}><p>The first decades are noisy: a few credited works can swing the share sharply.</p></ScrollStep>
      <ScrollStep scene={3} step={1}><p>The durable change begins much later. The curve rises after the 1980s and approaches, but does not reach, parity.</p></ScrollStep>
      <ScrollStep scene={3} step={2}><p>Departments move at different speeds. Small multiples keep the same scale so the contrast is not exaggerated.</p></ScrollStep>
    </div>
  </div>
</section>

<style>
  .scene-gender {
    background: var(--bg-light);
    color: var(--fg-on-light-strong);
  }

  .scene-grid {
    display: grid;
    grid-template-columns: minmax(0, 3fr) minmax(18rem, 2fr);
    gap: var(--space-6);
    width: min(var(--max-content), calc(100% - var(--space-4)));
    margin: 0 auto;
    padding: var(--space-10) 0;
  }

  .sticky-chart {
    position: sticky;
    top: var(--space-2);
    align-self: start;
    min-height: calc(100vh - var(--space-4));
    display: grid;
    align-content: center;
    gap: var(--space-3);
  }

  .controls {
    display: grid;
    gap: var(--space-2);
  }

  .notice,
  .source {
    margin: 0;
    color: var(--fg-on-light-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
  }

  .text-rail {
    color: var(--fg-on-light-mute);
    font-family: var(--font-body);
    font-size: clamp(var(--type-body-size), 2vw, 1.25rem);
    line-height: var(--type-body-line);
  }

  .text-rail p {
    max-width: 28rem;
    margin: 0;
  }

  @media (max-width: 900px) {
    .scene-grid {
      grid-template-columns: 1fr;
      padding: var(--space-6) 0;
    }

    .sticky-chart {
      position: relative;
      min-height: auto;
    }
  }
</style>
