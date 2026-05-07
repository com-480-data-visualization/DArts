<script>
  import { filters, clearSelectedCountry } from '../stores/filters.js';
  import DecadeSlider from '../components/DecadeSlider.svelte';
  import FilterChip from '../components/FilterChip.svelte';
  import Legend from '../components/Legend.svelte';
  import SceneTitle from '../components/SceneTitle.svelte';
  import ScrollStep from '../components/ScrollStep.svelte';
  import Globe from '../charts/Globe.svelte';

  let { countryByDecade = [], countrySummary = [], timeline = [] } = $props();

  const topThree = new Set(['USA', 'FRA', 'DEU']);

  let step = $derived($filters.activeScene === 2 ? $filters.activeStep : 0);
  let range = $derived($filters.decadeRange);
  let selectedCountry = $derived($filters.selectedCountry);
  let summaryByIso = $derived(new Map(countrySummary.map((d) => [d.iso3, d])));
  let selectedSummary = $derived(selectedCountry ? summaryByIso.get(selectedCountry) : null);
  let topThreeShare = $derived(computeTopThreeShare(countryByDecade, range));

  function computeTopThreeShare(rows, decadeRange) {
    const counts = {};
    for (const row of rows) {
      if (row.decade === null || row.decade < decadeRange[0] || row.decade > decadeRange[1]) continue;
      counts[row.iso3] = (counts[row.iso3] || 0) + row.n;
    }
    const total = Object.values(counts).reduce((sum, n) => sum + n, 0);
    const top = [...topThree].reduce((sum, iso3) => sum + (counts[iso3] || 0), 0);
    return total ? top / total : 0;
  }
</script>

<section class="scene-globe" aria-labelledby="scene-2-title">
  <div class="globe-stage">
    <div class="globe-copy">
      <SceneTitle
        kicker="Scene 2"
        title="Three countries hold two-thirds of MoMA."
        subline="Country color uses a sequential luminance ramp on credited works. The red-orange exception marks the top three."
        dark
      />
      <div class="steps">
        <ScrollStep scene={2} step={0}><p>Artists from <strong>129</strong> recorded nationalities enter the collection.</p></ScrollStep>
        <ScrollStep scene={2} step={1}><p>But once counts appear, the map stops looking global and starts looking concentrated.</p></ScrollStep>
        <ScrollStep scene={2} step={2}><p><strong>{(topThreeShare * 100).toFixed(0)}%</strong> of mapped credited works come from the United States, France, and Germany.</p></ScrollStep>
        <ScrollStep scene={2} step={3}><p>Scrub time: the concentration bends, but it does not disappear.</p></ScrollStep>
      </div>
      <Legend mode="sequential" minLabel="< 10" midLabel="100" maxLabel=">= 1,000" caption="Color encodes credited works in the active decade range." dark />
      <p class="exclusion">Excluded: 2.3% of artist credits have no mapped nationality in the cleaned corpus.</p>
      {#if step >= 3}
        <div class="slider-panel">
          <DecadeSlider {timeline} ariaLabel="Filter globe by decade range" />
          <p class="share type-mono">Top-three share: {(topThreeShare * 100).toFixed(1)}%</p>
        </div>
      {/if}
    </div>
    <div class="globe-wrap">
      <Globe {countryByDecade} {step} />
    </div>
    {#if selectedSummary}
      <aside class="country-panel" aria-label={`Selected country ${selectedSummary.country_name}`}>
        <button type="button" class="close" aria-label="Clear selected country" onclick={clearSelectedCountry}>x</button>
        <FilterChip label="Filtered" value={selectedSummary.country_name} dark onRemove={clearSelectedCountry} />
        <h3>{selectedSummary.country_name}</h3>
        <dl>
          <div><dt>Works</dt><dd>{selectedSummary.n.toLocaleString()}</dd></div>
          <div><dt>Artists</dt><dd>{selectedSummary.n_artists.toLocaleString()}</dd></div>
          <div><dt>Top medium</dt><dd>{selectedSummary.top_medium}</dd></div>
        </dl>
        <p class="sample">
          <span>Sample artist</span>
          <strong>{selectedSummary.sample_artist}</strong>
          {selectedSummary.sample_lifespan}<br />
          <em>{selectedSummary.sample_work_title}</em>
          {#if selectedSummary.sample_work_year}, {selectedSummary.sample_work_year}{/if}
        </p>
      </aside>
    {/if}
  </div>
</section>

<style>
  .scene-globe {
    min-height: 360vh;
    color: var(--fg-on-dark-strong);
    background: var(--bg-dark);
  }

  .globe-stage {
    position: sticky;
    top: 0;
    min-height: 100vh;
    display: grid;
    grid-template-columns: var(--rail-width) minmax(0, 1fr);
    gap: var(--space-4);
    align-items: center;
    padding: var(--space-4);
  }

  .globe-copy {
    z-index: 2;
    max-height: calc(100vh - var(--space-4));
    overflow: auto;
    padding: var(--space-3);
    background: color-mix(in srgb, var(--bg-dark) 74%, transparent);
    backdrop-filter: blur(8px);
    border: 1px solid color-mix(in srgb, var(--fg-on-dark-mute) 35%, transparent);
  }

  .steps {
    margin: var(--space-3) 0;
  }

  .steps :global(.scroll-step) {
    min-height: 44vh;
  }

  .steps p {
    margin: 0;
    color: var(--fg-on-dark-mute);
    font-family: var(--font-body);
    font-size: var(--type-body-size);
    line-height: var(--type-body-line);
  }

  strong {
    color: var(--fg-on-dark-strong);
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
  }

  .exclusion,
  .share {
    margin: var(--space-1) 0 0;
    color: var(--fg-on-dark-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
    line-height: var(--type-small-line);
  }

  .slider-panel {
    margin-top: var(--space-3);
    padding: var(--space-2);
    background: var(--bg-paper);
    color: var(--fg-on-light-strong);
  }

  .globe-wrap {
    display: grid;
    place-items: center;
    min-width: 0;
  }

  .country-panel {
    position: absolute;
    right: var(--space-4);
    top: var(--space-4);
    z-index: 3;
    width: min(24rem, calc(100vw - var(--space-4)));
    padding: var(--space-3);
    color: var(--fg-on-dark-strong);
    background: color-mix(in srgb, var(--bg-dark) 88%, transparent);
    border: 1px solid var(--fg-on-dark-mute);
  }

  .close {
    position: absolute;
    top: var(--space-1);
    right: var(--space-1);
    border: 0;
    color: var(--fg-on-dark-strong);
    background: transparent;
    cursor: pointer;
  }

  h3 {
    margin: var(--space-3) 0 var(--space-2);
    color: var(--fg-on-dark-strong);
    font-family: var(--font-display);
    font-size: var(--type-h2-size);
  }

  dl {
    display: grid;
    gap: var(--space-1);
    margin: 0;
  }

  dl div {
    display: flex;
    justify-content: space-between;
    gap: var(--space-2);
  }

  dt {
    color: var(--fg-on-dark-mute);
    font-family: var(--font-ui);
  }

  dd {
    margin: 0;
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
  }

  .sample {
    margin: var(--space-3) 0 0;
    color: var(--fg-on-dark-mute);
    font-family: var(--font-body);
  }

  .sample span,
  .sample strong {
    display: block;
  }

  .sample strong {
    margin: 0.25rem 0;
    color: var(--fg-on-dark-strong);
    font-family: var(--font-ui);
  }

  @media (max-width: 900px) {
    .globe-stage {
      grid-template-columns: 1fr;
      align-content: start;
    }

    .globe-copy {
      max-height: none;
    }

    .country-panel {
      position: fixed;
      inset-inline: var(--space-2);
      top: auto;
      bottom: var(--space-2);
      width: auto;
    }
  }
</style>
